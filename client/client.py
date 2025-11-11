import json
import socket

from Packets import *
from client_communications import *
from error_types import *
from client_communications import *
PORT = 12345
IP = "127.0.0.1"

STARTING_POS = (0,0)
class Game_Start:
    def __init__(self, connection : Connection):
        self.socket = connection
        self.player_id = 0
        self.name = ""
        self.player_state = 0   # holds current player state 0 -> menu, 1->waiting room, 2->ingame

    def run_game(self):
        try:
            name = ""
            self.socket.send_name(name) # sends chosen name to server
            response = self.socket.get_response()
            score = [0,0]     # contains score [0]->current player [1]->enemy player
            names = [name, ""]     # contains player names [0]->current player [1]->enemy player
            while response != 0:
                player_exit = 0
                id = response["id"] # server response
                if id == 0:     # error on server side
                    raise ServerError()
                elif id == 6:
                    self.player_id = response["player_id"]  # assigns id to player
                    pass
                elif id == 2: # when joining game
                    if self.player_state != 1:
                        raise IllegalAction()
                    self.player_state = 2
                    score = [0,0] # resets score
                    names[1] = response["enemy_name"] # gets enemy name to render on health bar
                    x, y = STARTING_POS

                elif id == 1:  # handles player repr every tick
                    player_hp, enemy_hp, enemy_pos, projectiles = self.socket.load_tick_stats(response, self.player_id)
                    # Rendering : 2 health bars according to hp  render enemy on screen with player name, and list of projectiles on screen
                    pass
                elif id == 3: # when a single round ends
                    is_win = response['won']
                    score[not is_win] += 1
                    x, y = STARTING_POS
                    pass
                elif id == 4: # when a single game ends
                    score = [0,0]
                    if self.player_state != 2:
                        raise IllegalAction()
                    self.player_state = 0
                    pass
                elif player_exit:
                    self.socket.send_command(ExitPacket(self.player_id).__repr__())      # in case player exits game
                    break
                else:
                    raise InvalidResponseID()

        except Exception as e:          # sends appropriate exception type to server
            self.socket.send_exception(e)
if __name__ == '__main__':


    client_connection = Connection(IP, PORT)
    Game_Start(client_connection).run_game()