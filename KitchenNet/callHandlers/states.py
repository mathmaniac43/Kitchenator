from enum import Enum
KSTATE = Enum('KSTATE', 'standby grab deliver return')


def init():

    ''' Kitchenator State '''
    global kitchenatorState
    kitchenatorState = KSTATE.standby

    ''' Arm State '''
    global armGoalState
    armGoalState = 'stop' # out of 'stop', 'go'
    global armGoalPose 
    armGoalPose = [0, 0, 0, 0] # x,y,pitch, yaw?

    '''
    Vision-related states
    '''
    global ingredientPos 
    ingredientPos = {'nutmeg': [0,0,0], 'ketamine': [0,0,0]}  # x,y,z
    
    global ingredientColorMap
    ingredientColorMap = {'nutmeg': 'blue', 'ketamine': 'orange'}

    global colorPoses
    colorPoses = { 'purple': {'x': 0, 'y': 0, 'z': 0, 'yaw': 0}, 'blue': {'x': 0, 'y': 0, 'z': 0, 'yaw': 0}, 'orange': {'x': 0, 'y': 0, 'z': 0, 'yaw': 0}}

    ''' Gesture State '''
    global gesture 
    gesture = 0


    ''' Goal Ingredient '''
    global goalIngredient
    goalIngredient = 'none'
