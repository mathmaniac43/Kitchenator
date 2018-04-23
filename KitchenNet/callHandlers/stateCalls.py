from bottle import post, request
import json 

''' Kitchenator State '''
mode = 'standby'

'''
    All state related calls, updating the 'gesture' state in bottleService.py
'''
@post('/setMode')
def setMode():
    req_obj = json.loads(request.body.read())
    # print(req_obj)
    global mode
    mode = req_obj["mode"]
    return 'mode set to {}!'.format(mode)

@post('/getMode')
def getMode():
    return 'mode is {}!'.format(mode)