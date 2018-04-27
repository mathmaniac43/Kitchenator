import json
# from callHandlers import gestureCalls, stateCalls, visionCalls, armCalls, uiCalls, voiceCalls
import socket
import sys
import time
import struct

from callHandlers import states # states.py maintains all Kitchenator states

print 'start'
states.init()

''' Vision Stuff '''
# colorOfInterest = 'none'
# sV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# vSocket = 51127
# sV_address = ('127.0.0.1', vSocket)
# sV.bind(sV_address)
# sV.listen(1)
# cV, cV_address = sV.accept()

''' Myo Stuff '''
sM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mSocket = 51123
mV_address = ('127.0.0.1', mSocket)
sM.bind(mV_address)
sM.listen(1)
cM, cM_address = sM.accept()



while True:
    
    # if states.kitchenatorState == 'standby':
    '''
    Check Myo Client first
    '''
    
    print 'trying Myo on %d' % mSocket
    try:
        data = {}
        data['goalIngredient'] = 'nutmeg'
        json_data = json.dumps(data)
        cM.sendto(json_data, cM_address)
        try:
            s = cM.recv(13)
            print(s)
            jMsg = json.loads(s)
            print(jMsg["gesture"])
            # print(len(s))
            # print(s)
            # print(':'.join(x.encode('hex') for x in s))
            # print(int(s,16))

            # b = bytearray(s)
            # print(struct.unpack('<d', b))
        except socket.timeout, e:
            print("timeout, failed to receive")
        
    except Exception, e:
        print(e)
        print 'shit hit the fan'
        print('****')

    time.sleep(1)


cM.close()