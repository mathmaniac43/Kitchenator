import httplib
import time
import json

starttime = time.time()
c = httplib.HTTPConnection('localhost', 8080)

gestRun = True
queryPeriod = 1
while gestRun:
    c.request('GET', '/getGoalIngredient')
    doc = c.getresponse().read()
    if doc != "none":
        ''' 
            Determine ingredient location here
        '''

        # c.request('SET', '/setGoalIngredientPos')
    
    time.sleep(queryPeriod - ((time.time() - starttime) % queryPeriod))