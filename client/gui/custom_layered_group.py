import pygame
from typing import List
from fireball import Fireball
from explosion import Explosion


class CustomLayeredGroup(pygame.sprite.Group):
    """A group that renders sprites based on their 'game_layer' attribute."""

    def update(self, screen_width: int, screen_height: int, platforms: List['Slab'] = None) -> None:
        """
        Custom update method to pass required arguments to sprites.

        :param screen_width: The width of the screen.
        :param screen_height: The height of the screen.
        :param platforms: List of platforms for collision (used by some sprites like Fireball).
        """
        for sprite in self.sprites():
            # Only update AdvancedGameObject subtypes (Explosion, Fireball) here
            if isinstance(sprite, (Fireball, Explosion)):
                sprite.update(screen_width, screen_height, platforms)

    def render(self, screen: pygame.Surface) -> None:
        """Renders sprites in order of their game_layer."""
        for sprite in sorted(self.sprites(), key=lambda s: getattr(s, "game_layer", 0)):
            # Sprites must have a draw method
            sprite.draw(screen)