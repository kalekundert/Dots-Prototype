import sys

import pygame
from pygame.locals import *

from vector import *
from manager import Manager

class GUI(Manager):

    def __init__(self, game, world, messenger, tribe):
        Manager.__init__(self, game, world, messenger)

        self.tribe = tribe

        self.screen = None
        self.screen_size = None

        self.selection = []

        self.modifier = False

        self.selection_start = ZeroVector()
        self.selection_end = ZeroVector()
        self.selecting = False

        self.pan_speed = 300
        self.pan_velocity = ZeroVector()
        self.world_position = ZeroVector()

    def setup(self):
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), FULLSCREEN)
        pygame.display.set_caption("Dots Prototype")

        size_tuple = self.screen.get_size()
        self.screen_size = Vector(*size_tuple)

        # Setting the initial viewpoint
        center = ZeroVector()
        for dot in self.tribe:
            center += dot.position

        center /= len(self.tribe.dots)
        self.world_position = center - self.screen_size / 2

    def update(self, time):
        self.handle_messages()

        self.update_input()
        self.handle_input()

        self.update_screen(time)

    def handle_messages(self):
        messages = self.receiver.dump_messages()
        for message in messages:

            if message["type"] == "kill":
                dot = message["dot"]
                if dot in self.selection:
                    self.selection.remove(dot)

            else:
                raise ValueError("Unrecognized message.")

    def update_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
                if event.key in (K_LSHIFT, K_RSHIFT):
                    self.modifier = True

            if event.type == KEYUP:
                if event.key in (K_LSHIFT, K_RSHIFT):
                    self.modifier = False
                if event.key == K_x:
                    self.stop_selection()


            if event.type == MOUSEBUTTONDOWN:
                position = Vector(*event.pos)

                # Left click: select
                if event.button == 1:
                    self.start_selection(position)

            if event.type == MOUSEMOTION:
                position = Vector(*event.pos)

                self.pan_screen(position)
                self.update_selection(position)

            if event.type == MOUSEBUTTONUP:
                position = Vector(*event.pos)

                # Left click: select
                if event.button == 1:
                    self.finish_selection(position)

                # Right click: move
                if event.button == 3:
                    self.move_selection(position)

    def start_selection(self, click):
        self.selection_start = click
        self.selection_end = click
        self.selecting = True

    def pan_screen(self, position):
        self.pan_velocity = ZeroVector()

        top = 0; left = 0
        right = self.screen_size.x
        bottom = self.screen_size.y

        if position.x < left + 5:
            self.pan_velocity += Vector(-1, 0)
        if position.x > right - 5:
            self.pan_velocity += Vector(1, 0)

        if position.y < top + 5:
            self.pan_velocity += Vector(0, -1)
        if position.y > bottom - 5:
            self.pan_velocity += Vector(0, 1)

        self.pan_velocity *= self.pan_speed

    def update_selection(self, position):
        if self.selecting:
            self.selection_end = position

    def finish_selection(self, click):
        start = self.selection_start
        end = self.selection_end

        top = min(start.y, end.y)
        bottom = max(start.y, end.y)

        left = min(start.x, end.x)
        right = max(start.x, end.x)

        self.selection = []

        for dot in self.tribe:
            position = dot.position
            screen_position = position - self.world_position

            if top > screen_position.y: continue
            if bottom < screen_position.y: continue

            if left > screen_position.x: continue
            if right < screen_position.x: continue

            self.selection.append(dot)

        self.selection_start = ZeroVector()
        self.selection_end = ZeroVector()
        self.selecting = False

    def move_selection(self, position):
        if len(self.selection) == 0:
            return

        center = ZeroVector()

        for dot in self.selection:
            center += dot.position

        center = center / len(self.selection)

        for dot in self.selection:
            displacement = dot.position - center
            target = position + displacement + self.world_position

            message = {}
            message["type"] = "move" if not self.modifier else "waypoint"
            message["position"] = target

            self.send_message(dot, message)

    def stop_selection(self):
        message = { "type" : "stop" }

        for dot in self.selection:
            self.send_message(dot, message)

    def handle_input(self):
        # Might just want to make this part of the update_input() method.  
        # We'll see how that goes once I get to doing real input.
        pass

    def update_screen(self, time):
        # Use Map object to select only the dots on the screen.
        self.screen.fill((0, 0, 0))

        # Pan the screen if necessary
        self.world_position += self.pan_velocity * (time / 1000)

        # Let the tokens draw themselves
        for token in self.world:
            token.draw(self.screen, self.world_position)

        # Highlight the selection
        for token in self.selection:
            token.draw_selected(self.screen, self.world_position)

        # Draw the selection box
        if self.selecting:
            start = self.selection_start
            end = self.selection_end

            top = min(start.y, end.y)
            left = min(start.x, end.x)

            width = abs(start.x - end.x)
            height = abs(start.y - end.y)

            color = (255, 255, 255)
            rect = Rect(left, top, width, height)
            width = 1

            pygame.draw.rect(self.screen, color, rect, width)

        # Update the display
        pygame.display.flip()
