from advanced_game_object import AdvancedGameObject
from settings import *
from explosion import Explosion


class Fireball(AdvancedGameObject):
    """
    A projectile shot by the player with parabolic motion.
    """

    def __init__(self, x: int, y: int, direction: int, group: pygame.sprite.Group, frames: List[pygame.Surface],
                 explosion_frames: List[pygame.Surface], initial_vel_y: float):
        """
        Initializes a Fireball projectile.

        :param x: Spawn center x-coordinate.
        :param y: Spawn center y-coordinate.
        :param direction: 1 for right, -1 for left.
        :param group: The sprite group(s) this object belongs to.
        :param frames: List of surfaces for the fireball flight animation.
        :param explosion_frames: List of surfaces for the explosion effect.
        :param initial_vel_y: Initial vertical velocity (negative for upward launch).
        """
        animations: Dict[str, List[pygame.Surface]] = {"fly": frames}
        super().__init__(x, y, animations, "fly", group, GameLayers.OBJECTS)

        self.direction: int = direction
        self.speed: int = FIREBALL_SPEED
        self.lifetime: int = FIREBALL_LIFETIME

        self.explosion_frames: List[pygame.Surface] = explosion_frames

        # Parabolic Motion Variables
        self.gravity: float = FIREBALL_GRAVITY
        self.vel_y: float = initial_vel_y

        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))
        self.facing_right: bool = direction > 0
        self.flip_image: bool = False

    def _check_kill_conditions(self, screen_width: int, screen_height: int) -> bool:
        """Checks if the fireball should be killed (off-screen, hit lifetime)."""
        is_off_screen: bool = (self.rect.right - self.rect.width + 10 < 0 or
                               self.rect.left + self.rect.width + FIREBALL_RIGHT_OFFSET_EXPLOSION > screen_width or
                               self.rect.top > screen_height)

        self.lifetime -= 1
        is_dead_from_lifetime: bool = (self.lifetime <= 0)

        if is_off_screen or is_dead_from_lifetime:
            # Spawn the explosion at the current center position
            if self.explosion_frames and self.groups():
                # Use the first group (the main render group) for spawning
                Explosion(self.rect.centerx, self.rect.centery, self.groups()[0], self.explosion_frames)
            self.kill()
            return True
        return False

    def update(self, screen_width: int, screen_height: int, platforms: List['Slab'] = None) -> None:
        """Move the fireball, apply gravity, and check boundaries."""
        # Note: platforms argument is ignored but kept for compatibility.

        # 1. Horizontal Movement
        self.rect.x += self.direction * self.speed

        # 2. Vertical Movement (Parabola)
        self.vel_y += self.gravity
        self.rect.y += int(self.vel_y)  # vel_y is float, rect needs int

        # 3. Check for explosion and removal
        if self._check_kill_conditions(screen_width, screen_height):
            return

        self.update_animation()

