import pygame


class BasicGameObject(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface, sprite_group: pygame.sprite.Group, layer: int):
        """
        Initialize a basic game object.

        Parameters:
        - x (int): The x-coordinate of the object's initial position.
        - y (int): The y-coordinate of the object's initial position.
        - image (pygame.Surface): The image representing the object.
        - sprite_group (pygame.sprite.Group): The sprite group to which the object belongs.
        - layer (int): The layer of the object within the sprite group.
        """
        super().__init__(sprite_group)
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))
        self.game_layer: int = layer

    def draw(self, *args):
        """
        Draw the basic game object on the screen.

        Parameters:
        - args: Additional arguments (not used in this method).
        """
        screen: pygame.Surface = args[0]
        screen.blit(self.image, self.rect)
