import socket
import sys
import time

sV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sV_address = ('127.0.0.1', 8001)
#s2_address = ('localhost', 8001)

sV.bind(sV_address)
#s2.bind(s2_address)

sV.listen(1)


cV, cV_address = sV.accept()

print(cV.recv(4096))

while True:
    time.sleep(5)
    
    print 'trying 8000'
    try:
        cV.sendall('k')
        s = cV.recv(4096)
        print(s)
        
    finally:
        print 'oops'

cV.close()