import threading
from itertools import count
from time import sleep

import pygame

from client.client import Client
from client.gui.loading_screen import LoadingScreen
from player import *
from settings import *
from slab import *
from client import *
from client.protocol import *

CLOSE_CLIENT_EVENT = pygame.USEREVENT + 1
END_SCREEN_DURATION = 5  # seconds
CLIENT_IP = "0.0.0.0"
SERVER_IP = "127.0.0.1"
# SERVER_IP = "172.20.20.23"
SERVER_PORT = 54321
CLIENT_PORT = 12345


class Game:
    """The main class managing the game loop, assets, and objects."""

    def __init__(self, username: str, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT, fps: int = FPS):
        """
        Initializes the Pygame window, assets, and game objects.

        :param width: Screen width.
        :param height: Screen height.
        :param fps: Frames per second limit.
        """


        pygame.init()
        self.window: pygame.Surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Wizard Platformer Example")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = True
        self.width: int = width
        self.height: int = height
        self.group: CustomLayeredGroup = CustomLayeredGroup()
        self.platforms: List[Slab] = []

        # Asset placeholders
        self.background: pygame.Surface
        self.player_sheet: pygame.Surface
        self.fireball_frames: List[pygame.Surface]
        self.explosion_frames: List[pygame.Surface]
        self.client = Client(CLIENT_IP, CLIENT_PORT, SERVER_IP, SERVER_PORT, username)
        self.client.connect_to_server()
        self.client.wait_for_id()

        self._load_assets()
        self._create_game_objects()
        self.enemy_projectile = Fireball(-100, -100, 0, self.group,
                                         self.fireball_frames, self.explosion_frames, WIZARD["initial_fireball_vel_y"])
        self.enemy_projectile.is_enemy = True
        self.enemy_fireball_fired = False
        self.update_gui = False

        # --- Game State Variables for End Screen ---
        self.game_over: bool = False
        self.win_status: Optional[bool] = None  # True for win, False for loss, None for ongoing
        self.end_screen_start_time: Optional[float] = None
        self.end_screen_font: pygame.font.Font = pygame.font.Font(None, 74)
        self.small_font: pygame.font.Font = pygame.font.Font(None, 36)
        # --- End Game State Variables ---

    def _load_background_asset(self) -> None:
        """Loads the background image or creates a fallback."""
        try:
            self.background = pygame.image.load("assets/background.jpg").convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
            print("[INFO] Background loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Could not load background.jpg: {e}. Using fallback solid color.")
            self.background = pygame.Surface((self.width, self.height))
            self.background.fill((40, 40, 50))

    def _load_sprite_sheet(self) -> None:
        """Loads the player sprite sheet or creates a fallback."""
        try:
            self.player_sheet = pygame.image.load("assets/wizard_sheet.png").convert_alpha()
            print("[INFO] Wizard sprite sheet loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Could not load wizard_sheet.png: {e}. Using fallback surface.")
            # Fallback size based on max frames (8) and rows (7)
            self.player_sheet = pygame.Surface((WIZARD["frame_size"] * 8, WIZARD["frame_size"] * 7))
            self.player_sheet.fill((255, 0, 255))

    def _load_animation_frames(self, name: str, folder: str, count: int, scale_to: int = 0) -> List[pygame.Surface]:
        """Loads a sequence of numbered animation frames from a folder."""
        frames: List[pygame.Surface] = []
        try:
            print(f"[INFO] Attempting to load {count} {name} images from '{folder}/[i].png'...")
            for i in range(1, count + 1):
                path: str = f"{folder}/{i}.png"
                frame: pygame.Surface = pygame.image.load(path).convert_alpha()
                if scale_to > 0:
                    frame = pygame.transform.scale(frame, (scale_to, scale_to))
                frames.append(frame)
            if len(frames) != count:
                raise RuntimeError(f"Not all {name} files were loaded.")
            print(f"[INFO] Successfully loaded all {count} {name} frames.")
        except Exception as e:
            print(f"[ERROR] Failed to load {name} images (Error: {e}).")
            return []
        return frames

    def _create_fireball_fallback_frames(self) -> List[pygame.Surface]:
        """Generates fallback fireball frames if asset loading fails."""
        frames: List[pygame.Surface] = []
        FIREBALL_FALLBACK_COUNT: int = 15
        FIREBALL_SIZE: int = 60
        for i in range(FIREBALL_FALLBACK_COUNT):
            frame: pygame.Surface = pygame.Surface((FIREBALL_SIZE, FIREBALL_SIZE), pygame.SRCALPHA)
            center: Tuple[int, int] = (FIREBALL_SIZE // 2, FIREBALL_SIZE // 2)
            idx: int = i if i < FIREBALL_FALLBACK_COUNT / 2 else FIREBALL_FALLBACK_COUNT - i
            radius_outer: float = 25 + (idx * 1.5)
            radius_core: float = 10 + idx * 0.5
            # Simplified drawing logic for fallback
            pygame.draw.circle(frame, (255, 120, 0, 150), center, int(radius_outer), 0)
            pygame.draw.circle(frame, (255, 180, 0), center, int(radius_outer - 5), 0)
            pygame.draw.circle(frame, (255, 255, 100), center, int(radius_core), 0)
            frames.append(frame)
        return frames

    def _create_explosion_fallback_frames(self) -> List[pygame.Surface]:
        """Creates a simple fallback explosion frame if asset loading fails."""
        frame: pygame.Surface = pygame.Surface((EXPLOSION_SIZE, EXPLOSION_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(frame, (255, 100, 0), (EXPLOSION_SIZE // 2, EXPLOSION_SIZE // 2), EXPLOSION_SIZE // 2, 0)
        return [frame]

    def _load_assets(self) -> None:
        """Orchestrates the loading of all game assets."""
        self._load_background_asset()
        self._load_sprite_sheet()

        self.fireball_frames = self._load_animation_frames(
            "fireball", "assets/Fireball", FIREBALL_FRAME_COUNT)
        if not self.fireball_frames:
            self.fireball_frames = self._create_fireball_fallback_frames()
            print("[INFO] Using fallback fireball frames.")

        self.explosion_frames = self._load_animation_frames(
            "explosion", "assets/exp", EXPLOSION_FRAME_COUNT, EXPLOSION_SIZE)
        if not self.explosion_frames:
            self.explosion_frames = self._create_explosion_fallback_frames()
            print("[INFO] Using fallback explosion frame.")

    def _create_game_objects(self) -> None:
        """Initializes the player and all static platforms."""
        # Player initialization
        self.players = {}

        # SLAB CREATION (Constant Positions)
        slab_data: List[Tuple[int, int, int, int]] = [
            (30, self.height - 150, 150, 20),
            (50, self.height - 350, 150, 20),
            (350, self.height - 200, 300, 20),
            (750, self.height - 300, 150, 20),
        ]

        for x, y, w, h in slab_data:
            slab: Slab = Slab(x, y, w, h, self.group)
            self.platforms.append(slab)


    def set_game_over(self, win: bool):
        """
        Sets the game state to game_over, records win/loss status,
        starts the timer for automatic closing, and marks the end screen start time.

        :param win: True if the local player won, False if they lost.
        """
        if not self.game_over:
            self.game_over = True
            self.win_status = win
            self.end_screen_start_time = pygame.time.get_ticks() / 1000.0  # Time in seconds

            # Start a timer thread to post the close event after the delay
            threading.Timer(END_SCREEN_DURATION,
                            lambda: pygame.event.post(pygame.event.Event(CLOSE_CLIENT_EVENT))).start()
            print(f"[INFO] Game Over: {'Win' if win else 'Loss'}. Client will close in {END_SCREEN_DURATION} seconds.")

    def display_end_screen(self):
        """Draws the victory or loss screen with the username and countdown."""
        if self.win_status is None:
            return

        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with 180/255 opacity
        self.window.blit(overlay, (0, 0))

        # Determine message and color
        if self.win_status:
            main_text = f"VICTORY, {self.client.username.upper()}!"
            color = (0, 255, 0)  # Green
        else:
            main_text = f"DEFEAT, {self.client.username.upper()}"
            color = (255, 0, 0)  # Red

        # Main message rendering
        text_surface = self.end_screen_font.render(main_text, True, color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 40))
        self.window.blit(text_surface, text_rect)

        # Countdown message rendering
        time_elapsed = (pygame.time.get_ticks() / 1000.0) - self.end_screen_start_time
        time_remaining = max(0, END_SCREEN_DURATION - time_elapsed)
        countdown_text = f"Closing in {int(time_remaining) + 1} seconds..."  # +1 for a more natural countdown start

        countdown_surface = self.small_font.render(countdown_text, True, (200, 200, 200))  # Light Gray
        countdown_rect = countdown_surface.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.window.blit(countdown_surface, countdown_rect)


    def handle_events(self) -> None:
        """Handles Pygame events like quit and input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == CLOSE_CLIENT_EVENT:
                print("[INFO] Received CLOSE_CLIENT_EVENT. Shutting down...")
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.players[self.client.player_id].attack()

    def handle_packets(self):
        packets = self.client.connection.get_packets()
        for packet in packets:
            try:
                data, address = packet
                if data["id"] == ServerPackets.GAME_STATUS.value:
                    data.pop("id")
                    projectiles: list[tuple[int, tuple[int, int]]] = data.get("projectiles")
                    data.pop("projectiles")
                    # print(data)
                    for player_id, (hp, (x, y)) in data.items():
                        self.players[int(player_id)].current_health = hp
                        if player_id != str(self.client.player_id):
                            self.players[int(player_id)].update_enemy(x, y)


                            if projectiles:
                                for (team_id, (px, py)) in projectiles:
                                    if team_id != str(self.client.player_id):
                                        if self.players[int(team_id)].flag:
                                            self.players[int(team_id)].attack()
                                            self.players[int(team_id)].flag = False

                                        self.players[int(team_id)].attack_cooldown = WIZARD["attack_cooldown"]
                                        self.enemy_projectile.rect.x = px
                                        self.enemy_projectile.rect.y = py
                            else:
                                self.enemy_fireball_fired = False
                                self.players[int(player_id)].flag = True

                                Explosion(self.enemy_projectile.rect.centerx, self.enemy_projectile.rect.centery, self.enemy_projectile.groups()[0],
                                self.enemy_projectile.explosion_frames)
                                self.enemy_projectile.rect.x = -200
                                self.enemy_projectile.rect.y = -200





                elif data["id"] == ServerPackets.START_GAME.value:
                    data.pop("id")
                    print(data)
                    for player_id, (username, (x, y)) in data.items():
                        player_id = int(player_id)
                        if player_id == self.client.player_id:
                            is_enemy = False
                        else:
                            is_enemy = True
                        self.players[int(player_id)] = Player(
                            x, y, self.group, self.player_sheet,
                            self.height, self.group, self.fireball_frames, self.explosion_frames,
                            is_enemy, username)
                    self.update_gui = True
                    return False


            except KeyError:
                pass

        # --- Check for Game Over condition after processing all packets ---
        if self.update_gui and not self.game_over :
            for player_id, player in self.players.items():
                if player.current_health <= 0:
                    self.set_game_over(player_id != self.client.player_id)  # Local player lost
        # --- End Game Over Check ---

        return True

    def run(self) -> None:

        """The main game loop."""
        while self.running:
            self.handle_packets()
            if self.update_gui:
                self.handle_events()

                if self.game_over:
                    # If game is over, only draw the end screen and flip
                    self.display_end_screen()
                    pygame.display.flip()
                    self.clock.tick(FPS)
                    continue  # Skip the rest of the game loop updates


                # Draw background
                self.window.blit(self.background, (0, 0))

                # Update player (needs platforms for collision)
                for player_id, player in self.players.items():
                    player.update(self.width, self.height, self.platforms)

                # Update the rest of the sprites (Fireballs and Explosions)
                self.group.update(self.width, self.height, self.platforms)

                # Draw all sprites using the layered group
                self.group.render(self.window)

                my_player = self.players[self.client.player_id]
                if my_player.fireball is not None and my_player.fireball.alive:
                    self.client.send_status_to_server(my_player.rect.x, my_player.rect.y, my_player.fireball.rect.x,
                                                      my_player.fireball.rect.y)
                else:
                    self.client.send_status_to_server(my_player.rect.x, my_player.rect.y)

                pygame.display.flip()
                self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
