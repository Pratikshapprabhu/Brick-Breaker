import sys
import net

def init():
    if len(sys.argv) > 2 :
        if sys.argv[1] == "-s" :
            return net.listen(sys.argv[2])
        elif sys.argv[1] == "-c" :
            return net.connect(sys.argv[2],sys.argv[3]) 
    print (f"Usage : {sys.argv[0]} (-s | -c) ipaddress")
    sys.exit()


