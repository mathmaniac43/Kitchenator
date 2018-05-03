from bottle import post, request, get
import json 

from . import states

'''
    All vision related calls, updating the ???
'''
@get('/getGoalIngredient')
def getGoalColor():
    data = {}
    data['goalIngredient'] = states.goalIngredient
    json_data = json.dumps(data)
    return json_data

@post('/setColorPoses')
def setColorPoses():
    print('setting color poses')
    req_obj = json.loads(request.body.read())
    print(req_obj)
    states.colorPoses = req_obj#["gesture"]

