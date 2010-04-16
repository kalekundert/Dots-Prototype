class Messenger:

    NEXT_ADDRESS = 0

    def __init__(self):
        self.players = []
        self.subscriptions = {}

    def deliver (self, sender_address, receiver_address, message):
        receiver = self.players[receiver_address]
        receiver.receive_message (message)

        listeners = self.subscriptions.get(sender_address)
        if not listeners:
            return

        for listener in listeners:
            listener.receive_message (message)

    def register (self, player):
        player.address = Messenger.NEXT_ADDRESS
        Messenger.NEXT_ADDRESS += 1

        self.players.append (player)

    def subscribe (self, listener, sender):
        listeners = self.subscriptions.get(sender)
        if not listeners:
            listeners = []

        listeners.append(listener)

class Receiver:
    def __init__(self, messenger):
        self.messenger = messenger
        messenger.register (self)

        self.messages = []

    def receive_message (self, message):
        self.messages.append (message);
        
    def dump_messages(self):
        messages = self.messages
        self.messages = []
        return messages

class Sender(Receiver):
    def send_message(self, receiver, message):
        self.messenger.deliver (self.address, receiver.address, message)

    #def listen_to (self, sender):
        #self.messenger.subscribe(self, sender)
