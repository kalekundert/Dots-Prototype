from dots.messaging import Sender

class Manager:

    # Subclasses will include:
    #  -Player
    #  -Collisions
    #  -Combat
    #  -Network
    #   etc.

    def __init__(self, world, messenger):
        self.world = world
        self.timer = 0;

        self.sender = Sender (messenger);
        self.receiver = self.sender

    def send_message(self, token, message):
        sender = self.sender
        receiver = token.receiver

        sender.send_message(receiver, message)

    def setup():
        pass

    def update(self, time):
        self.timer += time;

        if self.timer < 1000:
            return

        for token in self.world:
            self.send_message(token, "hello")

        self.timer = 0



