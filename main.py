#!/usr/bin/python
from game import *

game = Game()
while Game.run:
    game.handle_events()
    game.update()
    game.render()
game.quit()
