from bottle import post, request
import json 

from . import states

'''
    All gesture related calls, updating the 'gesture' state in bottleService.py
'''
@post('/setGestureState')
def setGestureState():
    req_obj = json.loads(request.body.read())
    states.gesture = req_obj["gesture"]
    return 'gesture set to {}!'.format(states.gesture)

@post('/getGestureState')
def getGestureState():
    return 'gesture is {}!'.format(states.gesture)