import json
import math
import time

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8001)
sock.connect(server_address)
sock.settimeout(0.05)
sock.sendall('woke up')


while True:
    # Handle json
    try:
        data = sock.recv(1)
        
        print('data: "%s"' % data)
        if data != "":
            full_json = '{%s, %s, %s}' % ('earth', 'wind', 'fire')
            sock.sendall(full_json)
    except socket.timeout:
        print 'timeout'
    except:
        print 'wtf'

    time.sleep(1)