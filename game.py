import object 
import pygame

screen_border_width = 5

class Game:
    run = True
    border = None
    screen = None
    def __init__(self):
        ok,fail=pygame.init()
        print(f"Initialization passed = {ok} failed = {fail} ")
        Game.screen = pygame.display.set_mode()
        Game.border = self.screen.get_rect().inflate(-20,-20)
        self.clock  = pygame.time.Clock()
        self.objects = []
        self.player = object.Player()
        self.ball = object.Ball()

    def handle_events(self):
        delay = self.clock.tick(60)
        events = pygame.event.get()
        for eve in events:
            if eve.type == pygame.QUIT:
                self.run = False
            elif eve.type == pygame.KEYDOWN:
                if eve.key == pygame.K_w:
                    self.player.vel[1] = -300*delay/1000
                elif eve.key == pygame.K_s:
                    self.player.vel[1] = 300*delay/1000
            elif eve.type == pygame.KEYUP:
                if eve.key == pygame.K_w or eve.key == pygame.K_s:
                    self.player.vel[1] = 0

    def update(self):
        self.player.update()
        if self.player.rect.colliderect(self.ball.rect):
           self.ball.vel[0] = -self.ball.vel[0]  
        self.ball.update()
        for object in self.objects:
            object.update()
            

    def render(self):
        self.screen.fill((0,0,0))
        self.player.draw()
        self.ball.draw()
        pygame.draw.rect(Game.screen,(0,0,255),self.border.inflate(screen_border_width/2,screen_border_width/2),width = screen_border_width)
        for object in self.objects:
            object.render()
        pygame.display.update()

    def quit(self):
        print ("Exiting now")
        pygame.quit()

    
