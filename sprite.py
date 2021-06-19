import pygame
import game
import glb
import random
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.Surface((glb.paddle_width,glb.paddle_height)) #
        self.img.fill((255,255,255))
        self.rect = self.img.get_rect(x=glb.paddle_x, y=glb.paddle_y)
        self.vel = [0,0] 

    def update(self):
        self.rect.move_ip(self.vel[0], self.vel[1])
        if self.rect.y < 0 :
            self.rect.y = 0
        elif self.rect.bottom > glb.field_height :
            self.rect.bottom = glb.field_height 

    def draw(self):
        game.Game.field.blit(self.img, self.rect)

class Opponent(Player):
    def __init__(self):
        super().__init__()
        self.rect.x = glb.field_width - self.rect.width - glb.paddle_x
        self.img.fill((0,0,0))

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_direction = 1
        self.y_direction = 1
        self.y_vel = random.randint(int(glb.ball_velocity*30/100),int(glb.yvel_max))
        self.img = pygame.Surface((2*glb.ball_radius,2*glb.ball_radius))
        self.img.fill((255,255,255))
        self.rect = self.img.get_rect(x=glb.ball_x,y=glb.ball_y)
    @property
    def x_vel(self):
        return int(math.sqrt(glb.ball_velocity ** 2 - self.y_vel ** 2) * self.x_direction)
    @x_vel.setter
    def x_vel(self,x):
        self.y_vel = int(math.sqrt(glb.ball_velocity ** 2 - x ** 2))
        

    def update(self,delay):
        self.rect.move_ip(self.x_vel*delay/1000,self.y_vel*self.y_direction*delay/1000)
        if self.rect.x < 0 :
            self.rect.x = 0 
            game.Game.run = False
            game.Game.lost = True
        elif self.rect.right > glb.field_width :
            self.rect.right = glb.field_width
            self.x_direction = -self.x_direction 
        if self.rect.y < 0 :
            self.rect.y = 0
            self.y_direction = -self.y_direction
        elif self.rect.bottom > glb.field_height :
            self.rect.bottom = glb.field_height
            self.y_direction = -self.y_direction


    def draw(self):
        game.Game.field.blit(self.img, self.rect)


class Block(pygame.sprite.Sprite):
    def __init__(self,state,x,y,w,h):
        self.state = state
        self.rect = pygame.rect.Rect(x,y,w,h)
        

    def draw(self):
        if self.state:
            pygame.draw.rect(game.Game.field,(0,0,0),self.rect)
        else:
            pygame.draw.rect(game.Game.field,(255,255,255),self.rect)
            
    def update(self,ball,player):
        state_change = False
        if not self.state and self.rect.colliderect(ball.rect):
            self.state = True
            state_change = True
        if not self.state and (self.rect.colliderect(player.rect) or self.rect.x <= 0):
            game.Game.run = False
            game.Game.lost = True
            print (self.state)
        return state_change
         





