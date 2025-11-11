class Player:
    hp = int
    pos = tuple[int, int]
    def __init__(self, hp: int, pos: tuple[int, int]):
        self.hp = hp
        self.pos = pos

    def to_tuple(self):
        return self.hp, self.pos
