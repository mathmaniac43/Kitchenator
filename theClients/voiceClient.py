import httplib
import time
import json

from random import randint


'''
Connects to the KitchenNet server at localhost:8080
updates the gesture there every second by posting to '/setGestureState'
'''

starttime = time.time()
c = httplib.HTTPConnection('127.0.0.1', 8000)

gestRun = True
delayTime = 10.0
while gestRun:
    print('updating goal ingredient....')
    data = {}
    diceRoll = randint(0,1)
    goalIngredient = "none"
    if diceRoll == 0:
        goalIngredient = "ketamine"
    else:
        goalIngredient = "nutmeg" 
    data['goalIngredient'] = goalIngredient
    json_data = json.dumps(data)
    c.request('POST', '/setGoalIngredient', json_data)
    doc = c.getresponse().read()
    print doc
    time.sleep(delayTime - ((time.time() - starttime) % delayTime))