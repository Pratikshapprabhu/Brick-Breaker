#!/usr/bin/python
import sys
import server

if len(sys.argv) != 2:
    print(f"{sys.argv[0]} (-s | -c)")
elif sys.argv[1] == '-s':
    server.init()

else:
    print("client")

