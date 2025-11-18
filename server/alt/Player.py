import pygame

from Projectile import Projectile

class Player(pygame.sprite.Sprite):

    rect: pygame.rect.Rect
    mask: pygame.Mask
    hp: int
    team_id: int

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

    def make_hit(self):
        self.hp -= self.BOMB_DAMAGE
        self.check_death()

    def check_death(self):
        if self.hp < self.MIN_HP:
            ...

    def same_team(self, team_id: int):
        return self.team_id == team_id

    def to_tuple(self):
        return self.hp, (self.rect.x, self.rect.y)

    def collide_projectiles(self, projectiles: list[Projectile]):
        res = []
        for proj in projectiles:
            if self.rect.colliderect(proj.rect):
                res.append(proj)
        return res

    def check_projectile_hit(self, projectile: Projectile):
        collide = self.mask.overlap(projectile.explosion_mask, projectile.explosion_dist)
        return collide
