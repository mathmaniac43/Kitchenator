import json
# from callHandlers import gestureCalls, stateCalls, visionCalls, armCalls, uiCalls, voiceCalls
import socket
import sys
import time

from callHandlers import states # states.py maintains all Kitchenator states

print 'start'
states.init()

''' Vision Stuff '''
colorOfInterest = 'none'
sV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
vSocket = 51123
sV_address = ('127.0.0.1', vSocket)
sV.bind(sV_address)
sV.listen(1)
cV, cV_address = sV.accept()

''' Myo Stuff '''
sM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mSocket = 51127
mV_address = ('127.0.0.1', mSocket)
sM.bind(sM_address)
sM.listen(1)
cM, cM_address = sM.accept()



while True:
    
    # if states.kitchenatorState == 'standby':
    '''
    Check Vision Client first
    '''
    
    print 'trying Vision on %d' % vSocket
    try:
        data = {}
        data['goalIngredient'] = 'nutmeg'
        json_data = json.dumps(data)
        cV.sendto(json_data, cV_address)
        try:
            s = cV.recv(1)
        except socket.timeout, e:
            print("timeout, failed to receive")
        print(s + '\n')
        
    except Exception, e:
        print(e)
        print 'shit hit the fan'
        print('****')

    time.sleep(1)


cV.close()