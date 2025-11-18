import pygame
import csv

from Projectile import Projectile

class Level:

    mask: pygame.Mask
    screen_hitbox: pygame.Rect

    DEFAULT_MASK = pygame.Mask((800, 800))
    MIN_X = -1000
    MIN_Y = -1000
    MAX_X = 1920
    MAX_Y = 1080
    SCREEN_EDGE_BUFFER = 50

    def __init__(self, mask: pygame.Mask = DEFAULT_MASK):
        self.mask = mask
        self.screen_hitbox = pygame.Rect(self.MIN_X, self.MIN_Y, self.MAX_X - self.MIN_X, self.MAX_Y - self.MIN_Y)

    def load(self, path: str):
        with open(path, "rt") as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                x1, y1, w, h = row
                box = pygame.Mask((int(w), int(h)), fill=True)
                self.mask.draw(other=box, offset=(int(x1), int(y1)))

    def collide_projectiles(self, projectiles: list[Projectile]) -> list[int]:
        """Returns indexes of collided projectiles"""
        res = []
        for i, proj in enumerate(projectiles):
            if self.mask.overlap(proj.mask, (proj.x, proj.y)):
                res.append(i)
        return res
