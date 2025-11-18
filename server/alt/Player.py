import pygame
from threading import Lock

from Projectile import Projectile

class Player(pygame.sprite.Sprite):

    rect: pygame.rect.Rect
    mask: pygame.Mask
    hp: int
    team_id: int

    lock: Lock

    WIDTH = 50
    HEIGHT = 50
    MIN_HP = 0
    MAX_HP = 100
    BOMB_DAMAGE = 50

    def __init__(self,team_id: int, x: int, y: int):
        super().__init__()
        self.rect = pygame.rect.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.mask = pygame.Mask((self.WIDTH, self.HEIGHT), fill=True)
        self.hp = self.MAX_HP
        self.team_id = team_id

        self.lock = Lock()

    def make_hit(self):
        self.lock.acquire()
        self.hp -= self.BOMB_DAMAGE
        self.check_death()
        self.lock.release()

    def check_death(self):
        self.lock.acquire()
        if self.hp < self.MIN_HP:
            print("dead!")
        self.lock.release()

    def same_team(self, team_id: int):
        return self.team_id == team_id

    def to_tuple(self):
        self.lock.acquire()
        res = (self.hp, (self.rect.x, self.rect.y))
        self.lock.release()
        return res


    def collide_projectiles(self, projectiles: list[Projectile]):
        res = []
        self.lock.acquire()
        for proj in projectiles:
            if self.rect.colliderect(proj.rect):
                res.append(proj)
        self.lock.release()
        return res

    def check_projectile_hit(self, projectile: Projectile):
        self.lock.acquire()
        collide = self.mask.overlap(projectile.explosion_mask, projectile.explosion_dist)
        self.lock.release()
        return collide
