from typing import Union, Dict, List, Tuple
import pygame
from src.client.general_game_objects.basic_game_object import BasicGameObject
from src.client.general.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class AdvancedGameObject(BasicGameObject):
    def __init__(self, x: int, y: int, angle: float, animation_dictionary: Dict[str, List[pygame.Surface]],
                 status: str, sprite_group: pygame.sprite.Group, layer: int):
        """
        Initialize an advanced game object.

        Parameters:
        - x (int): The x-coordinate of the object's initial position.
        - y (int): The y-coordinate of the object's initial position.
        - angle (float): The initial angle of the object.
        - animation_dictionary (Dict[str, List[pygame.Surface]]): A dictionary mapping animation names to lists of surfaces.
        - status (str): The initial status of the object.
        - sprite_group (pygame.sprite.Group): The sprite group to which the object belongs.
        - layer (int): The layer of the object within the sprite group.
        """
        super().__init__(x, y, pygame.Surface((0, 0)), sprite_group, layer)
        self.original_image = None
        self.angle: float = angle
        self.x: int = x
        self.y: int = y
        self.animations: Dict[str, List[pygame.Surface]] = animation_dictionary
        self.status: str = status
        self.frame_index: int = 0
        self.animation_comedown: int = 100
        self.last_frame_time: int = pygame.time.get_ticks()
        self.previous_location = (x, y)
        self.temp_location = (x, y)

    def update_pos(self, x: int, y: int) -> None:
        """
        Update the position of the object.

        Parameters:
        - x (int): The new x-coordinate.
        - y (int): The new y-coordinate.
        """
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(x, y))

    def update_status(self, status: str) -> None:
        """
        Update the status of the object.

        Parameters:
        - status (str): The new status.
        """
        if status in self.animations:
            self.status = status
        self.frame_index = 0

    def update_angle_and_rotate(self, angle: Union[float, int]) -> None:
        """
        Update the angle of the object and rotate its image.

        Parameters:
        - angle (Union[float, int]): The new angle.
        """
        self.angle = angle
        if self.original_image is not None:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def animate(self) -> None:
        """Animate the object."""
        current_time: int = pygame.time.get_ticks()
        if current_time - self.last_frame_time > self.animation_comedown:
            animation: List[pygame.Surface] = self.animations.get(self.status, [])  # Using get method to avoid KeyError
            self.frame_index += 1
            if self.frame_index >= len(animation):
                self.frame_index = 0

            self.original_image = animation[self.frame_index]
            self.image = self.original_image
            self.rect = self.image.get_rect(center=(self.x, self.y))

            self.last_frame_time = current_time
            self.update_angle_and_rotate(self.angle)

    def draw(self, *args):
        """
        Draw the object on the screen.

        Parameters:
        - args: Additional arguments (not used in this method).
        """
        screen: pygame.Surface = args[0]
        player_x: int = args[1]
        player_y: int = args[2]
        origin: Tuple[int, int] = (player_x - SCREEN_WIDTH // 2, player_y - SCREEN_HEIGHT // 2)
        screen.blit(self.image, (
            -origin[0] + self.x - self.rect.width // 2,
            -origin[1] + self.y - self.rect.height // 2))

    def check_collision_with_object(self, other_object: 'AdvancedGameObject') -> bool:
        """
        Check if the current object collides with another object.

        Parameters:

        other_object (AdvancedGameObject): The other object to check for collision.

        Returns:

        bool: True if a collision occurs, False otherwise."""

        if self.rect.colliderect(
                other_object.rect):
            self_mask = pygame.mask.from_surface(self.image)
            other_mask = pygame.mask.from_surface(other_object.image)
            offset = (other_object.rect.x - self.rect.x, other_object.rect.y - self.rect.y)
            overlap = self_mask.overlap(other_mask, offset)
            return overlap is not None

