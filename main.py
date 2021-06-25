#!/usr/bin/python

# This should be at the to so that pygame hello message will not print
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from game import *

game = Game()
while Game.run:
    game.handle_events()
    game.update()
    #  game.transmit_data()
    game.render()
game.quit()
