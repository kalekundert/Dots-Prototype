from dots.messaging import Receiver

class Token:
    def __init__(self, messenger):
        self.receiver = Receiver(messenger)
        self.counter = 0

    def get_receiver (self):
        return self.receiver

    def update (self, time):
        messages = self.receiver.dump_messages()
        for message in messages:

            if message == "count":
                self.counter += 1
                print self.counter

            elif message == "hello":
                print "Hello world!"
            elif message == "goodbye":
                print "Goodbye world!"

            else:
                # Bad message type.
                raise ValueError;
