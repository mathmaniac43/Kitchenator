from enum import Enum
KSTATE = Enum('KSTATE', 'standby seek deliver return')


def init():

    ''' Kitchenator State '''
    global kitchenatorState
    kitchenatorState = KSTATE.standby




    ''' Arm State '''
    global armGoalState
    armGoalState = 'standby' # out of 'standby', 'go', 'pause'
    global armGoalPose 
    armGoalPose = [0, 0, 0, 0] # x,y,pitch, yaw?


    '''
    Vision-related states
    '''
    global ingredientPos 
    ingredientPos = {'nutmeg': [0,0,0], 'ketamine': [0,0,0]}  # x,y,z
    
    global ingredientColorMap
    ingredientColorMap = {'nutmeg': 'blue', 'ketamine': 'orange'}

    ''' Gesture State '''
    global gesture 
    gesture = 0


    ''' Goal Ingredient '''
    global goalIngredient
    goalIngredient = 'none'
