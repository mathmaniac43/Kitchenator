from bottle import post, request, get
import json 

from . import states

'''
    All arm related calls, getting the arm states in bottleService.py
'''
@get('/getArmGoals')
def getArmGoals():
    data = {}
    data['armGoalState'] = states.armGoalState
    if states.kitchenatorState == states.KSTATE.deliver:
        data['armGoalPose'] = states.colorPoses['orange'] # Bowl is always ORANGE
    else:
        data['armGoalPose'] = states.colorPoses[states.ingredientColorMap[states.goalIngredient]]
    json_data = json.dumps(data)
    return json_data

@get('/getCurrentArmState')
def getCurrentArmState():
    data = {}
    data['currentArmState'] = states.currentArmState
    json_data = json.dumps(data)
    return json_data

@post('/setCurrentArmState')
def setCurrentArmState():
    req_obj = json.loads(request.body.read())
    states.currentArmState = req_obj["state"]
    print('Current Arm State:  {}'.format(states.currentArmState))
    