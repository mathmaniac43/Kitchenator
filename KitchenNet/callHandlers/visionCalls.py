from bottle import post, request
import json 


'''
    All vision related calls, updating the ???
'''
@post('/setGoalPose')
def setGoalPose():
    req_obj = json.loads(request.body.read())
    # print(req_obj)
    global goalPose
    goalPose = req_obj["goalPose"]
    return 'goalPose set to {}!'.format(goalPose)

@post('/getGoalPose')
def getGoalPose():
    return 'goal pose is {}!'.format(goalPose)