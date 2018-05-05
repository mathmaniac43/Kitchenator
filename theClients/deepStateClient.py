import httplib
import time
import json


'''
Connects to the KitchenNet server at localhost:8080
Checks and updates the state based on available information
For further information, find the state diagram for the Kitchenator
'''

starttime = time.time()
c = httplib.HTTPConnection('127.0.0.1', 12345)

runState = True
delayTime = 1.0

armGoingToPickupIngredient = False
armGoingToDeliver = False
armGoingToDump = False
armGoingToUndump = False
atSomePointTheArmMoved = False 
armGoingToReturnIngredient = False
armGoingToReleaseIngredient = False
armReturningToStandbyConfiguration = False

def setKState(client, newState):
    data = {}
    data['nuState'] = newState
    json_data = json.dumps(data)
    client.request('POST', '/setState', json_data)
    c.getresponse().read()

def setArmGoalState(client, armGoalState, gripperState):
    data = {}
    data['armGoalState'] = armGoalState
    data['gripperState'] = gripperState
    json_data = json.dumps(data)
    c.request('POST', '/setArmGoalState', json_data)
    doc = c.getresponse().read()

while runState:

    data = {}

    # Halt Gesture state beats all
    c.request('GET', '/getGestureState')
    doc = c.getresponse().read()
    d = json.loads(doc)
    if d['gesture'] == 2: # The halt gesture 
        print('Halt gesture detected, setting to standby, stopping arm')
        # Setting standby state
        setKState(c, 'standby')
        # Stopping arm
        setArmGoalState(c, 'stop', 'open')
        continue

    # Assuming no halt, continue with the state machine
    # Get current state
    c.request('GET', '/getState')
    doc = c.getresponse().read()
    d = json.loads(doc)
    currentState = d['state']
    print('Current state is ' + currentState)

    if currentState == "standby":
        print('Standby State')
        if not armReturningToStandbyConfiguration:
            if d['goalIngredient'] != 'none':
                print('Standby state, changing to \'grab\' for new ingredient...')
                setKState(c, 'grab')
            else:
                print('Standby state, no goal ingredient')
        else:
            print('Returning to standby configuration')
            # Get current arm state (idle/plan/move)
            c.request('GET', '/getCurrentArmState')
            doc = c.getresponse().read()
            d = json.loads(doc)
            if d['currentArmState'] == 'move':
                atSomePointTheArmMoved = True
            elif d['currentArmState'] == 'idle' and atSomePointTheArmMoved:
                print('Arm reached standby configuration')
                # Stop the arm, it's returned to standby mode
                setArmGoalState(c, 'stop', 'open')
                armReturningToStandbyConfiguration = False

    elif currentState == "grab":
        print('Grab State')
        if not armGoingToPickupIngredient:
            print('Telling arm to go pick up ingredient')
            setArmGoalState(c, 'go', 'close')
            armGoingToPickupIngredient = True
        elif armGoingToPickupIngredient:
            # Get current arm state (idle/plan/move)
            print('Arm is going to pick up ingredient')
            c.request('GET', '/getCurrentArmState')
            doc = c.getresponse().read()
            d = json.loads(doc)
            if d['currentArmState'] == 'move':
                atSomePointTheArmMoved = True
            elif d['currentArmState'] == 'idle' and atSomePointTheArmMoved:
                # Gripper should be closed on cup handle now,
                # set Kitchenator state to deliver
                setKState(c, 'deliver')
                atSomePointTheArmMoved = False
                armGoingToPickupIngredient = False
                continue

    elif currentState == "deliver":
        print("Deliver State")
        if not armGoingToDeliver and not armGoingToDump:
            # Direct arm to pick up the goal ingredient
            setArmGoalState(c, 'go', 'close')
            armGoingToDeliver = True
        elif armGoingToDeliver and not armGoingToDump:
            # Get current arm state (idle/plan/move)
            c.request('GET', '/getCurrentArmState')
            doc = c.getresponse().read()
            d = json.loads(doc)
            if d['currentArmState'] == 'move':
                atSomePointTheArmMoved = True
            elif d['currentArmState'] == 'idle' and atSomePointTheArmMoved:
                # Gripper should be closed on cup handle now,
                # set arm goal to dump
                atSomePointTheArmMoved = False
                setArmGoalState(c, 'dump', 'close')

                armGoingToDump = True
                armGoingToDeliver = False
                # Wait a damn second
                time.sleep(delayTime - ((time.time() - starttime) % delayTime))
                continue
        elif armGoingToDump:
            # Get current arm state (idle/plan/move)
            c.request('GET', '/getCurrentArmState')
            doc = c.getresponse().read()
            d = json.loads(doc)
            if d['currentArmState'] == 'move':
                atSomePointTheArmMoved = True
            elif d['currentArmState'] == 'idle' and atSomePointTheArmMoved:
                print('arm completed dump')
                armGoingToDump = False
                armGoingToUndump = True
                atSomePointTheArmMoved = False
                data = {}
                setArmGoalState(c, 'undump', 'close')
        elif armGoingToUndump:
            # Get current arm state (idle/plan/move)
            c.request('GET', '/getCurrentArmState')
            doc = c.getresponse().read()
            d = json.loads(doc)
            if d['currentArmState'] == 'move':
                atSomePointTheArmMoved = True
            elif d['currentArmState'] == 'idle' and atSomePointTheArmMoved:
                print('arm completed un-dump')
                armGoingToUndump = False
                armGoingToReturnIngredient = True
                atSomePointTheArmMoved = False
                # set Kitchenator state to rehome / return home
                setKState(c, 'rehome')
    elif currentState == "rehome":
        print("Rehome state")
        if not armGoingToReturnIngredient:
            setArmGoalState(c, 'go', 'close')
            armGoingToReturnIngredient = True
        elif not armGoingToReleaseIngredient:
            # Get current arm state (idle/plan/move)
            c.request('GET', '/getCurrentArmState')
            doc = c.getresponse().read()
            d = json.loads(doc)
            if d['currentArmState'] == 'move':
                atSomePointTheArmMoved = True
            elif d['currentArmState'] == 'idle' and atSomePointTheArmMoved:
                print('arm completed ingredient return')
                atSomePointTheArmMoved = False
                # set arm to release ingredient
                setArmGoalState(c, 'go', 'open')
                armGoingToReturnIngredient = True
                
        elif armGoingToReleaseIngredient:
            # Get current arm state (idle/plan/move)
            c.request('GET', '/getCurrentArmState')
            doc = c.getresponse().read()
            d = json.loads(doc)
            if d['currentArmState'] == 'move':
                atSomePointTheArmMoved = True
            elif d['currentArmState'] == 'idle' and atSomePointTheArmMoved:
                print('arm completed ingredient return')
                atSomePointTheArmMoved = False
                # set Kitchenator state to standby
                setKState(c, 'standby')

                # Set arm to move to standby position
                setArmGoalState(c, 'go', 'open')
                armReturningToStandbyConfiguration = True
    else:
        print("INVALID SYSTEM STATE, setting to standby")
        setKState(c, 'standby')


    time.sleep(delayTime - ((time.time() - starttime) % delayTime))
        



# 'All done'
