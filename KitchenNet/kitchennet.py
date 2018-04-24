import json
from bottle import run, post, request, response
from callHandlers import gestureCalls, stateCalls, visionCalls, armCalls, uiCalls

from callHandlers import states # states.py maintains all Kitchenator states

states.init()

ingredientOfInterest = 'none'

run(host='localhost', port=8080, debug=True)
