import messaging

from tokens import *
from vector import *

from random import uniform

class World:
    def __init__(self, messenger):
        self.messenger = messenger
        self.receiver = messaging.Receiver(messenger)

        self.map = None

        self.dots = []
        self.tribes = []

        self.tokens = []

    def __iter__(self):
        for token in self.tokens:
            yield token

    def setup(self):
        map = self.make_map()

        red = self.make_tribe((255, 0, 0), 250, 250)
        blue = self.make_tribe((0, 0, 255), 750, 750)

        for i in range(15):
            self.make_token(red)
            self.make_token(blue)

    def update(self, time):
        messages = self.receiver.dump_messages()
        for message in messages:
            if message["type"] == "kill":
                dot = message["dot"]
                if dot in self.dots:
                    self.dots.remove(dot)
                    self.tokens.remove(dot)
            else:
                raise ValueError("Bad message type: '%(type)s'" % message)

        for token in self:
            token.update(time)

    def make_map(self):
        new_receiver = messaging.Receiver(self.messenger)
        new_map = map.Map(new_receiver, 2000)

        self.map = new_map
        self.tokens.append(new_map)

        return new_map

    def make_tribe(self, color, x, y):
        new_receiver = messaging.Receiver(self.messenger)
        new_tribe = tribe.Tribe(new_receiver, color, x, y)

        self.tribes.append(new_tribe)
        self.tokens.append(new_tribe)

        return new_tribe

    def make_token(self, tribe):
        new_position = Vector(uniform(-250, 250), uniform(-250, 250))
        new_position += tribe.position

        new_receiver = messaging.Receiver(self.messenger)
        new_dot = dot.Dot(new_receiver, tribe, new_position)

        new_dot.create()

        self.dots.append(new_dot)
        self.tokens.append(new_dot)

        return new_dot
