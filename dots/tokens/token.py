from dots.messaging import Receiver

class Token:
    def __init__(self, receiver):
        self.receiver = receiver

    def get_receiver (self):
        return self.receiver

