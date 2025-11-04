import math

from Level import Level, Box
from Player import Player
from Collision import Collision

class Projectile:

    x0: int  # px
    y0: int  # px
    angle: float  # rads
    v0: float  # px/sec
    v0x: float  # px/sec
    v0y: float  # px/sec
    r: int  # px
    team: int

    t: float  # sec
    x: int  # px
    y: int  # px

    DEFAULT_ANGLE = math.pi / 4  # rads
    DEFAULT_BASE_VELOCITY = 100  # px/sec
    G = 30  # px/sec
    DEFAULT_EXPLOSION_RADIUS = 50  # px

    def __init__(self, x0: int, y0: int, team: int, angle: float = None, v0: float = None, r: int = None):
        self.x0 = x0
        self.y0 = y0
        self.team = team

        if angle is not None:
            self.angle = angle
        else:
            self.angle = self.DEFAULT_ANGLE

        if v0 is not None:
            self.v0 = v0
        else:
            self.v0 = self.DEFAULT_BASE_VELOCITY

        self.v0x = math.cos(self.angle) * self.v0
        self.v0y = math.sin(self.angle) * self.v0

        if r is not None:
            self.r = r
        else:
            self.r = self.DEFAULT_EXPLOSION_RADIUS

        self.t = 0
        self.x = self.x0
        self.y = self.y0

    def update_position(self, dt: float) -> None:
        self.t += dt
        self.x = self.x0 + int(self.t * self.v0x)
        self.y = self.y0 + int(self.t * self.v0y - 0.5 * self.G * self.t * self.t)

    def update_position_check_collisions(self, dt: float, level: Level, players: list[Player] = []) -> Collision:
        """Returns False and updates self coordinates if no collision; else returns collision coordinates (x,y)"""
        self.t += dt
        nx = self.x0 + int(self.t * self.v0x)
        ny = self.y0 + int(self.t * self.v0y - 0.5 * self.G * self.t * self.t)
        collision = level.check_collision_line(self.x, self.y, nx, ny)
        if collision:
            return collision
        for player in players:
            collision = self.check_player_collision_line(player, nx, ny)
            if collision:
                return collision

        self.t += dt
        self.x = nx
        self.y = ny
        return Collision.false()

    def check_player_hit(self, player: Player, level: Level) -> bool:
        within_range = math.dist((self.x, self.y), (player.x, player.y)) < self.r
        within_line_of_sight = level.check_collision_line(self.x, self.y, player.x, player.y)
        return within_range and within_line_of_sight

    def check_out_of_screen(self):
        return (self.x < Level.MIN_X - Level.SCREEN_EDGE_BUFFER
                or self.x > Level.MAX_X + Level.SCREEN_EDGE_BUFFER
                or self.y < Level.MIN_Y - Level.SCREEN_EDGE_BUFFER
                or self.y > Level.MAX_Y + Level.SCREEN_EDGE_BUFFER)

    def check_level_collision(self, level: Level):
        return level.check_collision_point(self.x, self.y)

    def check_player_collision(self, player: Player):
        player_box = Box.from_player(player)
        return player_box.check_collision_point(self.x, self.y)

    def check_player_collision_line(self, player: Player, x2: int, y2: int):
        player_box = Box.from_player(player)
        return player_box.check_collision_line(self.x, self.y, x2, y2)
