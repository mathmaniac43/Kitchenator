import json
from bottle import run
from callHandlers import gestureCalls, stateCalls, visionCalls, armCalls, uiCalls, voiceCalls

from callHandlers import states # states.py maintains all Kitchenator states

print 'start'
states.init()

run(host='127.0.0.1', port=12346, debug=True, reloader=True)

