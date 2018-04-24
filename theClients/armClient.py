import httplib
import time
import json

'''
 The Arm Manager/Client:

 -> Queries the state, if state is 'delivering' then query goalPos 
    (or maybe get it all as one json chunk)
 -> Start moving along waypoints, calling to query the state along the way??
 -> if state is 'delivering' & gesture = $StopGesture then pause, keep waiting for instructions
 -> etc, etc


'''

starttime = time.time()
c = httplib.HTTPConnection('localhost', 8080)

armRun = True
delayTime = 0.25
while armRun:
    print('checking state at %f....' % (time.time() - starttime))
    c.request('GET', '/getArmGoals')
    doc = c.getresponse().read()
    print doc
    time.sleep(delayTime - ((time.time() - starttime) % delayTime))
