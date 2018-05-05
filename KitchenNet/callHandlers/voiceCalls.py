from bottle import post, request
import json 

from . import states

'''
    All user-voice-order related calls, updating the 'goalIngredient' state in states.py
'''
@post('/setGoalIngredient')
def setGoalIngredient():
    states.goalIngredient = request.body.read()
    print("K I T C H E N A T O R activate!")
    return 'goal ingredient set to {}!'.format(states.goalIngredient)
    