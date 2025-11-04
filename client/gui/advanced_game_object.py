import pygame
import sys
from enum import Enum, auto
from typing import Dict, List, Tuple, Any
from basic_game_object import BasicGameObject
from settings import *

class AdvancedGameObject(BasicGameObject):
    """Base class for animated objects like players, enemies, and projectiles."""

    def __init__(self, x: int, y: int, animations: Dict[str, List[pygame.Surface]], status: str,
                 group: pygame.sprite.Group, layer: GameLayers):
        """
        Initializes an advanced, animated game object.

        :param x: Initial x-coordinate.
        :param y: Initial y-coordinate.
        :param animations: Dictionary mapping status strings to lists of frame surfaces.
        :param status: Initial animation status (e.g., "idle", "run").
        :param group: The sprite group(s) this object belongs to.
        :param layer: The rendering layer (GameLayers enum).
        """
        # Start with a placeholder surface; actual image set in update_animation
        super().__init__(x, y, pygame.Surface((1, 1), pygame.SRCALPHA), group, layer)
        self.animations: Dict[str, List[pygame.Surface]] = animations
        self.status: str = status
        self.frame_index: int = 0
        self.animation_cooldown: int = DEFAULT_COOLDOWN
        self.update_time: int = pygame.time.get_ticks()

        self.facing_right: bool = True
        # Set initial image from animations
        self.image: pygame.Surface = self.animations[self.status][self.frame_index]

    def set_status(self, new_status: str) -> None:
        """Changes the current animation status and resets frame index."""
        if self.status != new_status:
            self.status = new_status
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_animation(self) -> None:
        """Advances the animation frame based on cooldown."""
        frames: List[pygame.Surface] = self.animations.get(self.status, [])
        if not frames:
            return

        # Update the image to the current frame
        self.image = frames[self.frame_index]

        # Check if enough time has passed to advance the frame
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.update_time = pygame.time.get_ticks()

        # Flip the sprite if facing left
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

