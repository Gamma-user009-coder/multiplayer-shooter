import pygame
from settings import *


class BasicGameObject(pygame.sprite.Sprite):
    """Base class for all static game elements."""

    def __init__(self, x: int, y: int, image: pygame.Surface, group: pygame.sprite.Group, layer: GameLayers):
        """
        Initializes a basic game object.

        :param x: Initial x-coordinate (center).
        :param y: Initial y-coordinate (center).
        :param image: The sprite image surface.
        :param group: The sprite group(s) this object belongs to.
        :param layer: The rendering layer (GameLayers enum).
        """
        super().__init__(group)
        self.image: pygame.Surface = image
        # Use the provided x, y as center for BasicGameObject
        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))
        self.game_layer: int = layer.value

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the sprite onto the screen."""
        screen.blit(self.image, self.rect)


