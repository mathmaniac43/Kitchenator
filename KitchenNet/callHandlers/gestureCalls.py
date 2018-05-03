from bottle import post, get, request
import json 

from . import states

'''
    All gesture related calls, updating the 'gesture' state in bottleService.py
'''
@post('/setGestureState')
def setGestureState():
    req_obj = json.loads(request.body.read())
    print(req_obj)
    states.gesture = req_obj#["gesture"]
    return 'gesture set to {}!'.format(states.gesture)

@get('/getGestureState')
def getGestureState():
    data = {}
    data['gesture'] = states.gesture
    jData = json.dumps(data)
    return jData