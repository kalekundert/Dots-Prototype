from managers import *

class Game:
    def __init__(self, world, messenger):
        self.world = world
        self.messenger = messenger

    def setup(self):
        self.manager = manager.Manager(self.world, self.messenger)

    def update (self, time):
        self.manager.update(time)
