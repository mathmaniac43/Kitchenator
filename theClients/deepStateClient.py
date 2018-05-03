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
    print('getting state....')
    # try:
    c.request('GET', '/getState')
    doc = c.getresponse().read()
    d = json.loads(doc)
    print(doc)
    if d['state'] == "standby":
        if d['goalIngredient'] != 'none':
            print('Standby state, changing to seek for new ingredient...')
            data = {}
            data['nuState'] = 'seek'
            json_data = json.dumps(data)
            c.request('POST', '/setState', json_data)
            doc = c.getresponse().read()
        else:
            print('Standby state, no goal ingredient')
    elif d['state'] == "seek":
        print('Seek state, changing to \'standby\'')

        data = {}
        data['nuState'] = 'standby'
        json_data = json.dumps(data)
        c.request('POST', '/setState', json_data)
        doc = c.getresponse().read()

    time.sleep(delayTime - ((time.time() - starttime) % delayTime))
        



# 'All done'
