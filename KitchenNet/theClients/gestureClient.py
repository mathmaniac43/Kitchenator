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
while gestRun:
    print('updating gesture....')
    data = {}
    data['gesture'] = time.time() - starttime;
    json_data = json.dumps(data)# = '{"gesture": {}}'.format(time.time())
    c.request('POST', '/setGestureState', json_data)
    doc = c.getresponse().read()
    print doc
    time.sleep(1.0 - ((time.time() - starttime) % 1.0))


# 'All done'
