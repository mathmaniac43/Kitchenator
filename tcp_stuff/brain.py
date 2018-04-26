import socket
import sys
import time

sV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
vSocket = 8001
sV_address = ('127.0.0.1', vSocket)
#s2_address = ('localhost', 8001)
sV.bind(sV_address)
#s2.bind(s2_address)
sV.listen(1)
cV, cV_address = sV.accept()
print(cV.recv(4096))

while True:
    
    '''
    Check Vision Client first
    '''
    
    print 'trying Vision on %d' % vSocket
    try:
        cV.sendall('k')
        s = cV.recv(4096)
        print(s)
        
    finally:
        print 'oops'


cV.close()