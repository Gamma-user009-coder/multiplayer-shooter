from itertools import count

from client.client import Client
from player import *
from settings import *
from slab import *
from client import *
from client.protocol import *


CLIENT_IP = "0.0.0.0"
SERVER_IP = "127.0.0.1"
SERVER_PORT = 54321
CLIENT_PORT = 12345



class Game:
    """The main class managing the game loop, assets, and objects."""

    def __init__(self, username: str, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT,fps: int = FPS):
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

    def _load_background_asset(self) -> None:
        """Loads the background image or creates a fallback."""
        try:
            self.background = pygame.image.load("gui/assets/background.jpg").convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
            print("[INFO] Background loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Could not load background.jpg: {e}. Using fallback solid color.")
            self.background = pygame.Surface((self.width, self.height))
            self.background.fill((40, 40, 50))

    def _load_sprite_sheet(self) -> None:
        """Loads the player sprite sheet or creates a fallback."""
        try:
            self.player_sheet = pygame.image.load("gui/assets/wizard_sheet.png").convert_alpha()
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
            "fireball", "gui/assets/Fireball", FIREBALL_FRAME_COUNT)
        if not self.fireball_frames:
            self.fireball_frames = self._create_fireball_fallback_frames()
            print("[INFO] Using fallback fireball frames.")

        self.explosion_frames = self._load_animation_frames(
            "explosion", "gui/assets/exp", EXPLOSION_FRAME_COUNT, EXPLOSION_SIZE)
        if not self.explosion_frames:
            self.explosion_frames = self._create_explosion_fallback_frames()
            print("[INFO] Using fallback explosion frame.")

    def _create_game_objects(self) -> None:
        """Initializes the player and all static platforms."""
        # Player initialization
        self.players = {self.client.player_id: Player(
            200, self.height - WIZARD["height"], self.group, self.player_sheet,
            self.height, self.group, self.fireball_frames, self.explosion_frames,
        False)}

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

    def handle_events(self) -> None:
        """Handles Pygame events like quit and input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                    for player_id, (hp, (x, y)) in data.items():
                        if player_id == str(self.client.player_id):
                            continue
                        elif self.players.get(int(player_id)) is None:
                            self.players[int(player_id)] = Player(
                                x, y, self.group, self.player_sheet,
                                self.height, self.group, self.fireball_frames, self.explosion_frames,
                            False)
                        else:
                            self.players[int(player_id)].rect.x = x
                            self.players[int(player_id)].rect.y = y
            except KeyError:
                pass

    def run(self) -> None:
        """The main game loop."""
        while self.running:
            self.handle_events()

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
            self.client.send_status_to_server(my_player.rect.x, my_player.rect.y)
            self.handle_packets()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
