from enum import Enum

WORKING = False

if WORKING:
    KSTATE = Enum('standby', 'grab', 'deliver', 'rehome')
else:
    KSTATE = Enum('KSTATE', 'standby grab deliver rehome')


def init():

    ''' Kitchenator State '''
    global kitchenatorState
    kitchenatorState = KSTATE.standby

    ''' Arm State '''
    
    global armTargetState
    armTargetState = "standby"
    
    global armCurrentState
    armCurrentState = "standby"
    
    global armStopGo
    armStopGo = "go"
    
    global waitingToContinue
    waitingToContinue = 'False'

    '''
    Vision-related states
    '''    
    global ingredientColorMap
    ingredientColorMap = {'nutmeg': 'blue', 'flour': 'purple', '':'', 'invalid':''}

    global colorPoses
    colorPoses = None

    ''' Gesture State '''
    global gesture 
    gesture = 0


    ''' Goal Ingredient '''
    global goalIngredient
    goalIngredient = ''
