from managers import *

class Game:
    def __init__(self, world, messenger):
        self.world = world
        self.messenger = messenger

        self.managers = []

    def setup(self):
        tribe = self.world.tribes[0]
        gui_manager = gui.GUI(self.world, self.messenger, tribe)
        self.managers.append(gui_manager)

        for manager in self.managers:
            manager.setup()

    def update (self, time):
        for manager in self.managers:
            manager.update(time)
