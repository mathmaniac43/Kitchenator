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

<<<<<<< HEAD
=======
# TODO: ('setGoalArmPosition')
>>>>>>> 5c23b260c076676a14c51ca81fda9ffd7143c569
