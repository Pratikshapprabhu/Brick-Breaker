#!/usr/bin/python
import pygame
from game import *

ok,fail=pygame.init()
print(f"Initialization passed = {ok} failed = {fail} ")

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()







    







while run:
    delay = clock.tick(60)
    screen.fill((0,0,0))
    events = pygame.event.get()
    for eve in events:
        if eve.type == pygame.QUIT:
            run = False
        elif eve.type == pygame.KEYDOWN:
            if eve.key == pygame.K_w:
                p1.vel[1] = -100*delay/1000
            elif eve.key == pygame.K_a:
                p1.vel[0] = -100*delay/1000
            elif eve.key == pygame.K_s:
                p1.vel[1] = 100*delay/1000
            elif eve.key == pygame.K_d:
                p1.vel[0] = 100*delay/1000
        elif eve.type == pygame.KEYUP:
            if eve.key == pygame.K_w or eve.key == pygame.K_s:
                p1.vel[1] = 0
            elif eve.key == pygame.K_a or eve.key == pygame.K_d:
                p1.vel[0] = 0
    p1.update()
    screen.blit(p1.img,p1.rect)

    pygame.display.update()

print ("Exiting now")
pygame.quit()
