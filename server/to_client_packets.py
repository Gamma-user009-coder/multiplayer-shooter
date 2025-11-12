from Projectile import Projectile
from typing import Optional
from Player import Player
from enum import Enum

class ToClientPackets(Enum):
    ERROR_MESSAGE = 0
    PLAYER_STATUS = 1
    JOIN_GAME_RESPONSE = 2
    END_ROUND_PACKET = 3
    END_GAME_PACKET = 4
    JOIN_ROOM_RESPONSE = 5
    ASSIGN_ID_PACKET = 6

# packet id: 0
class ErrorMessage:
    error_id = int

# packet id: 1
class PlayerStatus:
    players = dict[int, Player]
    projectiles = list[Projectile]
    def __init__(self, players, projectiles):
        self.players = players
        self.projectiles = projectiles

    def to_dict(self):
        dct = {}
        for player in self.players:
            dct[player.id] = player.to_tuple()
        return dct


# packet id: 2
class JoinGameResponse:
    id = int
    ...

# packet id: 3
class EndRound:
    won = bool

# packet id: 4
class EndGame:
    won = bool

# packet id: 5
class JoinRoomResponse:
    room_id = int
    ...

# packet id: 6
class AssignId:
    player_id = int
    def __init__(self, player_id):
        self.player_id = player_id

    def to_dict(self):
        return {'player_id': self.player_id}
    ...