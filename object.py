import pygame
import game


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.Surface((20,125))
        self.img.fill((255,255,255))
        self.rect = self.img.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.vel = [0,0] 

    def update(self):
        self.rect.move_ip(self.vel)
        if self.rect.y < 0 :
            self.rect.y = 0
        elif self.rect.bottom > game.Game.screen.get_rect().bottom :
            self.rect.bottom = game.Game.screen.get_rect().bottom 

    def draw(self):
        game.Game.screen.blit(self.img, self.rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.Surface((20,20))
        self.img.fill((255,255,255))
        self.rect = self.img.get_rect()
        self.rect.x = game.Game.screen.get_rect().width/2
        self.rect.y = game.Game.screen.get_rect().height/2
        self.vel = [5,5] 
        

    def update(self):
        self.rect.move_ip(self.vel)
        if self.rect.x < 0 :
            self.rect.x = 0 
            game.Game.run = False
        elif self.rect.right > game.Game.screen.get_rect().right :
            self.rect.right = game.Game.screen.get_rect().right
            self.vel[0] = -self.vel[0] 
        if self.rect.y < 0 :
            self.rect.y = 0
            self.vel[1] = -self.vel[1] 
        elif self.rect.bottom > game.Game.screen.get_rect().bottom :
            self.rect.bottom = game.Game.screen.get_rect().bottom 
            self.vel[1] = -self.vel[1] 


    def draw(self):
        game.Game.screen.blit(self.img, self.rect)
