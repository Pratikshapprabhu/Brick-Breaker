import pygame
import game


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.Surface((20,125))
        self.img.fill((255,255,255))
        self.rect = self.img.get_rect()
        print(self.rect)
        self.rect.move_ip(10,10)
        print(self.rect)
        self.vel = [0,0] 

    def update(self):
        self.rect.move_ip(self.vel)
        if self.rect.y < 0 :
            self.rect.y = 0
        elif self.rect.bottom > game.Game.screen.get_rect().bottom :
            self.rect.bottom = game.Game.screen.get_rect().bottom 

    def draw(self):
        game.Game.screen.blit(self.img, self.rect)
