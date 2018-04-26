import json
# from callHandlers import gestureCalls, stateCalls, visionCalls, armCalls, uiCalls, voiceCalls
import socket
import sys
import time

from callHandlers import states # states.py maintains all Kitchenator states

states.init()

ingredientOfInterest = 'none'

sV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sV_address = ('127.0.0.1', 8000)
sV.bind(sV_address)

sV.listen(1)

cV, cV_address = sV.accept()

print(cV.recv(4096))

while True:
    print 'trying Vision on 8000'
    try:
        cV.sendall('k')
        s = cV.recv(4096)
        print(s)
    finally:
        print 'oops'


cV.close()
