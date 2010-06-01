from vector import *
from token import Token

class Tribe(Token):
    def __init__(self, receiver, color, x, y):
        Token.__init__(self, receiver)

        self.dots = []
        self.manager = None     # Set in the GUI manager constructor.

        self.color = color
        self.position = Vector(x, y)

    def __iter__(self):
        for dot in self.dots:
            yield dot

    def update(self, time):
        messages = self.receiver.dump_messages()
        for message in messages:

            if message["type"] == "kill":
                dot = message["dot"]
                self.remove_dot(dot)
                print "%s: %d dots left" % (self.color, len(self.dots))

            else:
                raise ValueError("Bad message type '%s'." % message["type"])

    def add_dot(self, dot):
        self.dots.append(dot)

    def remove_dot(self, dot):
        if dot in self.dots:
            self.dots.remove(dot)
