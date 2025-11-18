import pygame
import math
from threading import Lock

class Projectile(pygame.sprite.Sprite):

    rect: pygame.Rect
    mask: pygame.Mask
    v: pygame.Vector2
    explosion_r: int
    explosion_mask: pygame.Mask
    explosion_dist: tuple[int, int]
    team_id: int
    x: float
    y: float

    lock: Lock

    WIDTH = 20
    HEIGHT = 20
    DEFAULT_ANGLE = math.pi / 4
    DEFAULT_BASE_V = 100
    GRAVITY = -120
    DEFAULT_EXPLOSION_R = 50

    def __init__(self,
                 team_id: int,
                 x: float,
                 y: float,
                 angle: float = DEFAULT_ANGLE,
                 velocity: float = DEFAULT_BASE_V,
                 explosion_r: int = DEFAULT_EXPLOSION_R,
                 width: int = WIDTH,
                 height: int = HEIGHT,):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.Mask((self.rect.width, self.rect.height), fill=True)
        self.v = pygame.Vector2.from_polar((velocity, angle))
        self.team_id = team_id
        self.explosion_r = explosion_r

        expl_surface = pygame.Surface((2 * self.explosion_r, 2 * self.explosion_r), pygame.SRCALPHA)
        pygame.draw.circle(expl_surface, pygame.Color(255, 255, 255), (self.explosion_r, self.explosion_r), self.explosion_r)
        self.explosion_mask = pygame.mask.from_surface(expl_surface)
        self.explosion_dist = (int(self.x - self.explosion_r), int(self.y - self.explosion_r))

        self.lock = Lock()

    # @property
    # def x(self):
    #     return self.rect.x
    # @x.setter
    # def x(self, value):
    #     self.rect.x = value
    # @property
    # def y(self):
    #     return self.rect.y
    # @y.setter
    # def y(self, value):
    #     self.rect.y = value


    def update_position(self, dt: float) -> None:
        self.lock.acquire()
        self.v.y -= self.GRAVITY * dt
        self.x += self.v.x * dt
        self.y += self.v.y * dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.explosion_dist = (int(self.x - self.explosion_r), int(self.y - self.explosion_r))
        self.lock.release()



    # def check_collision(self, level: Level, players: dict[int, Player]) -> Collision:
    #     pygame.
