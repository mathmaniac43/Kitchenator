from bottle import post, request, get
import json 

from . import states

'''
    All state related calls, updating the 'gesture' state in bottleService.py
'''

# Function for translating state json to KSTATE
def string2State(x):
    return {
        'standby': states.KSTATE.standby,
        'grab': states.KSTATE.grab,
        'deliver': states.KSTATE.deliver,
        'rehome': states.KSTATE.rehome
    }[x]

def state2String(x):
    return {
        states.KSTATE.standby : 'standby',
        states.KSTATE.grab : 'grab',
        states.KSTATE.deliver: 'deliver',
        states.KSTATE.rehome: 'rehome'
    }[x]

@post('/setState')
def setMode():
    req_obj = json.loads(request.body.read())
    # print(req_obj)
    states.kitchenatorState = string2State(req_obj["nuState"])
    print('New State set to {}'.format(states.kitchenatorState))
    return 'mode set to {}!'.format(states.kitchenatorState)

@get('/getState')
def getMode():
    data = {}
    data['state'] = state2String(states.kitchenatorState)
    data['goalIngredient'] = states.goalIngredient
    jData = json.dumps(data)
    return jData

@post('/setArmGoalState')
def setArmGoalState():
    req_obj = json.loads(request.body.read())
    # states.armGoalState = req_obj["armGoalState"]
    states.gripperState = req_obj["gripperState"]