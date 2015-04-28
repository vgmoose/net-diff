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
    
    # get the remote's file size
    size = communicate(str(len(content)))
    
    # make sure they are the same
    if size == str(len(content)):
#        print("Filesizes are the same! Proceeding...\n")
        pass
    else:
        print("Filesizes are different. This is not supported at this time.")
        exit();
    
    # recursively compare md5s of each half of the bytes
    offset = compare(content, 0)
    
    print("These files start to differ at offset 0x%x" % offset)
    
def compare(data, offset):
    # get the middle
    midpoint = int(len(data)/2)
    
    # base case, when we're down to one byte stop
    if (len(data) == 1):
        return offset
    
    # split into two halves
    my_half1 = data[:midpoint]
    my_half2 = data[midpoint:]
    
    # md5 hash each half
    m1 = md5(my_half1)
    m2 = md5(my_half2)
    
    # get and send halves hashes to peer
    p1 = communicate(m1)
    p2 = communicate(m2)
    
    # compare them
    if m1 != p1:
        return compare(my_half1, offset)
    elif m2 != p2:
        return compare(my_half2, offset+midpoint)
    else:
        print("These files are identical!\n")
        exit()
        

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
    try:
        print("Hosting server on our public IP (%s) on port %i" % (urllib2.urlopen('http://checkip.rickyayoub.com').read(), port))
    except:
        pass
    print("Waiting for a client to connect...")
    
    server = socket(AF_INET, SOCK_STREAM)

    server.bind(('', port))
    server.listen(0)
    peer, addr = server.accept()
    
    common_networking()
    
