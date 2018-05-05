import httplib
import time
import json

from random import randint


'''
Connects to the KitchenNet server at localhost:8080
updates the gesture there every second by posting to '/setGestureState'
'''

starttime = time.time()
c = httplib.HTTPConnection('127.0.0.1', 12345)

armRun = True
delayTime = 1.0
while armRun:
    armState = raw_input("Enter arm state (move/idle/plan)...")
    data = {}
    data['state'] = armState;
    json_data = json.dumps(data)
    c.request('POST', '/setCurrentArmState', json_data)
    doc = c.getresponse().read()
    print doc
    time.sleep(delayTime - ((time.time() - starttime) % delayTime))


# 'All done'
