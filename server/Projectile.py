class Projectile:

    # id of player who threw the projectile
    team_id = int
    starting_pos = tuple[int, int]
    angle = int
    def __init__(self, team_id, starting_pos: tuple[int, int], angle: int):
        self.team_id = team_id
        self.starting_pos = starting_pos
        self.angle = angle