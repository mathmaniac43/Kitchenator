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
    print('getting state....')
    try:
        c.request('GET', '/getState')
    except Exception, e:
        print('failed get')
    doc = c.getresponse().read()
    if doc == "KSTATE.standby":
        print('Standby state, changing to seek')
        data = {}
        data['nuState'] = 'seek'
        json_data = json.dumps(data)
        c.request('POST', '/setState', json_data)
        # doc = c.getresponse().read()
    elif doc == "KSTATE.seek":
        print('Seek state, changing to \'standby\'')

        data = {}
        data['nuState'] = 'standby'
        json_data = json.dumps(data)
        c.request('POST', '/setState', json_data)
        # doc = c.getresponse().read()

    time.sleep(delayTime - ((time.time() - starttime) % delayTime))
        



# 'All done'
