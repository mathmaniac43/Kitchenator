import httplib
import time
import json

from random import randint


'''
Connects to the KitchenNet server at localhost:8080
updates the gesture there every second by posting to '/setGestureState'
'''

starttime = time.time()
c = httplib.HTTPConnection('127.0.0.1', 8080)

gestRun = True
delayTime = 1.0
while gestRun:
    print('updating gesture....')
    data = {}
    data['gesture'] = randint(0,2);
    json_data = json.dumps(data)
    c.request('POST', '/setGestureState', json_data)
    doc = c.getresponse().read()
    print doc
    time.sleep(delayTime - ((time.time() - starttime) % delayTime))


# 'All done'
