import httplib
import time
import json

starttime = time.time()
c = httplib.HTTPConnection('127.0.0.1', 8080)

gestRun = True
queryPeriod = 1
while gestRun:


        # c.request('SET', '/setGoalIngredientPos')
    
    time.sleep(queryPeriod - ((time.time() - starttime) % queryPeriod))