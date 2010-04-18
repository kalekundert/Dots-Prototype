import messaging

from tokens import *
from vector import *

from random import uniform

class World:

    def __init__(self, messenger):
        self.messenger = messenger

        self.map = None

        self.dots = []
        self.tribes = []

        self.tokens = []

    def __iter__(self):
        for token in self.tokens:
            yield token

    def setup(self):
        map = self.make_map()
        tribe = self.make_tribe()

        for i in range(15):
            self.make_token(tribe)

    def update(self, time):
        for token in self:
            token.update(time)

    def make_map(self):
        new_receiver = messaging.Receiver(self.messenger)
        new_map = map.Map(new_receiver, 2000)

        self.map = new_map
        self.tokens.append(new_map)

        return new_map

    def make_tribe(self):
        new_receiver = messaging.Receiver(self.messenger)
        new_tribe = tribe.Tribe(new_receiver)

        self.tribes.append(new_tribe)
        self.tokens.append(new_tribe)

        return new_tribe


    def make_token(self, tribe):
        new_position = Vector(uniform(0, 500), uniform(0, 500))
        new_receiver = messaging.Receiver(self.messenger)
        new_dot = dot.Dot(new_receiver, tribe, new_position)

        new_dot.create()

        self.dots.append(new_dot)
        self.tokens.append(new_dot)

        return new_dot
