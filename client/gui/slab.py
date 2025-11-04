from basic_game_object import BasicGameObject
import pygame
from settings import *

class Slab(BasicGameObject):
    """
    A static platform object with a stylized drawn design for collision.
    """

    def __init__(self, x: int, y: int, width: int, height: int, group: pygame.sprite.Group):
        """
        Initializes a Slab platform.

        :param x: Top-left x-coordinate.
        :param y: Top-left y-coordinate.
        :param width: Width of the slab.
        :param height: Height of the slab.
        :param group: The sprite group(s) this object belongs to.
        """
        # Create a surface for the slab with transparency
        image: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Call super with the image. x and y are for the top-left of the slab, but BasicGameObject uses center.
        # We override rect below.
        super().__init__(x, y, image, group, GameLayers.MAP)

        self.width: int = width
        self.height: int = height
        # Correct rect to use top-left coordinates for platform placement
        self.rect: pygame.Rect = self.image.get_rect(topleft=(x, y))
        self.is_platform: bool = True

        self._draw_slab_design()

    def _draw_slab_design(self) -> None:
        """Draws a stylized stone slab texture onto the slab surface using constants."""

        # BASE FILL & HIGHLIGHT
        self.image.fill(BASE_COLOR)
        pygame.draw.rect(self.image, HIGHLIGHT_COLOR,
                         (0, 0, self.width, HIGHLIGHT_HEIGHT))

        # VERTICAL "CRACK" LINES
        step: int = max(MIN_VERTICAL_STEP, self.width // 8)
        # Using floor division in range ensures it doesn't go over the width boundary
        for i in range(1, self.width // step + 1):
            x_pos: int = i * step
            pygame.draw.line(self.image, CRACK_COLOR,
                             (x_pos, 0), (x_pos, self.height), LINE_WIDTH)

        # HORIZONTAL "LAYER" LINES
        layer_height: int = self.height // HORIZONTAL_DIVISIONS
        for i in range(1, HORIZONTAL_DIVISIONS):
            y_pos: int = i * layer_height
            pygame.draw.line(self.image, CRACK_COLOR,
                             (0, y_pos), (self.width, y_pos), LINE_WIDTH)

        # BORDER OUTLINE
        pygame.draw.rect(self.image, BORDER_COLOR,
                         (0, 0, self.width, self.height), BORDER_WIDTH)
