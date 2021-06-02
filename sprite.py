import pygame
import game


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.Surface((20,125)) #
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

class Opponent(Player):
    def __init__(self):
        super().__init__()
        self.rect.x = game.Game.border.right - self.rect.width
        self.img.fill((0,0,0))

class Ball(pygame.sprite.Sprite):
    def __init__(self,pad):
        super().__init__()
        self.img = pygame.Surface((20,20))
        self.img.fill((255,255,255))
        self.rect = self.img.get_rect()
        self.rect.midleft = pad.rect.midright
        self.vel = [3,3] 
        

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


class Block(pygame.sprite.Sprite):
    def __init__(self,state,x,y,w,h):
        self.state = state
        self.rect = pygame.rect.Rect(x,y,w,h)
        

    def draw(self):
        if self.state:
            pygame.draw.rect(game.Game.screen,(0,0,0),self.rect)
        else:
            pygame.draw.rect(game.Game.screen,(255,255,255),self.rect)
            
    def update(self,ball,player,border):
        if not self.state and self.rect.colliderect(ball.rect):
            self.state = True
            ball.vel[0] = -ball.vel[0] 
        if not self.state and (self.rect.colliderect(player.rect) or self.rect.x < border.x):
            game.Game.run = False
            print ("YOU LOST!!!!!!")
         





