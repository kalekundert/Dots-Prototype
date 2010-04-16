from tokens import *

class World:

    def __init__(self, messenger):
        self.tokens = []
        self.messenger = messenger

    def __iter__(self):
        for token in self.tokens:
            yield token

    def update (self, time):
        for token in self:
            token.update(time)

    def make_token(self):
        new_token = token.Token(self.messenger)
        self.tokens.append(new_token)

        return new_token
