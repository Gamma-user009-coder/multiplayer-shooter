
class Client_Name:
    def __init__(self, player_id: int, name : str):
        self.name = name
        self.player_id = player_id
    def __repr__(self) -> dict:
        return {
            "id" : 1,
            "player_id" : self.player_id,
            "name" : self.name,
        }

class GameRoom_Packet:
    def __init__(self, player_id : int ,mode : int ):
        self.mode = mode
        self.player_id = player_id
    def __repr__(self) -> dict:
        return {
            "id": 2,
            "player_id": self.player_id,
            "mode": self.mode # mode 1 for enter waiting room else 0
        }

class Bomb_Repr:
    def __init__(self, flag : bool, x: int, y: int, angle : int):
        self.flag = flag
        self.cord = (x, y)
        self.angle = angle


class Player_Packet:
    def __init__(self, player_id : int, x : int, y : int, bomb : Bomb_Repr):
        self.player_id = player_id
        self.cord = (x, y)
        self.bomb = bomb
    def __repr__(self) ->dict:
        return { "id" : 3,
                 "player_id": self.player_id,
                 "cord" : self.cord,
                 "bomb" : self.bomb}

class ExitPacket:
    def __init__(self, player_id : int):
        self.player_id = player_id
    def __repr__(self) ->dict:
        return {
            "id" : 4,
            "player_id": self.player_id,
        }


class ErrorPacket:
    def __init__(self, player_id : int, error : int):
        self.player_id = player_id
        self.error = error
    def __repr__(self) ->dict:
        return {
            "id" : 0,
            "player_id": self.player_id,
            "error_id": self.error
        }
