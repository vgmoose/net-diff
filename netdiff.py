#!/bin/python

import os, sys, urllib2, hashlib
from socket import *

# default port
port = 3823
host = False
isclient = False

chunk = 9999

def usage():
    print("on server:\n\tpython %s file [port]" % sys.argv[0])
    print("on client:\n\tpython %s file [hostname] [post]" % sys.argv[0])
    exit()
    
def md5(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

# first argument is required and is the file to diff
try:
    #read all bytes into memory
    content = bytearray(open(sys.argv[1], "rb").read())
    print("\nLoaded %s (%i bytes) into memory!" % (os.path.basename(sys.argv[1]), len(content)))
    print("Hash: %s\n" % md5(content))
except:
    usage()

# second argument is either a port or an ip
if (len(sys.argv) > 2):
    try:
        port = int(sys.argv[2])
    except:
        host = sys.argv[2]
        isclient = True
        
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

# communicate will send then receive or receive then send depending on the isclient variable
def communicate(my_value):
    # client sends second
    if isclient:
        peer_value = peer.recv(chunk)
        peer.send(my_value)
    # server sends first
    else:
        peer.send(my_value)
        peer_value = peer.recv(chunk)
    
    # return the peer's value
    return peer_value

# common networking code
def common_networking():
    print("Connected to %s!\n" % peer.getpeername()[0])
    
    # check if the sizes are the same
    size = communicate(str(len(content)))
    
    print size
    print str(len(content))
    

# if client
if isclient:
    print("Trying to connect to %s on port %i..." % (host, port))
                    
    try:
        peer = socket(AF_INET, SOCK_STREAM)
        peer.connect((host, port))
    except:
        print("Error: No server found at %s" % host)
        exit()
    
    common_networking()
    
# if host
else:
    print("Hosting server on our public IP (%s) on port %i" % (urllib2.urlopen('http://ip.42.pl/raw').read(), port))
    print("Waiting for a client to connect...\n")
    
    server = socket(AF_INET, SOCK_STREAM)

    server.bind(('', port))
    server.listen(0)
    peer, addr = server.accept()
    
    common_networking()
    
