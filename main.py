#!/usr/bin/python
import pygame
from game import *

game = Game()
game.init()

while game.run:
    game.handl_events()
    game.update()
    game.render()

game.quit()
