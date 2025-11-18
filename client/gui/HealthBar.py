import pygame
# Assuming settings.py defines Colors and GameLayers
from settings import Colors, GameLayers
from basic_game_object import BasicGameObject


class HealthBar(BasicGameObject):
    """
    A visual representation of an entity's health designed to follow a sprite.
    """

    def __init__(self, width: int, height: int, max_health: int, group: pygame.sprite.Group):
        # Initial dummy values for x, y, and current_health
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health

        # Create the initial image (full health)
        initial_image = self._create_bar_image()

        # Initialize the parent class with (0, 0) as a starting point
        # The position will be immediately updated by the owning object (Player)
        super().__init__(0, 0, initial_image, group, GameLayers.UI)

        # Adjust the layer to ensure it always draws on top of the character
        self.game_layer = GameLayers.UI.value

    def _create_bar_image(self) -> pygame.Surface:
        """Creates or updates the internal image surface based on current health."""

        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        health_ratio = self.current_health / self.max_health
        current_bar_width = int(self.width * health_ratio)

        # Draw a black border
        pygame.draw.rect(image, Colors.BLACK, (0, 0, self.width, self.height), 2)

        # Determine fill color
        if health_ratio > 0.6:
            color = Colors.GREEN
        elif health_ratio > 0.3:
            color = Colors.YELLOW
        else:
            color = Colors.RED

        # Draw the health fill
        fill_rect = pygame.Rect(1, 1, current_bar_width - 2, self.height - 2)
        pygame.draw.rect(image, color, fill_rect)

        return image

    def update_bar(self, current_health: int, new_x: int, new_y: int) -> None:
        """
        Updates both the health value and the bar's position.

        :param current_health: The entity's current health.
        :param new_x: The x-coordinate of the bar's top-left corner.
        :param new_y: The y-coordinate of the bar's top-left corner.
        """
        # 1. Update position
        self.rect.topleft = (new_x, new_y)

        # 2. Update health and image only if health changed
        if current_health != self.current_health:
            self.current_health = max(0, min(current_health, self.max_health))
            self.image = self._create_bar_image()