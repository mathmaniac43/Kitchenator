import json
from bottle import run
from callHandlers import gestureCalls, stateCalls, visionCalls, armCalls, uiCalls, voiceCalls

from callHandlers import states # states.py maintains all Kitchenator states

states.init()

colorOfInterest = 'none'

run(host='127.0.0.1', port=12345, debug=True, reloader=True)

