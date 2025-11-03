

class Box:

    x1: int
    y1: int
    x2: int
    y2: int

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        """x1 < x2; y1 < y2"""
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def check_collision_point(self, x: int, y: int) -> bool:
        return (self.x1 <= x <= self.x2) and (self.y1 <= y <= self.y2)

    def check_collision_line(self, x1: int, y1: int, x2: int, y2: int):
        ...

    def _get_corners(self):
        ...
        # return [(self.x1, self.y1), (self.x2, self.y1), (self.)]

    @staticmethod
    def _check_collision_line_line(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int):
        t = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        r = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        return (0 <= t <= 1) and (0 <= r <= 1)

    @staticmethod
    def _check_collision_line_horizontal(x1: int, y1: int, x2: int, y2: int):
        ...


class Level:

    boxes: list[Box]

    MIN_X = 0
    MIN_Y = 0
    MAX_X = 1920
    MAX_Y = 1080
    SCREEN_EDGE_BUFFER = 50

    def __init__(self, boxes: list[Box]):
        self.boxes = []
        for box in boxes:
            self.boxes.append(box)

    def check_collision_point(self, x: int, y: int) -> bool:
        """Check if a point collides with the level"""
        for box in self.boxes:
            if box.check_collision_point(x, y):
                return True
        return False

    def check_collision_line(self, x1: int, y1: int, x2: int, y2: int):
        ...

    def add_box(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.boxes.append(Box(x1, y1, x2, y2))
