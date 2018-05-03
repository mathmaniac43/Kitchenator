import json
from bottle import run
from callHandlers import gestureCalls, stateCalls, visionCalls, armCalls, uiCalls, voiceCalls

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


run(host='127.0.0.1', port=12345, debug=True, reloader=True)

