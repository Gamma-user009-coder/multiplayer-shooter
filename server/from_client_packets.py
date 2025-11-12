from Projectile import Projectile
from typing import Optional
from enum import Enum

class FromClientPackets(Enum):
    ERROR_MESSAGE = 0
    JOIN_GAME_REQUEST = 1
    PLAYER_STATUS = 2
    FIRST_CONNECTION_REQUEST = 3
    JOIN_ROOM_REQUEST = 4


# packet id: 0
class ErrorMessage:
    player_id = int
    error_id = int
    message = str

    def __init__(self, player_id, error_id, message):
        self.player_id = player_id
        self.error_id = error_id
        self.message = message

# packet id: 2
class PlayerStatus:
    player_id = int
    pos = tuple[int, int]
    projectile = Optional[Projectile]

    def __init__(self, player_id, pos, projectile):
        self.player_id = player_id
        self.pos = pos
        self.projectile = projectile

# packet id: 1
class JoinGameRequest:
    player_id = int
    username = str
    def __init__(self, player_id, username):
        self.player_id = player_id
        self.username = username
    ...

# packet id: 3
class FirstConnectionRequest:
    username = str
    def __init__(self, username):
        self.username = username

    # this isn't needed on the server because the server doesn't serialize
    # a packet from the client, it's left here for now for test1.py
    def to_dict(self):
        return {'id': FromClientPackets.FIRST_CONNECTION_REQUEST.value, 'username': self.username}

# packet id: 4
class JoinRoomRequest:
    player_id = int
    room_id = int
    ...