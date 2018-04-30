import httplib
import time
import json


'''
Connects to the KitchenNet server at localhost:8080
Checks and updates the state based on available information
For further information, find the state diagram for the Kitchenator
'''

starttime = time.time()
c = httplib.HTTPConnection('127.0.0.1', 8080)

runState = True
delayTime = 1.0
while runState:
    print('updating gesture....')
    data = {}
    data['gesture'] = randint(0,2);
    json_data = json.dumps(data)
    c.request('POST', '/setGestureState', json_data)
    doc = c.getresponse().read()
    print doc
    time.sleep(delayTime - ((time.time() - starttime) % delayTime))


# 'All done'
