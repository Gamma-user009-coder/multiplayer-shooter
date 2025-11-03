

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
        """Returns False if no collision; else the collision coordinates (x,y)"""
        c0, c1, c2, c3 = self._get_corners()
        for collision in [
            self._check_collision_line_horizontal(x1, y1, x2, y2, c0[0], c1[0], c0[1]),
            self._check_collision_line_horizontal(x1, y1, x2, y2, c3[0], c2[0], c2[1]),
            self._check_collision_line_vertical(x1, y1, x2, y2, c1[1], c2[1], c1[0]),
            self._check_collision_line_vertical(x1, y1, x2, y2, c0[1], c3[1], c0[0])
        ]:
            if collision:
                return collision
        return False


    def _get_corners(self):
        return [(self.x1, self.y1), (self.x2, self.y1), (self.x2, self.y2), (self.x1, self.y2)]
        # 3 2
        # 0 1

    @staticmethod
    def _check_collision_line_line(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int):
        t = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        r = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        if (0 <= t <= 1) and (0 <= r <= 1):
            return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        else:
            return False

    @staticmethod
    def _check_collision_line_horizontal(x1: int, y1: int, x2: int, y2: int, x3: int, x4: int, y3: int):
        """Returns False if no collision, otherwise the collision coordinates (x,y)"""
        if y1 > y2:
            y1, y2 = y2, y1
            x1, x2 = x2, x1
        if (y3 < y1) or (y3 > y2):
            return False
        t = (y3 - y1) / (y2 - y1)
        tx = x1 + t * (x2 - x1)
        if (x3 <= tx <= x4) or (x4 <= tx <= x3):
            return (tx, y3)
        return False

    @staticmethod
    def _check_collision_line_vertical(x1: int, y1: int, x2: int, y2: int, y3: int, y4: int, x3: int):
        """Returns False if no collision, otherwise the collision coordinates (x,y)"""
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        if (x3 < x1) or (x3 > x2):
            return False
        t = (x3 - x1) / (x2 - x1)
        ty = y1 + t * (y2 - y1)
        if (y3 <= ty <= y4) or (y4 <= ty <= y3):
            return (x3, ty)
        return False


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
        """Returns False if no collision; else the collision coordinates (x,y)"""
        for box in self.boxes:
            collision = box.check_collision_line(x1, y1, x2, y2)
            if collision:
                return collision
        return False

    def add_box(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.boxes.append(Box(x1, y1, x2, y2))
