import math

class Projectile:

    x0: int  # px
    y0: int  # px
    angle: float  # rads
    v0: float  # px/sec
    v0x: float  # px/sec
    v0y: float  # px/sec
    r: int  # px

    t: float  # sec
    x: int  # px
    y: int  # px

    DEFAULT_ANGLE = math.pi / 4  # rads
    DEFAULT_BASE_VELOCITY = 100  # px/sec
    G = 10  # px/sec

    def __init__(self, x0: int, y0: int, angle: float = None, v0: float = None):
        self.x0 = x0
        self.y0 = y0
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

        self.t = 0
        self.x = self.x0
        self.y = self.y0

    def update_position(self, dt: float) -> None:
        self.t += dt
        self.x = self.x0 + int(self.t * self.v0x)
        self.y = self.y0 + int(self.t * self.v0y - 0.5 * self.G * self.t * self.t)

    def check_player_collision(self, x: int, y: int) -> bool:
        return math.dist((self.x, self.y), (x, y)) < self.r