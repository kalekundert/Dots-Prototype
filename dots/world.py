import messaging

from tokens import *
from vector import *

from random import uniform

class World:

    def __init__(self, messenger):
        self.messenger = messenger

        self.tribes = []
        self.tokens = []

    def __iter__(self):
        for token in self.tokens:
            yield token

    def setup(self):
        tribe = self.make_tribe();
        for i in range(25):
            self.make_token(tribe);

    def update(self, time):
        for token in self:
            token.update(time)

    def make_tribe(self):
        new_receiver = messaging.Receiver(self.messenger)
        new_tribe = tribe.Tribe(new_receiver)

        self.tribes.append(new_tribe)
        return new_tribe


    def make_token(self, tribe):
        new_position = Vector(uniform(0, 500), uniform(0, 500))
        new_receiver = messaging.Receiver(self.messenger)
        new_dot = dot.Dot(new_receiver, tribe, new_position)

        self.tokens.append(new_dot)
        return new_dot
