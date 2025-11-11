from Packets import *
from error_types import *
import socket
import json
class Projectile:     # placeholder
    pass
class Connection:
    def __init__(self, ip : str, port : int):
        self.ip = ip
        self.port = port
        self.player_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.player_socket.connect((ip, port))                      # opens UDP connection on PORT

    def send_command(self, command: dict) -> None:
        self.player_socket.send(json.dumps(command).encode())

    def get_response(self) -> dict:
        response = self.player_socket.recv(1024)
        return json.loads(response.decode())

    def load_tick_stats(self, response: dict, player_id : int) -> [int, int, tuple[int, int], list[Projectile]]:
        try:
            return (response['player_hp'], response['enemy_hp'], response['enemy_pos'], response['projectiles'])
        except Exception as e:  ## error handling server status update
            self.send_command(ErrorPacket(player_id, 0).__repr__())  # illegal response error error_id->0

    def send_exception(self, player_id : int, e: Exception) -> None:  # sends appropriate exception error to server
        try:
            self.send_command(ErrorPacket(player_id, e.value).__repr__())
        except Exception:
            self.send_command(ErrorPacket(player_id, -1).__repr__())  # different exception
        print(e)

    def send_name(self, player_id : int, name: str) -> None:
        # sends client name to server
        self.send_command(Client_Name(player_id, name).__repr__())

    def send_player(self, player_id : int,  x: int, y: int, bomb: Bomb_Repr) -> None:
        self.send_command(Player_Packet(player_id, x, y, bomb).__repr__())

    def join_waiting_room(self, player_id : int, player_state : int) -> int:
        self.send_command(GameRoom_Packet(player_id, player_state).__repr__())
        response = self.get_response()
        try:
            if response['id'] == 5:
                return response['room_id']
            else:
                raise ServerError()
        except ServerError as e:  # invalid server response
            self.send_exception(e)
        return 0

    def leave_waiting_room(self, player_state : int , player_id : int) -> None:
        try:
            if player_state != 1:
                raise IllegalAction()
            self.send_command(GameRoom_Packet(player_id, player_state).__repr__())
        except IllegalAction as e:
            self.send_exception(player_id, e)  # leaving when not in waiting room

    def exit_game(self, player_id : int) -> None:
        self.send_command(ExitPacket(player_id).__repr__())
