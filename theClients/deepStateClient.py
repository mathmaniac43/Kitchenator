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
while runState:
    print('evaluating state....')
    
    data = {}

    # Halt Gesture state beats all
    c.request('GET', '/getGestureState')
    doc = c.getresponse().read()
    d = json.loads(doc)
    if d['gesture'] == 2: # The halt gesture 
        # Setting standby state
        data['nuState'] = 'standby'
        json_data = json.dumps(data)
        c.request('POST', '/setState', json_data)
        doc = c.getresponse().read()
        continue

    # Assuming no halt, continue with the state machine
    # Get current state
    c.request('GET', '/getState')
    doc = c.getresponse().read()
    d = json.loads(doc)
    currentState = d['state']
    print('Current state is ' + currentState)

    if currentState == "standby":
        if d['goalIngredient'] != 'none':
            print('Standby state, changing to \'grab\' for new ingredient...')
            data['nuState'] = 'grab'
            json_data = json.dumps(data)
            c.request('POST', '/setState', json_data)
            doc = c.getresponse().read()
        else:
            print('Standby state, no goal ingredient')
    elif currentState == "grab":
        data['armGoalState'] = 'go'
        data['gripperState'] = 'open'
        json_data = json.dumps(data)
        c.request('POST', '/setArmGoalState', json_data)
        doc = c.getresponse().read()

    elif currentState == "deliver":
        print("Deliver state")

    elif currentState == "return":
        print("Return state")
    else:
        print("INVALID SYSTEM STATE, setting to standby")
        data['nuState'] = 'standby'
        json_data = json.dumps(data)
        c.request('POST', '/setState', json_data)
        doc = c.getresponse().read()


    time.sleep(delayTime - ((time.time() - starttime) % delayTime))
        



# 'All done'
