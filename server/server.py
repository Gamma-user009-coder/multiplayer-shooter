import socket
import time

from Player import Player
from Projectile import Projectile
from Level import Level


class Server:

    players: list[Player]
    projectiles: list[Projectile]
    level: Level

    last_update: float  # sec

    def __init__(self):
        self.last_update = time.perf_counter()

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

        dt = time.perf_counter() - self.last_update

        new_projectiles = []
        update_projectiles = False
        for projectile in self.projectiles:
            projectile.update_position(dt)
            if projectile.check_out_of_screen():
                update_projectiles = True
            else:
                new_projectiles.append(projectile)

        if update_projectiles:
            self.projectiles = new_projectiles

        self.last_update = time.perf_counter()

    def check_collisions(self):
        """Check if any of the bombs connected to a surface or player, and update their hp values accordingly"""

        new_projectiles = []
        update_projectiles = False
        for projectile in self.projectiles:
            px, py = projectile.x, projectile.y

            # If it collides with the level
            if self.level.check_collision_point(px, py):
                update_projectiles = True

                # If it collides with an enemy player
                for player in self.players:
                    if (projectile.check_player_hit(player.x, player.y, self.level)
                            and player.same_team(projectile.team)):
                        player.make_hit()

            else:
                new_projectiles.append(projectile)

        # Don't change projectiles if none of them need to be removed
        if update_projectiles:
            self.projectiles = new_projectiles


    def send_updates_to_clients(self):
        """Send back packets to the clients about the statuses of all players and projectiles"""
        ...
