import httplib 
import json

client = httplib.HTTPConnection('127.0.0.1', 12346)

    
def post(client, endpoint, value):
    print 'setting %s to %s' % (endpoint, value)
    json_data = json.dumps(value)
    client.request('POST', '/%s' % endpoint, json_data)
    return client.getresponse().read()




'''
Connects to the KitchenNet server at localhost:12346
Sets value at any endpoint to any value
'''

c = httplib.HTTPConnection('127.0.0.1', 12346)

gestRun = True
delayTime = 1.0
while gestRun:
    endPt = raw_input("Enter Endpoint...")
    value = raw_input("Enter value...")
    post(c, endPt, value)
    