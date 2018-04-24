from bottle import post, request, get
import json 

from . import states

'''
    All vision related calls, updating the ???
'''
@get('/getGoalIngredient')
def getGoalIngredient():
    req_obj = json.loads(request.body.read())
    # print(req_obj)
    global goalPose
    goalPose = req_obj["goalPose"]
    return 'goalPose set to {}!'.format(goalPose)

