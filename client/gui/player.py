from settings import *
import pygame
from advanced_game_object import *
from basic_game_object import *
from custom_layered_group import *
from fireball import Fireball

# ==============================
# PLAYER HELPER FUNCTIONS
# ==============================

def _load_scaled_frames_from_sheet(sheet: pygame.Surface, row: int, count: int) -> List[pygame.Surface]:
    """
    Extracts, scales, and returns a list of animation frames from a sprite sheet row.

    :param sheet: The full sprite sheet surface.
    :param row: The row index (0-based) on the sprite sheet.
    :param count: The number of frames in the row.
    :return: List of scaled pygame.Surface frames.
    """
    frames: List[pygame.Surface] = []
    frame_size: int = WIZARD["frame_size"]
    scale: float = WIZARD["scale"]

    for col in range(count):
        rect: pygame.Rect = pygame.Rect(col * frame_size, row * frame_size, frame_size, frame_size)
        frame: pygame.Surface = sheet.subsurface(rect)
        scaled_frame: pygame.Surface = pygame.transform.scale(frame, (int(frame_size * scale),
                                                                       int(frame_size * scale)))
        frames.append(scaled_frame)
    return frames


class Player(AdvancedGameObject):
    """The main player controlled character."""

    def __init__(self, x: int, y: int, group: pygame.sprite.Group, sprite_sheet: pygame.Surface, screen_height: int,
                 render_group: 'CustomLayeredGroup', fireball_frames: List[pygame.Surface],
                 explosion_frames: List[pygame.Surface], is_enemy: bool):
        """
        Initializes the Player object.

        :param x: Initial x-coordinate.
        :param y: Initial y-coordinate.
        :param group: The sprite group(s) this object belongs to.
        :param sprite_sheet: The surface containing all player animations.
        :param screen_height: The height of the game screen for boundary checks.
        :param render_group: The group to which projectiles will be added.
        :param fireball_frames: Frames for the fireball projectile.
        :param explosion_frames: Frames for the explosion effect.
        """
        animations: Dict[str, List[pygame.Surface]] = self._extract_animations(sprite_sheet)
        super().__init__(x, y, animations, "idle", group, GameLayers.OBJECTS)
        self._setup_player_attributes(screen_height, render_group, fireball_frames, explosion_frames)
        self.is_enemy = is_enemy

    def _extract_animations(self, sheet: pygame.Surface) -> Dict[str, List[pygame.Surface]]:
        """Extracts and scales all animation sets from the sprite sheet."""
        animations: Dict[str, List[pygame.Surface]] = {}
        for name, (row, count) in WIZARD["animation_rows"].items():
            animations[name] = _load_scaled_frames_from_sheet(sheet, row, count)
        return animations

    def _setup_player_attributes(self, screen_height: int, render_group: 'CustomLayeredGroup',
                                 fireball_frames: List[pygame.Surface], explosion_frames: List[pygame.Surface]) -> None:
        """Initializes all non-animation related player attributes."""
        # The actual collision box
        self.rect: pygame.Rect = pygame.Rect((self.rect.x, self.rect.y, WIZARD["width"], WIZARD["height"]))
        self.rect.bottom = screen_height  # Initial placement at the bottom of the screen

        self.image_scale: float = WIZARD["scale"]
        self.offset: List[int] = WIZARD["offset"]

        self.gravity: int = WIZARD["gravity"]
        self.vel_y: float = 0
        self.speed: int = WIZARD["speed"]
        self.jump_power: int = WIZARD["jump_power"]
        self.jump: bool = False
        self.running: bool = False
        self.attacking: bool = False
        self.attack_cooldown: int = 0
        self.shot_fired: bool = False

        self.render_group: CustomLayeredGroup = render_group
        self.fireball_frames: List[pygame.Surface] = fireball_frames
        self.explosion_frames: List[pygame.Surface] = explosion_frames

    def shoot_fireball(self) -> None:
        """Instantiates a new fireball projectile with initial vertical velocity."""
        # Calculate the spawn position (near the wand)
        offset_x: int = WIZARD["staff_x_offset"] if self.facing_right else -WIZARD["staff_x_offset"]
        spawn_x: int = self.rect.centerx + offset_x
        spawn_y: int = self.rect.y + WIZARD["staff_y_offset"]

        direction: int = 1 if self.facing_right else -1
        initial_vel_y: float = WIZARD["initial_fireball_vel_y"]

        Fireball(spawn_x, spawn_y, direction, self.render_group,
                 self.fireball_frames, self.explosion_frames, initial_vel_y)

    def _apply_gravity_and_vertical_movement(self, dy: int, screen_height: int, platforms: List['Slab']) -> Tuple[int, int]:
        """Applies gravity, checks vertical collision with platforms, and returns adjusted dy."""
        # Apply Gravity
        self.vel_y += self.gravity
        dy += int(self.vel_y)

        # Platform Collision (Vertical Movement)
        for platform in platforms:
            # Check for potential collision with vertical movement applied
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                # Falling onto the platform (Top collision)
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.jump = False
                    dy = 0  # Resolve movement
                # Jumping into the bottom of the platform (Bottom collision)
                elif self.vel_y < 0 and self.rect.top >= platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                    dy = 0

        # Ground boundary check
        if self.rect.bottom + dy > screen_height:
            dy = screen_height - self.rect.bottom
            self.vel_y = 0
            self.jump = False

        self.rect.y += dy
        return dy, self.vel_y

    def _apply_horizontal_movement(self, dx: int, screen_width: int) -> int:
        """Applies horizontal movement and checks screen boundaries."""
        self.rect.x += dx

        # Horizontal boundary check
        if self.rect.left  < 30:
            self.rect.left = 30
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        return dx

    def handle_input(self, screen_width: int, screen_height: int, platforms: List['Slab']) -> None:
        """Handles player movement, gravity, and collision with platforms."""
        keys: Any = pygame.key.get_pressed()
        dx: int = 0
        dy: int = 0
        self.running = False

        # Movement Input
        if not self.attacking:
            if keys[pygame.K_a]:
                dx = -self.speed
                self.running = True
                self.facing_right = False
            if keys[pygame.K_d]:
                dx = self.speed
                self.running = True
                self.facing_right = True
            if keys[pygame.K_w] and not self.jump:
                self.vel_y = self.jump_power
                self.jump = True

        self._apply_horizontal_movement(dx, screen_width)
        self._apply_gravity_and_vertical_movement(dy, screen_height, platforms)

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def attack(self) -> None:
        """Starts the attack animation if the cooldown is ready."""
        if self.attack_cooldown == 0 and not self.attacking:
            self.attacking = True
            self.frame_index = 0
            self.shot_fired = False

    def update_status(self) -> None:
        """Determines the current animation status based on player state."""
        if self.attacking:
            self.set_status("attack1")
        elif self.jump:
            self.set_status("jump")
        elif self.running:
            self.set_status("run")
        else:
            self.set_status("idle")

    def _handle_attack_logic(self) -> None:
        """Handles fireball spawning and resets attack state once animation finishes."""
        if self.attacking and self.status == "attack1":
            # Fireball spawning logic: shoots on frame 4 of the attack animation
            if self.frame_index == 4 and not self.shot_fired:
                self.shoot_fireball()
                self.shot_fired = True

            # Check if attack animation finished
            if self.frame_index >= len(self.animations[self.status]) - 1:
                self.attacking = False
                self.attack_cooldown = WIZARD["attack_cooldown"]

    def update(self, screen_width: int, screen_height: int, platforms: List['Slab']) -> None:
        """Main update loop, handles input, status, and animation."""
        if not self.is_enemy:
            self.handle_input(screen_width, screen_height, platforms)
        self.update_status()
        self.update_animation()
        self._handle_attack_logic()

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the player sprite, adjusting position by the offset to align with the collision rect."""
        img: pygame.Surface = self.image
        # Using the defined scale to center the image better in the collision box
        screen.blit(img, (self.rect.x - (self.offset[0] * self.image_scale),
                          self.rect.y - (self.offset[1] * self.image_scale)))

