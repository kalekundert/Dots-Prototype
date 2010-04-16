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
        self.sender = Sender (messenger);

        self.timer = 0;

    def get_sender(self):
        return self.sender

    def update(self, time):
        self.timer += time;

        if self.timer < 1000:
            return

        for token in self.world:
            sender = self.get_sender()
            receiver = token.get_receiver()
            sender.send_message(receiver, "hello")

        self.timer = 0



