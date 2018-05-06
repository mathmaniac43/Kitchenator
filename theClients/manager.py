import httplib
import time
import json

'''
Connects to the KitchenNet server at localhost:8080
Checks and updates the state based on available information
For further information, find the state diagram for the Kitchenator
'''

delayTime = 1.0

starttime = time.time()
client = httplib.HTTPConnection('192.168.0.10', 12345)

    
def post(client, endpoint, value):
    print 'setting %s to %s' % (endpoint, value)
    json_data = json.dumps(value)
    client.request('POST', '/%s' % endpoint, json_data)
    return client.getresponse().read()
    
def get(client, endpoint):
    client.request('GET', '/%s' % endpoint)
    doc = client.getresponse().read()
    return json.loads(doc)

    
    
while True:
    print ''
    
    time.sleep(delayTime - ((time.time() - starttime) % delayTime))

    gesture = get(client, 'getGesture')
    if gesture == 2:
        post(client, 'setArmStopGo', 'stop')
    elif gesture == 1:
        post(client, 'setArmStopGo', 'go')
        post(client, 'setWaiting', 'False')
    
    if gesture != 0:
        initial_gesture = gesture
        while gesture == initial_gesture:
            print 'Waiting for gesture to end...'
            time.sleep(0.1)
            gesture = get(client, 'getGesture')
        continue

    arm_status = get(client, 'getArmCurrentStatus')
    print(arm_status)
    if arm_status['stopgo'] == 'stop':
        print 'Arm stopped, awaiting "go" command.'
        
    waiting = get(client, 'getWaiting')
    print 'Waiting? %s' % waiting
    if waiting == 'True':
        print 'Currently waiting for "go" command.'
        continue
    
    targetState = arm_status['targetState']
    if targetState == arm_status['currentState']:
        
        # Proceed from current target state to next
        if targetState == 'standby':
            all_poses = get(client, 'getAllPoses')
            if len(all_poses) > 0:
                post(client, 'setArmTargetState', 'planning')
            else:
                print 'Awaiting vision system positions.'
        
        elif targetState == 'planning':
            post(client, 'setArmTargetState', 'grab')
        
        elif targetState == 'grab':
            post(client, 'setArmTargetState', 'pre_dump')
        
        elif targetState == 'pre_dump':
            post(client, 'setArmTargetState', 'dump')
        
        elif targetState == 'dump':
            post(client, 'setArmTargetState', 'standby')
            post(client, 'setGoalIngredient', 'invalid')
            
    else: # manager is waiting for arm to catch up to target.
    
        print 'Waiting for arm to proceed.'
        
        if targetState == 'grab' or targetState == 'pre_dump':
            post(client, 'setWaiting', 'True')
