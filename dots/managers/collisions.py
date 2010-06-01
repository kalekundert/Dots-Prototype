from vector import *
from manager import Manager

class Collisions(Manager):

    def __init__(self, game, world, messenger):
        Manager.__init__(self, game, world, messenger)

    def update(self, time):
        for first in self.world.dots:
            # Make sure each dot is on the map.
            self.keep_on_map(first);

            # Make sure no dots are colliding.  (This is N-squared as is, but
            # I can do better with a smarter map class.)
            for second in self.world.dots:
                self.fix_collision(first, second)

    def keep_on_map(self, dot):
        radius = dot.radius
        x, y = dot.position.get_tuple()

        map = self.world.map

        if x - radius < 0:
            x = radius
        if x + radius > map.size:
            x = map.size - radius

        if y - radius < 0:
            y = radius
        if y + radius > map.size:
            y = map.size - radius

        message = {}
        message["type"] = "reposition"
        message["position"] = Vector(x, y)

        self.send_message (dot, message)

    # Fixing one collision could conceivably create another, but I'm not
    # going to worry about that yet.
    def fix_collision(self, first, second):
        if first is second:
            return

        # Find out if there is a collision
        displacement = first.position - second.position

        radius = first.radius + second.radius
        distance = displacement.get_magnitude()

        if distance > radius:
            return

        # Deal with the collision
        overlap = radius - distance
        correction = (overlap / 2.0) * displacement.get_normal()

        first_message = {}
        first_message["type"] = "reposition"
        first_message["position"] = first.position + correction

        second_message = {}
        second_message["type"] = "reposition"
        second_message["position"] = second.position - correction

        self.send_message(first, first_message)
        self.send_message(second, second_message)

