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
    
@get('/getArmCurrentStatus')
def getArmCurrentStatus():
    data = {}
    data['targetState']  = states.armTargetState
    data['currentState'] = states.armCurrentState
    data['stopgo']       = states.armStopGo
    data['color']        = states.ingredientColorMap[states.goalIngredient]
    
    json_data = json.dumps(data)
    return json_data

@post('/setArmCurrentState')
def setArmCurrentState():
    states.armCurrentState = json.loads(request.body.read())
    return 'cool'

@post('/setArmTargetState')
def setArmTargetState():
    states.armTargetState = json.loads(request.body.read())
    return 'cool'

@post('/setArmStopGo')
def setArmStopGo():
    states.armStopGo = json.loads(request.body.read())
    return 'cool'
