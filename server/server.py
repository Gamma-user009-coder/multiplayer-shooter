from json import JSONDecodeError

from Player import Player
from Projectile import Projectile
import socket
import threading
import queue
import json
import client_packets
import server_packets


class Connection:
    ip = str
    port = int

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def to_tuple(self):
        return self.ip, self.port

class Server:

    # list of (Player, socket)
    # socket is ip, port
    server_socket = socket.socket
    incoming_data = queue.Queue[tuple[bytes, Connection]]
    outgoing_data = queue.Queue[tuple[bytes, Connection]]
    connections = dict[int, Connection]
    players = dict[int, Player]
    projectiles: list[Projectile]
    next_connection_id: int

    def __init__(self):
        self.players: dict[int, Player] = {}
        self.projectiles: list[Projectile] = []
        self.incoming_data: queue.Queue[tuple[bytes, Connection]] = queue.Queue()
        self.outgoing_data: queue.Queue[tuple[bytes, Connection]] = queue.Queue()
        self.connections: dict[int, Connection] = {}
        self.next_connection_id = 0


    def start(self):
        """ Initiate the server and start the listening thread and the data sending thread"""
        # AF_INET specifies the address family (IPv4)
        # SOCK_DGRAM specifies the socket type (UDP)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.server_socket.bind(('0.0.0.0', 12345))
        print(f"UDP server listening")
        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.send_data, daemon=True).start()
        self.handle_data()


    def listen(self):
        """ Listen for incoming packets and add them to the incoming data queue. A thread will always run this function. """
        while True:
            data, connection = self.server_socket.recvfrom(2048)
            try:
                if json.loads(data)['id'] == 6:
                    new_player_id = self.next_connection_id
                    self.connections[new_player_id] = Connection(connection[0], connection[1])
                    self.next_connection_id += 1

                    msg = json.dumps(server_packets.AssignId(new_player_id).to_dict()).encode()

                    self.outgoing_data.put((msg, Connection(connection[0], connection[1])))

            except JSONDecodeError:
                # return error to client (maybe returning error to client isn't required, TBD)
                print("Invalid JSON")
                continue

            except KeyError:
                # return error to client (maybe returning error to client isn't required, TBD)
                print("Invalid packet - key error")
                continue

            except TypeError:
                print("Invalid packet - type error")
                continue

            self.incoming_data.put((data, Connection(connection[0], connection[1])))


    def handle_data(self):
        """ Get a packet out of the incoming data queue, parse it then pass it to the handler """
        while True:
            data, connection = self.incoming_data.get()
            try:
                json_dict = json.loads(data.decode())

            except JSONDecodeError:
                print("Invalid JSON")
                # return error to client (maybe returning error to client isn't required, TBD)
                continue

            self.handle_requests(json_dict)


    def handle_requests(self, json_dict):
        """ Get json and pass it to the correct handler """
        print("handling request for json:", json_dict)
        try:
            if json_dict['id'] == 0:
                print("0")
                # TODO: handle error message

            if json_dict['id'] == 1:
                print("1")
                player_id, username = json_dict['player_id'], json_dict['name']
                join_game = client_packets.JoinGameRequest(player_id, username)
                # TODO: handle join request

            elif json_dict['id'] == 2:
                print("2")
                self.handle_player_update(json_dict)

            else:
                print("unknown id")

        except KeyError:
            print("key error while deserializing")

        except TypeError:
            print("type error while deserializing")


    def handle_player_update(self, json_dict):
        """ Handle packet of update of a player's status """
        projectile = None
        player_id = json_dict['player_id']
        if json_dict['bomb'] != 0:
            x, y, angle = json_dict['bomb']
            projectile = Projectile(player_id, (x, y), angle)
        player_status = client_packets.PlayerStatus(player_id, json_dict['cord'], projectile)

        self.players[player_status.player_id].pos = player_status.pos
        if projectile:
            self.projectiles.append(projectile)

        for player in self.players:
            msg = server_packets.PlayerStatus(self.players, self.projectiles).to_dict()
            msg = json.dumps(msg).encode()
            self.outgoing_data.put(())
        # TODO: fully handle player status update

    def send_data(self):
        """ Send packets from the outgoing packets queue to the correct client. A thread will always run this function """
        while True:
            data, connection = self.outgoing_data.get()
            print(data, connection.to_tuple())
            self.server_socket.sendto(data, connection.to_tuple())


    # def tick(self):
    #     self.get_player_updates()
    #     self.update_projectiles()
    #     self.check_collisions()
    #     self.send_updates_to_clients()


def main():
    Server().start()


if __name__ == '__main__':
    main()