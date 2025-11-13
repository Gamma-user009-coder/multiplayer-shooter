from .communication import *
import socket
import json
from .protocol import *


class Client:
    def __init__(self, client_ip: str, client_port: int, server_ip: str, server_port: int, name: str):
        self.connection = Connection(client_ip, client_port, server_ip, server_port)
        self.player_id = None
        self.username = name


    def connect_to_server(self):
        data = FirstConnectionRequest(self.username).to_dict()
        self.connection.send(data)

    def wait_for_id(self):
        while True:
            packets = self.connection.get_packets()
            for packet in packets:
                try:
                    data, address = packet
                    if data["id"] == ServerPackets.ASSIGN_ID_PACKET.value:
                        self.player_id = packet["player_id"]
                        break
                except KeyError:
                    pass

    def send_status_to_server(self, player_x, player_y, projectile_x=0, projectile_y=0):
        player = PlayerStatus(self.player_id, (player_x,player_y), None)
        if projectile_x and projectile_y:
            bomb = Projectile(self.player_id, (projectile_x, projectile_y), 0)
            player.projectile = bomb
        self.connection.send(player.to_dict())



