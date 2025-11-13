from enum import Enum
from typing import Optional


class Projectile:
    # id of player who threw the projectile
    team_id = int
    starting_pos = tuple[int, int]
    angle = int

    def __init__(self, team_id, starting_pos: tuple[int, int], angle: int):
        self.team_id = team_id
        self.starting_pos = starting_pos
        self.angle = angle


class PlayerPack:
    hp = int
    pos = tuple[int, int]

    def __init__(self, hp: int, pos: tuple[int, int]):
        self.hp = hp
        self.pos = pos

    def to_tuple(self):
        return self.hp, self.pos


class ServerPackets(Enum):
    ERROR_MESSAGE = 0
    GAME_STATUS = 1
    JOIN_GAME_RESPONSE = 2
    END_ROUND_PACKET = 3
    END_GAME_PACKET = 4
    JOIN_ROOM_RESPONSE = 5
    ASSIGN_ID_PACKET = 6


# packet id: 1
class GameStatus:
    players = dict[int, PlayerPack]
    projectiles = list[Projectile]

    def __init__(self, players, projectiles):
        self.players = players
        self.projectiles = projectiles


# packet id: 6
class AssignId:
    player_id = int

    def __init__(self, player_id):
        self.player_id = player_id


class ClientPackets(Enum):
    ERROR_MESSAGE = 0
    JOIN_GAME_REQUEST = 1
    PLAYER_STATUS = 2
    FIRST_CONNECTION_REQUEST = 3
    JOIN_ROOM_REQUEST = 4


# packet id: 2
class PlayerStatus:
    player_id = int
    pos = tuple[int, int]
    projectile = Optional[Projectile]

    def __init__(self, player_id, pos, projectile):
        self.player_id = player_id
        self.pos = pos
        self.projectile = projectile

    def to_dict(self):
        return {"id": ClientPackets.PLAYER_STATUS.value, "player_id": self.player_id, "pos": self.pos, "projectile": self.projectile}


# packet id: 3
class FirstConnectionRequest:
    username = str

    def __init__(self, username):
        self.username = username

    def to_dict(self):
        return {'id': ClientPackets.FIRST_CONNECTION_REQUEST.value, 'username': self.username}

#
# class InvalidResponseID(Exception):
#     def __init__(self, message="Invalid server response provided"):
#         super().__init__(message)
#         self.value = 0
#         self.message = message
#
#     def __str__(self) -> str:
#         return self.message
#
#
# class ServerError(Exception):
#     def __init__(self, message="Server misshandled input"):
#         super().__init__(message)
#         self.value = 1
#         self.message = message
#
#     def __str__(self) -> str:
#         return self.message
#
#
# class IllegalAction(Exception):
#     def __init__(self, message="Illegal action on client side"):
#         super().__init__(message)
#         self.value = 2
#         self.message = message
#
#     def __str__(self) -> str:
#         return self.message
