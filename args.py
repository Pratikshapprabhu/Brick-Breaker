import sys
import net

def init():
    if len(sys.argv) > 1 :
        if sys.argv[1] == "-s" :
            return net.listen()
        elif sys.argv[1] == "-c" :
            return net.connect(sys.argv[2]) 
    print (f"Usage : {sys.argv[0]} (-s | -c ipaddress)")
    sys.exit()


