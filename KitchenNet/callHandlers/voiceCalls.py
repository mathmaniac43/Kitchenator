from bottle import post, request
import json 

from . import states

'''
    All user-voice-order related calls, updating the 'goalIngredient' state in states.py
'''
@post('/setGoalIngredient')
def setGoalIngredient():
    states.goalIngredient = json.loads(request.body.read())
