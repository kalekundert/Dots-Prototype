import pygame
from pygame import *

from token import Token

class Map(Token):

    def __init__(self, receiver, size):
        Token.__init__(self, receiver)
        self.size = size

    def draw(self, screen, offset):
        color = (80, 80, 80)
        rect = Rect(-offset.x, -offset.y, self.size, self.size)

        pygame.draw.rect(screen, color, rect)
