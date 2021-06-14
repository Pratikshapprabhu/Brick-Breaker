#!/usr/bin/python
from game import *

game = Game()
while Game.run:
    game.handle_events()
    game.update()
    game.transmit_data()
    game.render()
game.quit()
