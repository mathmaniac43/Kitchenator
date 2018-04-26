import socket
import sys
import time

sV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sV_address = ('localhost', 8000)
#s2_address = ('localhost', 8001)

sV.bind(sV_address)
#s2.bind(s2_address)

s1.listen(1)
#s2.listen(1)

#s1.setblocking(0)
#s2.setblocking(0)

c1, c1_address = s1.accept()

print(c1.recv(4096))

while True:
    time.sleep(5)
    
    print 'trying 8000'
    try:
        c1.sendall('k')
        s = c1.recv(4096)
        print(s)
        
    finally:
        print 'oops'
    #print 'trying 8001'
    #c2, c2_address = s2.accept()
    #try:
    #    s = c2.recv(4096)
    #    print(s)
    #    c2.sendall(s)
    #    
    #finally:
    #    print 'closing 8001'
    #    c2.close()
    
c1.close()