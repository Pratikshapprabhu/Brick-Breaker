import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.Surface((100,100))
        self.img.fill((255,255,255))
        self.rect = pygame.Rect(100,100,0,0)
        self.vel = [0,0] 

    def update(self):
        self.rect.move_ip(self.vel)

    def draw(self, screen):
        screen.blit(self.img, self.rect)
