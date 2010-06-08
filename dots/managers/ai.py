from debug import *
from vector import *

from manager import Manager

class AI(Manager):
    def __init__(self, game, world, messenger, tribe):
        Manager.__init__(self, game, world, messenger)

        self.tribe = tribe

    def setup(self):
        for dot in self.tribe:
            message = self.new_message("wander")
            self.send_message(dot, message)

    # This function will contain AI code at some point.
    def update(self, time):
        messages = self.receiver.dump_messages()
        for message in messages:

            if message["type"] == "create":
                dot = message["dot"]
                if dot.tribe is self.tribe:
                    message = self.new_message("wander")
                    self.send_message(dot, message)
                    debug("Sent wander message")

            else:
                raise ValueError ("Unrecognized message type '%s'." % message["type"])


