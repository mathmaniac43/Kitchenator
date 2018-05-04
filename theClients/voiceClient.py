import httplib
import time
import json
import pygame

from random import randint


'''
Connects to the KitchenNet server at localhost:8080
Supposedly starts listening when you hit 'Up Arrow'
FOR NOW it just generates a random ingredient and sends
that over the wire
'''
#pygame.init()
starttime = time.time()
c = httplib.HTTPConnection('127.0.0.1', 12345)

voiceRun = True
delayTime = 1.0
# while voiceRun:
    # events = pygame.event.get()
    # for event in events:
    #     if(event.type == pygame.KEYDOWN):
    #         if event.key == pygame.K_UP:

    #             print('updating goal ingredient....')
data = {}
#             diceRoll = randint(0,1)
#             goalIngredient = "none"
#             if diceRoll == 0:
#                 print('flour')
goalIngredient = "flour"
#             else:
#                 print('NUTMEEEEEEG')
#                 goalIngredient = "nutmeg" 
data['goalIngredient'] = goalIngredient
json_data = json.dumps(data)
c.request('POST', '/setGoalIngredient', json_data)
doc = c.getresponse().read()
    #             print doc
# time.sleep(delayTime - ((time.time() - starttime) % delayTime))