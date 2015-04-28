#!/bin/python

import os, sys, urllib2
from socket import *

# default port
port = 3823
host = False

def usage():
    print("on server:\n\tpython %s file [port]" % sys.argv[0])
    print("on client:\n\tpython %s file [hostname] [post]" % sys.argv[0])
    exit()

# first argument is required and is the file to diff
try:
    content = open(sys.argv[1], "rb")
except:
    usage()

# second argument is either a port or an ip
if (len(sys.argv) > 2):
    try:
        port = int(sys.argv[2])
    except:
        host = sys.argv[2]
        
# third argument can only be a port
if (len(sys.argv) > 3):
        try:
            port = int(sys.argv[3])
        except:
            print("invalid port number")
            
# order of operations:
# 1. connect
# 2. send sizes (server first)
# 3. if the same, split file in half and hash both halves
# 4. transmit both hashes (server first)
# 5. recurse step 4 on the halves that don't match hashes
# 6. when no halves match anymore, report area of bytes that is different
# 7. if small, send the bytes over the server to output them and their offsets

# future:
# ascii support (render text like diff does)
# work on files of arbitrary sizes, not just the same


## if client
#if host:
#    print("Connecting to %s on port %i" % (host, port))
#    
#    s = socket(AF_INET, SOCK_STREAM)
#    s.connect((host, port))
#    
#    # receive size
#    size = s.recv(9999)
#    s.send(my_name)
#    
## if host
#else:
#    print("Hosting server on our public IP (%s) on port %i" % (urllib2.urlopen('http://ip.42.pl/raw').read(), port))
#    