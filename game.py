import socket
import sprite 
import pygame
import net
import pickle
import args
import glb
import threading

#screen = comp screen
#field = playing screen
#game surface = 800/450 default screen
#border surface = field outside border

class Game:
    field = pygame.Surface((glb.field_width,glb.field_height))
    run = True
    lost = False
    def __init__(self):
        self.frame_delay = 0
        ok,fail=pygame.init()
        #  self.sock,self.remote = args.init()
        self.screen = pygame.display.set_mode()
        self.game_surface = pygame.Surface((glb.game_screen_width,glb.game_screen_height))
        self.border = pygame.Surface((glb.border_width,glb.border_height))
        self.clock  = pygame.time.Clock()
        self.blocks = []
        self.player = sprite.Player()
        self.opponent = sprite.Opponent() 
        self.ball = sprite.Ball()
        self.oball = sprite.Ball()
        self.border.fill((255,255,255))
        self.frame_counter = 10
        #  self.rthread = threading.Thread(target = self.receive)
        
        #  self.rthread.start()
        if fail:
            print(f"Initialization passed = {ok} failed = {fail} ")

        for x in range (int(glb.columns/2)):
            for y in range (glb.rows):
                self.blocks.append(sprite.Block(True, x*glb.block_width, y*glb.block_height, glb.block_width, glb.block_height))
        
        for x in range (int(glb.columns/2), glb.columns):
            for y in range (glb.rows):
                self.blocks.append(sprite.Block(False, x*glb.block_width, y*glb.block_height, glb.block_width, glb.block_height))

    def handle_events(self):
        self.frame_delay = self.clock.tick(60)
        events = pygame.event.get()
        for eve in events:
            if eve.type == pygame.QUIT:
                Game.run = False
            elif eve.type == pygame.KEYDOWN:
                if eve.key == pygame.K_w:
                    self.player.vel[1] = -300*self.frame_delay/1000
                elif eve.key == pygame.K_s:
                    self.player.vel[1] = 300*self.frame_delay/1000
            elif eve.type == pygame.KEYUP:
                if eve.key == pygame.K_w or eve.key == pygame.K_s:
                    self.player.vel[1] = 0

    def update(self):
        self.player.update()
        if self.player.rect.colliderect(self.ball.rect):
            self.ball.x_direction = 1   
            multiplier = 2 * (self.ball.rect.center[1] - self.player.rect.center[1]) / self.player.rect.height
            #(vmax * mult - (abs(mult) * v) +v
            y_vel = glb.yvel_max * multiplier + (1 - abs(multiplier)) * self.ball.y_vel * self.ball.y_direction
            if y_vel > 0:
                self.ball.y_direction = 1
            else:
                self.ball.y_direction = -1
            self.ball.y_vel = abs(y_vel)

        self.ball.update(self.frame_delay)
        area = 0 
        finalrect = None
        # Block with higher area of intersection is considerd
        for block in self.blocks:
            if block.update(self.ball,self.player):
                crect = block.rect.clip(self.ball)
                carea = crect.width * crect.height
                if carea > area:
                    finalrect = crect
                    area =carea
        if finalrect:
            if finalrect.height > finalrect.height:
                self.ball.y_direction = -self.ball.y_direction
            elif finalrect.width < finalrect.height:
                self.ball.x_direction = -self.ball.x_direction
            else :
                self.ball.y_direction = -self.ball.y_direction
                self.ball.x_direction = -self.ball.x_direction
            #  self.send_bdata()

    def send_bdata(self):
        block_array = [True]*len(self.blocks)
        for index,block in enumerate(self.blocks):
            block_array[index] = block.state
        block_dump = net.PackType.block
        block_dump += pickle.dumps(block_array)
        try:
            self.sock.sendto(block_dump,(self.remote,glb.port))
        except (BrokenPipeError , EOFError):
            print (" Player left")
            Game.run = False

    def transmit_data(self):
        data = net.PackType.data
        data += pickle.dumps((self.player.rect,self.ball.rect))
        try:
            self.sock.sendto(data,(self.remote,glb.port))
        except (BrokenPipeError , EOFError):
            print (" Player left")
            Game.run = False

    def receive(self):
        while Game.run:
            try:
                packet = self.sock.recv(500)
            except (socket.timeout, OSError):
                print("Player left")
                Game.run = False
                continue
            ptype = bytes(packet[:1])
            data = packet[1:]
            if ptype == net.PackType.data:
                self.handle_data(data)
            elif ptype == net.PackType.block:
                self.handle_block(data)
            elif ptype == net.PackType.lost:
                Game.run = False
            elif ptype == net.PackType.close:
                Game.run = False

    def handle_block(self,data):
        block_array = pickle.loads(data)
        for index, state in enumerate(block_array):
            row = index % glb.rows
            column = index // glb.rows
            column = glb.columns - column - 1
            index = column * glb.rows + row 
            self.blocks[index].state = not state

    def handle_data(self,data):
        paddle,ball = pickle.loads(data)
        self.opponent.rect.y = paddle.y
        self.oball.rect.y = ball.y
        self.oball.rect.x = glb.field_width - ball.x - ball.width

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
        if Game.lost:
            self.sock.sendto(net.PackType.lost,(self.remote,glb.port))
            print("YOU LOST!!")
        else :
            print("YOU WIN")
        #  self.sock.sendto(net.PackType.close,(self.remote,glb.port))
        pygame.quit()
        #  self.sock.close()
        self.rthread.join()
