import messaging

from tokens import *
from vector import *

from random import uniform

class World:

    def __init__(self, messenger):
        self.tokens = []
        self.messenger = messenger

    def __iter__(self):
        for token in self.tokens:
            yield token

    def setup(self):
        for i in range(25):
            self.make_token();

    def update(self, time):
        for token in self:
            token.update(time)

    def make_token(self):
        new_position = Vector(uniform(0, 500), uniform(0, 500))
        new_receiver = messaging.Receiver(self.messenger)
        new_token = token.Token(new_receiver, new_position)

        self.tokens.append(new_token)
        return new_token
