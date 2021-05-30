#!/usr/bin/python
from game import *

game = Game()
while game.run:
    game.handle_events()
    game.update()
    game.send()
    game.render()
game.quit()
