from vector import *
from manager import Manager

from dots.constants import *

# Rename this to health manager (instead of combat manager) in the final
# version.
class Combat(Manager):

    def __init__(self, game, world, messenger):
        Manager.__init__(self, game, world, messenger)

    def update(self, time):
        maybe_dead = []

        for dot in self.world.dots:
            targets = []

            # Choose targets
            for other in self.world.dots:
                if dot is other:
                    continue
                if dot.tribe is other.tribe:
                    continue

                distance = Vector.get_distance(dot.position, other.position)

                distance -= dot.radius
                distance -= other.radius

                if distance < COMBAT_RANGE:
                    targets.append(other)

            # Assign damage
            try: damage_per_sec = COMBAT_DAMAGE / len(targets)
            except ZeroDivisionError:
                continue

            for target in targets:
                damage = damage_per_sec * time / 1000
                damage_message = self.new_message ("damage", damage=damage)

                self.send_message(target, damage_message)
                maybe_dead.append(target)

        # Get rid of dead dots
        for dot in maybe_dead:
            if dot.health > 0:
                continue

            # It might be nice if this message included a tribe attribute, 
            # because a couple different managers need to know which tribe 
            # the ex-dot belonged to.  It's easy enough to figure this out
            # from the dot itself, but it might be cleaner if the message 
            # just contained the relevant information.
            kill_message = self.new_message ("kill", dot=dot)

            self.send_message(dot.tribe, kill_message)
            self.send_message(self.world, kill_message)

            self.send_message(self.game.gui_manager, kill_message)
            self.send_message(self.game.victory_manager, kill_message)
