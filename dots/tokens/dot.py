import pygame
from pygame import *

from vector import *
from token import Token

from dots.constants import *

class Dot(Token):
    FISRT = True
    def __init__(self, receiver, tribe, position):
        Token.__init__(self, receiver)
        self.tribe = tribe

        self.first = Dot.FISRT
        Dot.FISRT = False

        self.position = position
        self.velocity = ZeroVector()

        self.dead = False
        self.health = MAX_HEALTH
        self.growth = 0

        self.speed = 50
        self.radius = 15
        self.color = tribe.color

        self.targets = []

    def __eq__(self, other):
        return self is other

    def create(self):
        self.tribe.add_dot(self)

    def update (self, time):
        messages = self.receiver.dump_messages()
        for message in messages:

            if message["type"] == "move":
                self.targets = [message["position"]]

            elif message["type"] == "waypoint":
                position = message["position"]
                self.targets.append(position)

            elif message["type"] == "reposition":
                self.position = message["position"]

            elif message["type"] == "damage":
                self.health -= message["damage"]
                # This will not be called after the dot is killed, because
                # the world will not update this dot once it (the world)
                # thinks the dot is dead.  So my hacky self.dead variable 
                # isn't doing anything.

            elif message["type"] == "growth":
                self.growth = message["growth"]

            elif message["type"] == "stop":
                self.velocity = ZeroVector()
                self.targets = []
            else:
                raise ValueError("Bad message type '%s'." % message["type"])

        try:
            target = self.targets[0]
            displacement = target - self.position

            if displacement.get_magnitude() < self.radius:
                self.targets.remove(target)
                self.velocity = ZeroVector()
            else:
                self.velocity = displacement.get_normal(self.speed)

        except IndexError:
            pass

        self.position += self.velocity * (time / 1000)

    def draw(self, screen, offset):
        color = self.color
        radius = self.radius

        position = self.position - offset
        tuple = position.get_int_tuple()

        self.draw_health(screen, offset)
        pygame.draw.circle(screen, color, tuple, radius)

    def draw_health(self, screen, offset):
        height = 4
        margin = 2
        length = 25

        offset += Vector(length / 2, self.radius + margin + height)

        injured_color = (255, 0, 0)
        injured_length = length

        injured_position = self.position - offset
        injured_tuple = injured_position.get_tuple()
        injured_rect = Rect(injured_tuple, (injured_length, height))

        healthy_color = (0, 255, 0)
        healthy_length = (self.health / MAX_HEALTH) * length

        healthy_tuple = injured_tuple
        healthy_rect = Rect(healthy_tuple, (healthy_length, height))

        outline_color = (0, 0, 0)
        outline_rect = injured_rect

        pygame.draw.rect (screen, injured_color, injured_rect)
        if healthy_length > 1:
            pygame.draw.rect (screen, healthy_color, healthy_rect)
        pygame.draw.rect (screen, outline_color, outline_rect, 1)

    def draw_selected(self, screen, offset):
        if self.dead:
            return

        width = 2
        color = self.color
        radius = self.radius + 5

        position = self.position - offset
        tuple = position.get_int_tuple()

        pygame.draw.circle(screen, color, tuple, radius, width)

