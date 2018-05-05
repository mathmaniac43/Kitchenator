from bottle import post, request, get
import json 

from . import states

'''
    All arm related calls, getting the arm states in bottleService.py
'''
@get('/getAllPoses')
def getAllPoses():
    data = {}
    if states.colorPoses:
        for p in states.colorPoses:
            data[p] = states.colorPoses[p]
    json_data = json.dumps(data)
    return json_data
    
@get('/getArmGoals')
def getArmGoals():
    data = {}
    data['armGoalState'] = states.armGoalState
    data['gripperState'] = states.gripperState
    if states.colorPoses and not states.goalIngredient == 'none':
        if states.armGoalState == 'deliver' or states.armGoalState == 'dump' or states.armGoalState == 'undump':
            data['armGoalColor'] = "orange"
        elif states.kitchenatorState == states.KSTATE.standby:
            print('TODO: Get standby color for arm')
            data['armGoalColor'] = "none"
        else:
            data['armGoalColor'] = states.ingredientColorMap[states.goalIngredient]
    else:
        data['armGoalPose'] = ""
        
    json_data = json.dumps(data)
    return json_data

@get('/getCurrentArmState')
def getCurrentArmState():
    data = {}
    data['currentArmState'] = states.currentArmState
    data['armLocation'] = states.armLocation
    json_data = json.dumps(data)
    return json_data

@post('/setCurrentArmState')
def setCurrentArmState():
    req_obj = json.loads(request.body.read())
    states.currentArmState = req_obj["state"]
    states.armLocation = req_obj["location"]
    print('Current Arm State:  {}'.format(states.currentArmState))
    