import pygame
from pygame.locals import *

from dots.messaging import Receiver

class Token:
    def __init__(self, receiver, position):
        self.receiver = receiver

        self.position = position
        self.radius = 5

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

    def draw (self, screen):
        color = (255, 0, 0)
        position = self.position.get_int_tuple()
        radius = self.radius

        pygame.draw.circle(screen, color, position, radius)
