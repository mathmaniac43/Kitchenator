from bottle import post, request, get
import json 

from . import states

'''
    All vision related calls, updating the ???
'''
@get('/getGoalIngredient')
def getGoalIngredient():
    data = {}
    data['goalIngredient'] = states.goalIngredient
    json_data = json.dumps(data)
    return json_data

