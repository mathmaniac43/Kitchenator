import httplib
import time
import json

starttime = time.time()
c = httplib.HTTPConnection('localhost', 8080)

gestRun = True
queryPeriod = 1.5;
while gestRun:
    c.request('POST', '/getGoalIngredient', '{}')
    doc = c.getresponse().read()
    print doc
    time.sleep(queryPeriod - ((time.time() - starttime) % queryPeriod))