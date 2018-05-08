from enum import Enum

WORKING = True

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
    #colorPoses = None
    colorPoses = {"blue" : { "x" : -0.4, "y" : 0.301, "z" : 0.09, "yaw" : 1.88 }, "purple" : { "x" : 0.52, "y" : 0.3, "z" : 0.09, "yaw" : 0.716 }, "orange" : {"x" : -0.0, "y" : 0.421, "z" : 0.09, "yaw" : 1.88 }}

    ''' Gesture State '''
    global gesture 
    gesture = 0


    ''' Goal Ingredient '''
    global goalIngredient
    goalIngredient = ''
