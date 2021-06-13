import socket
import pygame
import glb
import sys
import os

socket.setdefaulttimeout(10.0)
paclen = 10

def listen(host):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.bind((host,glb.port))
    data,(rhost,_) = sock.recvfrom(paclen)
    sock.sendto(data,(rhost,glb.port))
    data2,(r2host,_) = sock.recvfrom(paclen)
    if rhost == r2host and data == data2:
        return (sock,rhost)
    else:
        sock.sendto(glb.connection_close,(rhost,glb.port))
        sock.close()
        pygame.quit()
        sys.exit()

def connect(host,target):
    data =os.urandom(paclen)
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.bind((host,glb.port))
    sock.sendto(data,(target,glb.port))
    sdata,(shost,_) = sock.recvfrom(paclen)
    if sdata == data and shost == target:
        sock.sendto(data,(target,glb.port))
        return sock
    else :
        sock.close()
        pygame.quit()
        sys.exit()

def game_init(soc,server):
    if server :
        payload = b"init"
        soc.sendall(payload)
        if payload != soc.recv(4):
            sys.exit()
        else :
            soc.sendall(payload)
    else :
        s = soc.recv(4)
        soc.sendall(s)
        if s != soc.recv(4):
            sys.exit()
    pygame.time.set_timer(glb.TMR_EVE_1,200)

