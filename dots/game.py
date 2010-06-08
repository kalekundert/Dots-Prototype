from managers import *

class Game:
    def __init__(self, world, messenger):
        self.world = world
        self.messenger = messenger

        self.managers = []

    def setup(self):
        red = self.world.tribes[0]
        blue = self.world.tribes[1]

        self.gui_manager = gui.GUI(self, self.world, self.messenger, red)
        self.managers.append(self.gui_manager)

        self.ai_manager = ai.AI(self, self.world, self.messenger, blue)
        self.managers.append(self.ai_manager)

        self.collision_manager = collisions.Collisions(self, self.world, self.messenger)
        self.managers.append(self.collision_manager)

        self.combat_manager = combat.Combat(self, self.world, self.messenger)
        self.managers.append(self.combat_manager)

        self.growth_manager = growth.Growth(self, self.world, self.messenger)
        self.managers.append(self.growth_manager)

        self.victory_manager = victory.Victory(self, self.world, self.messenger)
        self.managers.append(self.victory_manager)

        for manager in self.managers:
            manager.setup()

    def update (self, time):
        for manager in self.managers:
            manager.update(time)
