#!/usr/bin/python
import pygame

ok,fail=pygame.init()
print(f"Initialization passed = {ok} failed = {fail} ")

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
run = True



while run:
    clock.tick(60)
    events = pygame.event.get()
    for eve in events:
        if eve.type == pygame.QUIT:
            run = False
    pygame.display.update()

print ("Exiting now")
pygame.quit()
