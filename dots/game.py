from managers import *

class Game:
    def __init__(self, world, messenger):
        self.world = world
        self.messenger = messenger

        self.managers = []

    def setup(self):
        tribe = self.world.tribes[0]

        self.gui_manager = gui.GUI(self, self.world, self.messenger, tribe)
        self.managers.append(self.gui_manager)

        self.collision_manager = collisions.Collisions(self, self.world, self.messenger)
        self.managers.append(self.collision_manager)

        self.combat_manager = combat.Combat(self, self.world, self.messenger)
        self.managers.append(self.combat_manager)

        for manager in self.managers:
            manager.setup()

    def update (self, time):
        for manager in self.managers:
            manager.update(time)
