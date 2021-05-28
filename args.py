import sys
import net

port = 1111
def init():
    if len(sys.argv) == 3 :
        if sys.argv[1] == "-s" :
            s = net.listen(sys.argv[2],port)
            return (s,True)
        elif sys.argv[1] == "-c" :
            s = net.connect(sys.argv[2],port)
            return (s,False)
    print (f"Usage : {sys.argv[0]} (-s | -c) ipaddress")
    sys.exit()


