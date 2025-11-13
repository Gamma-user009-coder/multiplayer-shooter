class Player:

    x: int
    y: int
    hp: int
    team: int
    width: int = 50
    height: int = 50
    username: str

    MIN_HP = 0
    MAX_HP = 100
    BOMB_DAMAGE = 50

    def __init__(self, team: int, username:str = 'john doe'):
        self.x = 0
        self.y = 0
        self.hp = self.MAX_HP
        self.team = team
        self.username = username

    def make_hit(self):
        self.hp -= self.BOMB_DAMAGE
        self.check_death()

    def check_death(self):
        if self.hp < self.MIN_HP:
            ...

    def same_team(self, team):
        return self.team == team

    def to_tuple(self):
        return self.hp, (self.x, self.y)
