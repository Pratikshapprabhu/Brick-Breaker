import socket

soc = None

def init():
    global soc
    soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    soc.bind(("0.0.0.0",5000))
    try: 
        while True:
            rdata,remote = soc.recvfrom(100)
            handle_connection(remote,rdata)
    except KeyboardInterrupt:
        quit()
        
def handle_connection(remote,rdata):
    print(f"data recved from hostname: {remote[0]},port: {remote[1]},data is {rdata}")
    soc.sendto(rdata,remote)
            
def quit():
    soc.close()



