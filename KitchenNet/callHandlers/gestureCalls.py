from bottle import post, get, request
import json 

from . import states

'''
    All gesture related calls, updating the 'gesture' state in bottleService.py
'''
@post('/setGesture')
def setGesture():
    states.gesture = json.loads(request.body.read())
    return 'cool'

@get('/getGesture')
def getGesture():
    return str(states.gesture)

@get('/getWaiting')
def getWaiting():
    return json.dumps(str(states.waitingToContinue))

@post('/setWaiting')
def setWaiting():
    states.waitingToContinue = json.loads(request.body.read())
    return 'cool'
