from advanced_game_object import AdvancedGameObject
from settings import *

class Explosion(AdvancedGameObject):
    """
    Temporary sprite that plays an animation once and then removes itself.
    """

    def __init__(self, x: int, y: int, group: pygame.sprite.Group, frames: List[pygame.Surface]):
        """
        Initializes an Explosion object.

        :param x: Center x-coordinate.
        :param y: Center y-coordinate.
        :param group: The sprite group(s) this object belongs to.
        :param frames: List of surfaces for the explosion animation.
        """
        animations: Dict[str, List[pygame.Surface]] = {"explode": frames}
        # Start the animation at frame 0
        super().__init__(x, y, animations, "explode", group, GameLayers.OBJECTS)

        # Override cooldown to speed up explosion
        self.animation_cooldown: int = EXPLOSION_COOLDOWN

        # Center the rect using the size of the first frame
        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))

        # Flag to track if the animation has completed
        self.is_finished: bool = False

    def update_animation(self) -> None:
        """Advances the animation frame once and kills the sprite when done."""
        if self.is_finished:
            return

        frames: List[pygame.Surface] = self.animations[self.status]
        self.image = frames[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

            if self.frame_index >= len(frames):
                # Animation finished!
                self.is_finished = True
                self.kill()

    def update(self, screen_width: int, screen_height: int, platforms: List['Slab'] = None) -> None:
        """Main update loop."""
        # Note: platforms argument is ignored but kept for compatibility with CustomLayeredGroup.update call.
        self.update_animation()
