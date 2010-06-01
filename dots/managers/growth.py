from vector import *
from manager import Manager

from dots.constants import *

class Growth(Manager):

    def __init__(self, game, world, messenger):
        Manager.__init__(self, game, world, messenger)

    def update(self, time):
        for dot in self.world.dots:

            crowding_dots = 0

            for other in self.world.dots:
                if dot is other: continue

                distance = Vector.get_distance(dot.position, other.position)

                distance -= dot.radius
                distance -= dot.radius

                if distance < GROWTH_RANGE:
                    crowding_dots += 1

            rate = 1 / (crowding_dots + 1)
            growth = dot.growth + rate * (time / 1000)


            if growth > GROWTH_RATE:
                restart_message = self.new_message("growth", growth=0)
                create_message = self.new_message("create", dot=dot)

                self.send_message(dot, restart_message)
                self.send_message(self.world, create_message)

            else:
                growth_message = self.new_message("growth", growth=growth)
                self.send_message(dot, growth_message)


