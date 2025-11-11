import socket
import time

from Player import Player
from Projectile import Projectile
from Level import Level


class Server:

    players: dict[int, Player]
    projectiles: list[Projectile]
    level: Level

    last_update: float  # sec

    def __init__(self):
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

    def send_updates_to_clients(self):
        """Send back packets to the clients about the statuses of all players and projectiles"""
        ...
