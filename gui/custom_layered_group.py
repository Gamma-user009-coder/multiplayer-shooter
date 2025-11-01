import pygame
from typing import List
from src.client.general_game_objects.basic_game_object import BasicGameObject
from src.client.general_game_objects.advanced_game_object import AdvancedGameObject


class CustomLayeredGroup(pygame.sprite.Group):
    def render(self, screen: pygame.Surface, player_x: int, player_y: int) -> None:
        """
        Render the sprites in the group.

        Parameters:
        - screen (pygame.Surface): The surface to render the sprites on.
        - player_x (int): The x-coordinate of the player.
        - player_y (int): The y-coordinate of the player.
        """
        sprites: List[pygame.sprite.Sprite] = self.sprites()
        sorted_list: List[pygame.sprite.Sprite] = sorted(sprites, key=lambda sprite: sprite.game_layer)
        for game_sprite in sorted_list:
            if isinstance(game_sprite, AdvancedGameObject):
                game_sprite.draw(screen, player_x, player_y)
            elif isinstance(game_sprite, BasicGameObject):
                game_sprite.draw(screen)
