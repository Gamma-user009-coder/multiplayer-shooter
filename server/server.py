from Player import Player
from Projectile import Projectile
from Level import Level

from json import JSONDecodeError

import time
import socket
import threading
import queue
import json
import client_packets
from client_packets import ClientPackets
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

    players: dict[int, Player]
    projectiles: list[Projectile]
    level: Level

    last_update: float  # sec
    
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
        
        self.last_update = time.perf_counter()

    def tick(self):
        self.get_player_updates()
        self.update_projectiles_check_collisions()
        self.send_updates_to_clients()

    def get_player_updates(self):
        """Receive the clients' updates about their player status"""
        ...
    # obsolete
    def update_projectiles(self):
        """Update the positions of all existing projectiles"""

        dt = time.perf_counter() - self.last_update

        new_projectiles = []
        update_projectiles = False
        for projectile in self.projectiles:
            projectile.update_position(dt)   # update_position_check_collisions()
            if projectile.check_out_of_screen():
                update_projectiles = True
            else:
                new_projectiles.append(projectile)

        if update_projectiles:
            self.projectiles = new_projectiles

        self.last_update = time.perf_counter()

    # obsolete
    def check_collisions(self):
        """Check if any of the bombs connected to a surface or player, and update their hp values accordingly"""

        new_projectiles = []
        update_projectiles = False

        for projectile in self.projectiles:
            # Check for a collision with the level
            collision = projectile.check_level_collision(self.level)
            if not collision:
                # Check for a collision with an enemy player
                for player in self.players:
                    if player.same_team(projectile.team):
                        collision = collision or projectile.check_player_collision(player)

            if collision:
                # Check if an enemy player is hit
                for player in self.players:
                    if player.same_team(projectile.team) and projectile.check_player_hit(player, self.level):
                        player.make_hit()

            if collision:
                update_projectiles = True
            else:
                new_projectiles.append(projectile)

        # Don't change projectiles if none of them need to be removed
        if update_projectiles:
            self.projectiles = new_projectiles


    def update_projectiles_check_collisions(self):

        new_projectiles = []
        update_projectiles = False

        dt = time.perf_counter() - self.last_update
        if dt < 0.0001:
            return
        self.last_update = time.perf_counter()

        # For each projectile in the air,
        for projectile in self.projectiles:
            # Check if it collided with something; if not, update its position
            collision = projectile.update_position_check_collisions(dt, self.level, self.players)

            # If it collided or moved out of screen, remove it
            if collision or projectile.check_out_of_screen():
                update_projectiles = True
            else:
                new_projectiles.append(projectile)

            # If there's a collision, check if any enemy players were hit
            if collision:
                for player in self.players.values():
                    if (not player.same_team(projectile.team)) and projectile.check_player_hit(player, self.level):
                        player.make_hit()

        # No need to update the list if we don't need to remove any projectiles
        if update_projectiles:
            self.projectiles = new_projectiles


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
        """ Listen for incoming packets and add them to the incoming data queue.
            In case of a new connection the server will assign them an id and respond to the client.
            A thread will always run this function. """
        while True:
            data, connection = self.server_socket.recvfrom(2048)
            try:
                if json.loads(data)['id'] == ClientPackets.FIRST_CONNECTION_REQUEST.value:
                    print("new client connected")
                    new_player_id = self.next_connection_id
                    self.connections[new_player_id] = Connection(connection[0], connection[1])
                    self.next_connection_id += 1

                    msg = json.dumps(server_packets.AssignId(new_player_id).to_dict()).encode()

                    self.outgoing_data.put((msg, Connection(connection[0], connection[1])))
                    continue

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
            if json_dict['id'] == ClientPackets.ERROR_MESSAGE.value:
                print("handling error message packet")
                # TODO: handle error message

            if json_dict['id'] == ClientPackets.JOIN_GAME_REQUEST.value:
                print("handling join game request packet")
                player_id, username = json_dict['player_id'], json_dict['name']
                join_game = client_packets.JoinGameRequest(player_id, username)
                # TODO: handle join request

            elif json_dict['id'] == ClientPackets.PLAYER_STATUS.value:
                print("handle player status update packet")
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
            print(data, connection.to_tuple(), sep='\n')
            self.server_socket.sendto(data, connection.to_tuple())

    



def main():
    Server().start()


if __name__ == '__main__':
    main()