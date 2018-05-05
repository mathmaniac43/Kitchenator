import httplib
import time
import json

from random import randint


'''
Connects to the KitchenNet server at localhost:8080
updates the goal ingredient when a user types it in 
'''

starttime = time.time()
c = httplib.HTTPConnection('127.0.0.1', 12345)

gestRun = True
delayTime = 1.0
while gestRun:
    goalIngredient = raw_input("Enter goal ingredient...")
    data = {}
    data['goalIngredient'] = goalIngredient;
    json_data = json.dumps(data)
    c.request('POST', '/setGoalIngredient', json_data)
    doc = c.getresponse().read()
    print doc
    time.sleep(delayTime - ((time.time() - starttime) % delayTime))


# 'All done'
