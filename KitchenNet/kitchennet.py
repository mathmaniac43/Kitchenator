import json
from bottle import run, post, request, response
from callHandlers import gestureCalls, stateCalls, visionCalls, armCalls, uiCalls, voiceCalls

from callHandlers import states # states.py maintains all Kitchenator states

states.init()

colorOfInterest = 'none'

run(host='127.0.0.1', port=8080, debug=True)

