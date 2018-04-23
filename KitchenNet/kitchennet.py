import json

from bottle import run, post, request, response

from callHandlers import gestureCalls, stateCalls, visionCalls, armCalls, uiCalls


run(host='localhost', port=8080, debug=True)
