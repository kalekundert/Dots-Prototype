#!/usr/bin/python

import sys
import time

from dots import *
from time import clock

try:
    messenger = messaging.Messenger()

    world = world.World(messenger)
    world.setup()

    game = game.Game(world, messenger)
    game.setup()

    last_tick = time.time()

    while True:
        this_tick = time.time()
        time_diff = 1000 * (this_tick - last_tick)

        game.update(time_diff)
        world.update(time_diff)

        last_tick = this_tick

except KeyboardInterrupt:
    sys.exit(0)
