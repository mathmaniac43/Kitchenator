import json

from bottle import run, post, request, response

from callHandlers import gestureCalls, stateCalls, visionCalls, armCalls


''' Arm State '''
goalPose = [0,0,0,0,0,0]
armState = 'standy'


run(host='localhost', port=8080, debug=True)