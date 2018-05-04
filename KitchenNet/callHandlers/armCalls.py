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
    data['armGoalPose'] = states.colorPoses[states.ingredientColorMap[states.goalIngredient]]
    json_data = json.dumps(data)
    return json_data