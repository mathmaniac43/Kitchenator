import httplib
import time
import json

starttime = time.time()
c = httplib.HTTPConnection('localhost', 8080)

gestRun = True
while gestRun:
    c.request('POST', '/getGestureState', '{}')
    doc = c.getresponse().read()
    print doc
    time.sleep(2.0 - ((time.time() - starttime) % 2.0))


# 'All done'
