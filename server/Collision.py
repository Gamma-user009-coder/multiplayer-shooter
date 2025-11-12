class Collision:
    collided: bool
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.collided = True
        self.x = x
        self.y = y

    def __bool__(self):
        return self.collided

    @classmethod
    def false(cls):
        col = cls(0,0)
        col.collided = False
        return col
