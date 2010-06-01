from dots.messaging import Sender

class Manager:

    # Subclasses will include:
    #  -Player
    #  -Collisions
    #  -Combat
    #  -Network
    #   etc.

    def __init__(self, game, world, messenger):
        self.world = world
        self.game = game

        self.sender = Sender (messenger);
        self.receiver = self.sender

    def send_message(self, token, message):
        sender = self.sender
        receiver = token.receiver

        sender.send_message(receiver, message)

    def new_message(self, type, **values):
        values["type"] = type
        return values

    def setup(self): pass

    def update(self, time): pass
