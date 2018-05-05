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
armGoingToReturnIngredient = False
armGoingToReleaseIngredient = False
armReturningToStandbyConfiguration = False

def setKState(client, newState):
    data = {}
    data['nuState'] = newState
    json_data = json.dumps(data)
    client.request('POST', '/setState', json_data)
    client.getresponse().read()

def setArmGoalState(client, armGoalState, gripperState):
    data = {}
    data['armGoalState'] = armGoalState
    data['gripperState'] = gripperState
    json_data = json.dumps(data)
    client.request('POST', '/setArmGoalState', json_data)
    doc = client.getresponse().read()

currentGesture = 0
while runState:

    data = {}

    # Halt Gesture state beats all
    c.request('GET', '/getGestureState')
    doc = c.getresponse().read()
    d = json.loads(doc)
    print(d)
    
    if d[u'gesture'] is not 0:
        currentGesture = d[u'gesture']
        
    print(currentGesture)
    if currentGesture == 2: # The halt gesture 
        print('Halt gesture detected, setting to standby, stopping arm')
        # Setting standby state
        #setKState(c, 'standby')
        # Stopping arm
        setArmGoalState(c, 'stop', 'same')
        time.sleep(delayTime - ((time.time() - starttime) % delayTime))

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
        if d['goalIngredient'] != 'none':
            print('Standby state, changing to \'grab\' for new ingredient...')
            setKState(c, 'grab')
        else:
            print('Standby state, no goal ingredient')
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
            if d['armLocation'] == 'landingpad':
                setKState(c, 'deliver')
                armGoingToPickupIngredient = False
                continue
    elif currentState == "deliver":
        print("Deliver State")
        if not armGoingToDeliver and not armGoingToDump and not armGoingToUndump:
            # Direct arm to pick up the goal ingredient
            setArmGoalState(c, 'go', 'close')
            armGoingToDeliver = True
        elif armGoingToDeliver and not armGoingToDump and not armGoingToUndump:
            # Get current arm state (idle/plan/move)
            c.request('GET', '/getCurrentArmState')
            doc = c.getresponse().read()
            d = json.loads(doc)
            if d['armLocation'] == 'bowl':
                # Arm should be at bowl now, check gesture 
                if currentGesture == 1:
                    # set arm goal to dump
                    setArmGoalState(c, 'dump', 'close')
                    armGoingToDump = True
                    armGoingToDeliver = False
                    continue
                else:
                    print('Awaiting continue gesture .... ')
        elif armGoingToDump:
            print("armGoingToDump")
            # Get current arm state (idle/plan/move)
            c.request('GET', '/getCurrentArmState')
            doc = c.getresponse().read()
            d = json.loads(doc)
            print(d)
            if d['armLocation'] == 'bowl_dump':
                print('arm completed dump')
                armGoingToDump = False
                armGoingToUndump = True
                setArmGoalState(c, 'undump', 'close')
        elif armGoingToUndump:
            print("arm going to undump")
            # Note: undump is really undump - return ingredient - go to standby mode
            # Get current arm state (idle/plan/move)
            c.request('GET', '/getCurrentArmState')
            doc = c.getresponse().read()
            d = json.loads(doc)
            print(d)
            if d['armLocation'] == 'standby':
                print('arm completed un-dump')
                armGoingToUndump = False
                armGoingToReturnIngredient = True
                # set Kitchenator state to standby
                armReturningToStandbyConfiguration = True

                # Set goal ingredient to "none"
                print("mission accomplished!")
                data = {}
                data['goalIngredient'] = "none"
                json_data = json.dumps(data)
                c.request('POST', '/setGoalIngredient', json_data)
                c.getresponse().read()

                setKState(c, 'standby')
            else:
                print("Arm is returning ingredient, returning to standby")
    else:
        print("INVALID SYSTEM STATE, setting to standby")
        setKState(c, 'standby')


    time.sleep(delayTime - ((time.time() - starttime) % delayTime))
        



# 'All done'
