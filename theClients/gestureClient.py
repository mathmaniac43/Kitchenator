import httplib
import time
import json


'''
Connects to the KitchenNet server at localhost:8080
updates the gesture there every second by posting to '/setGestureState'
'''

starttime = time.time()
c = httplib.HTTPConnection('localhost', 8080)

gestRun = True
delayTime = 1.0
while gestRun:
    print('updating gesture....')
    data = {}
    data['gesture'] = time.time() - starttime;
    json_data = json.dumps(data)# = '{"gesture": {}}'.format(time.time())
    c.request('POST', '/setGestureState', json_data)
    doc = c.getresponse().read()
    print doc
    time.sleep(delayTime - ((time.time() - starttime) % delayTime))


# 'All done'
