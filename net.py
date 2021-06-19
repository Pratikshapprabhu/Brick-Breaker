import socket
import pygame
import glb
import sys
import os
import netifaces

socket.setdefaulttimeout(10.0)                              #set socket timeout = 10sec
paclen = 10                                                  #communication packet length = 10
host = netifaces.ifaddresses('wlan0')[netifaces.AF_INET6][0]['addr']
class PackType:
    syn = b"\x00"                                           #ack bit = 00
    data = b"\x01"                                          #data starts with 01
    block = b"\x02"                                         #block data starts with 02
    close = b"\xff"                                         #communication ends with ff 

def listen():                                           #function to wait for conecting opponent
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)#create socket for UDP communication
    sock.bind((host,glb.port))                              #
    try:
        data,addr_info = sock.recvfrom(paclen)              #three way hand shaking to confirm opponent player connection
        sock.sendto(data,(addr_info[0],glb.port))
        data2,addr_info2 = sock.recvfrom(paclen)
        if addr_info == addr_info2 and data == data2:
            return (sock,addr_info[0])
        else:
            sock.sendto(PackType.close,(addr_info[0],glb.port)) #if connection fails send close packet and end communication and close socket
            raise socket.timeout
    except socket.timeout:
        print("Socket Timeout")
        sock.close()
        pygame.quit()
        sys.exit()

def connect(target):                                  #function to connect 
    data =os.urandom(paclen)
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.bind((host,glb.port))
    try:
        sock.sendto(data,(target,glb.port))
        sdata,saddr_info = sock.recvfrom(paclen)
        if sdata == data and saddr_info[0] == target:
            sock.sendto(data,(target,glb.port))
            return (sock,target)
        else:
            raise socket.timeout
    except socket.timeout:
        print("Socket error")
        sock.close()
        pygame.quit()
        sys.exit()


