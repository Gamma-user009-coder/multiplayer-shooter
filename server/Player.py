class Player:

    x: int
    y: int
    hp: int
    team: int


    MIN_HP = 0
    MAX_HP = 100
    BOMB_DAMAGE = 50

    def __init__(self, team: int):
        self.x = 0
        self.y = 0
        self.hp = self.MAX_HP
        self.team = team

    def make_hit(self):
        self.hp -= self.BOMB_DAMAGE
        self.check_death()

    def check_death(self):
        if self.hp < self.MIN_HP:
            ...

    def same_team(self, team):
        return self.team == team