from bottle import post, request, get
import json 

from . import states

'''
    All state related calls, updating the 'gesture' state in bottleService.py
'''

# Function for translating state json to KSTATE
def translateState(x):
    return {
        'standby': states.KSTATE.standby,
        'seek': states.KSTATE.seek,
    }[x]

@post('/setState')
def setMode():
    req_obj = json.loads(request.body.read())
    # print(req_obj)
    states.kitchenatorState = translateState(req_obj["nuState"])
    print('New State set to {}'.format(states.kitchenatorState))
    return 'mode set to {}!'.format(states.kitchenatorState)

@get('/getState')
def getMode():
    return '{}'.format(states.kitchenatorState)