import sprite 
import pygame
import net
import pickle
import args
import glb

#screen = comp screen
#field = playing screen
#game surface = 800/450 default screen
#border surface = field outside border

class Game:
    field = pygame.Surface((glb.field_width,glb.field_height))
    run = True

    def __init__(self):
        ok,fail=pygame.init()
        self.sock,self.remote = args.init()
        self.screen = pygame.display.set_mode()
        self.game_surface = pygame.Surface((glb.game_screen_width,glb.game_screen_height))
        self.border = pygame.Surface((glb.border_width,glb.border_height))
        self.clock  = pygame.time.Clock()
        self.blocks = []
        self.player = sprite.Player()
        self.opponent = sprite.Opponent() 
        self.ball = sprite.Ball(self.player)
        self.oball = sprite.Ball(self.opponent)
        self.oball.img.fill ((0,0,0))
        self.border.fill((255,255,255))

        print(f"Initialization passed = {ok} failed = {fail} ")

        for x in range (int(glb.columns/2)):
            for y in range (glb.rows):
                self.blocks.append(sprite.Block(True, x*glb.block_width, y*glb.block_height, glb.block_width, glb.block_height))
        
        for x in range (int(glb.columns/2), glb.columns):
            for y in range (glb.rows):
                self.blocks.append(sprite.Block(False, x*glb.block_width, y*glb.block_height, glb.block_width, glb.block_height))
       
        pygame.time.set_timer(glb.TMR_EVE_1,200)
        print("Successfully Initiated")

    def handle_events(self):
        delay = self.clock.tick(60)
        events = pygame.event.get()
        for eve in events:
            if eve.type == pygame.QUIT:
                Game.run = False
            elif eve.type == pygame.KEYDOWN:
                if eve.key == pygame.K_w:
                    self.player.vel[1] = -300*delay/1000
                elif eve.key == pygame.K_s:
                    self.player.vel[1] = 300*delay/1000
            elif eve.type == pygame.KEYUP:
                if eve.key == pygame.K_w or eve.key == pygame.K_s:
                    self.player.vel[1] = 0
            elif eve.type == glb.TMR_EVE_1:
                self.up_transfer()

    def update(self):
        self.player.update()
        if self.player.rect.colliderect(self.ball.rect):
           self.ball.vel[0] = -self.ball.vel[0]  
        self.ball.update()
        for block in self.blocks:
            block.update(self.ball,self.player)
            
    def up_transfer(self):
        x  = pickle.dumps((self.player.rect,self.ball.rect))
        try:
            self.sock.sendto(x,(self.remote,glb.port))
            r = self.sock.recv(120)
            paddle,ball = pickle.loads(r)
            self.opponent.rect.y = paddle.y
            self.oball.rect.y = ball.y
            self.oball.rect.x =glb.field_width - ball.x - ball.width
            for block in self.blocks : 
                if block.state and block.rect.colliderect(self.oball.rect):
                    block.state = False
        except (BrokenPipeError , EOFError):
            print (" Player left")
            Game.run = False

    def render(self):
        self.game_surface.fill((100,100,100))
        Game.field.fill((0,0,0))
        for block in self.blocks:
            block.draw()
        self.player.draw()
        self.opponent.draw()
        self.ball.draw()
        self.oball.draw()
        self.game_surface.blit(self.border, pygame.rect.Rect(glb.border_x, glb.border_y,glb.border_width,glb.border_height))
        self.game_surface.blit(self.field, pygame.rect.Rect(glb.field_x, glb.field_y,glb.field_width, glb.field_height))
        pygame.transform.scale(self.game_surface, self.screen.get_rect().size, self.screen)
        pygame.display.update()

    def quit(self):
        print ("Exiting now")
        pygame.quit()
        self.sock.close()
