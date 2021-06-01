import sprite 
import pygame
import socket
import net
import pickle
import args
import glb

screen_border_width = 5
rows = 5
columns = 20
class Game:
    border = None
    screen = pygame.Surface((600,400))
    run = True

    def __init__(self):
        socket.setdefaulttimeout(10.0)
        ok,fail=pygame.init()
        print(f"Initialization passed = {ok} failed = {fail} ")
        self.sock,server = args.init()
        self.display_surface = pygame.display.set_mode()
        Game.border = self.screen.get_rect().inflate(-20,-20)
        Game.border.width -= Game.border.width % columns
        Game.border.height -= Game.border.height % rows
        self.clock  = pygame.time.Clock()
        self.objects = []
        self.player = sprite.Player()
        self.opponent = sprite.Opponent() 
        self.ball = sprite.Ball(self.player)
        block_width = int(Game.border.width/columns)
        block_height = int(Game.border.height/rows)
         
        for x in range (Game.border.x,int(Game.border.width/2 + Game.border.x),block_width):
            for y in range (Game.border.y,Game.border.height,block_height):
                self.objects.append(sprite.Block(True,x,y,block_width,block_height))
        
        for x in range (int(Game.border.width/2 + Game.border.x),Game.border.right,block_width):
            for y in range (Game.border.y,Game.border.height,block_height):
                self.objects.append(sprite.Block(False,x,y,block_width,block_height))
       
        net.init(self.sock,server)
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
        for sprite in self.objects:
            sprite.update(self.ball)
            
    def up_transfer(self):
        x  = pickle.dumps(self.player.rect)
        try:
            self.sock.sendall(x)
            r = self.sock.recv(60)
            loc = pickle.loads(r)
            self.opponent.rect.y = loc.y
            print (f"Opponent location {loc}")
        except BrokenPipeError:
            print (" Player left")
            Game.run = False

    def render(self):
        self.screen.fill((0,0,0))
        for sprite in self.objects:
            sprite.draw()
        self.player.draw()
        self.opponent.draw()
        self.ball.draw()
        pygame.draw.rect(Game.screen,(0,0,255),self.border.inflate(screen_border_width/2,screen_border_width/2),width = screen_border_width)
        pygame.transform.scale(Game.screen,self.display_surface.get_rect().size,self.display_surface)
        pygame.display.update()

    def quit(self):
        print ("Exiting now")
        pygame.quit()
        self.sock.close()
