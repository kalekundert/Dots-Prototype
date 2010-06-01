from manager import Manager
from debug import debug

# Maybe this should be called the defeat manager...
class Victory(Manager):
    def __init__(self, game, world, messenger):
        Manager.__init__(self, game, world, messenger)

    def setup(self):
        self.keep_playing = True

    def update(self, time):
        messages = self.receiver.dump_messages()
        for message in messages:

            if message["type"] == "kill":
                dot = message["dot"]
                tribe = dot.tribe

                # The world is updated after the services, so the dot in
                # question won't have been removed yet.
                if len(tribe.dots) == 1:
                    # GUI and AI managers should be listening to this
                    # message, but they aren't right now.  
                    message = self.new_message("kill-player", tribe=tribe)

                    self.send_message(self, message)
                    self.send_message(self.world, message)

            elif message["type"] == "kill-player":
                tribe = message["tribe"]
                world = self.world

                # The same "off-by-one" logic does not apply here, because 
                # the world will receive the "kill-player" message on it's 
                # next update.  This is one reson why these conversations
                # should be handled all in one frame.
                if len(world.tribes) <= 1:
                    self.keep_playing = False

            else:
                raise ValueError("Invalid message type '%s'." % message["type"])


