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
    global armGoalState
    armGoalState = 'stop' # out of 'stop', 'go', 'dump', 'undump'

    global currentArmState
    currentArmState = 'idle' # out of 'idle', 'plan', 'move'

    global armGoalPose 
    armGoalPose = [0, 0, 0, 0] # x,y,pitch, yaw?

    global gripperState
    gripperState = "open"

    '''
    Vision-related states
    '''    
    global ingredientColorMap
    ingredientColorMap = {'nutmeg': 'blue', 'flour': 'purple'}

    global colorPoses
    colorPoses = None

    ''' Gesture State '''
    global gesture 
    gesture = 0


    ''' Goal Ingredient '''
    global goalIngredient
    goalIngredient = 'none'
