import pygame
import game


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.Surface((20,125))
        self.img.fill((255,255,255))
        self.rect = self.img.get_rect()
        self.rect.x = game.Game.border.x
        self.rect.y = game.Game.border.y
        self.vel = [0,0] 

    def update(self):
        self.rect.move_ip(self.vel)
        if self.rect.y < game.Game.border.y :
            self.rect.y = game.Game.border.y
        elif self.rect.bottom > game.Game.border.bottom :
            self.rect.bottom = game.Game.border.bottom 

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
        if self.rect.x < game.Game.border.x :
            self.rect.x = game.Game.border.x 
            game.Game.run = False
        elif self.rect.right > game.Game.border.right :
            self.rect.right = game.Game.border.right
            self.vel[0] = -self.vel[0] 
        if self.rect.y < game.Game.border.y :
            self.rect.y = game.Game.border.y
            self.vel[1] = -self.vel[1] 
        elif self.rect.bottom > game.Game.border.bottom :
            self.rect.bottom = game.Game.border.bottom 
            self.vel[1] = -self.vel[1] 


    def draw(self):
        game.Game.screen.blit(self.img, self.rect)
