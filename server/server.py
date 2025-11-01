from Player import Player
from Projectile import Projectile

class Server:

    players: list[Player]
    projectiles: list[Projectile]

    def __init__(self):
        ...

    def tick(self):
        self.get_player_updates()
        self.update_projectiles()
        self.check_collisions()
        self.send_updates_to_clients()

    def get_player_updates(self):
        """Receive the clients' updates about their player status"""
        ...

    def update_projectiles(self):
        """Update the positions of all existing projectiles"""
        ...

    def check_collisions(self):
        """Check if any of the bombs connected to a surface or player, and update their hp values accordingly"""
        ...

    def send_updates_to_clients(self):
        """Send back packets to the clients about the statuses of all players and projectiles"""
        ...
