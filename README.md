# Kitchenator

* Kitchenator is powered by KitchenNet 

All software tested on MacOS Sierra Version 10.12.6

## Overview
The state is recorded and available on a server launched by `kitchennet.py`
The clients hook into this server and either update or check on the state by calling different HTTP methods
KitchenNet is (at least for now) the state manager

Information is passed between clients by updates to the state managed by KitchenNet.
All data is passed as JSON

### Gesture Client:
Updates the gesture state in KitchenNet 
Gesture JSON: 

`{"gesture": 1}`

### Arm Client:
Checks KitchenNet to see if it should be 'going' (and if so, where to), 'standby', or 'paused'
The arm client's GET request returns JSON of the form:
`{"armGoalPose": [x, y, pitch, yaw], "armGoalState": 'standby/paused/going'}`

### Vision Client:
Checks KitchenNet for a desired target, if so updates the target arm pose

### Voice Command Client:
COMIN REAL SOON
https://github.com/mozilla/DeepSpeech#using-the-python-package

### Visual User Interface:
Back-burner priority, but will display basic Kitchenator state information, error messages, or maybe debug information

## Dependencies:
* Python2
* bottle
* httplib (Python3 requires a switch to http.client)
* json


## Operation

In one terminal, run: 
> python KitchenNet/kitchennet.py

In another terminal, run:
> python theClients/gestureClient.py
This script will update the gesture every second

In another terminal, run:
> python theClients/testClient.py
This script will keep querying the current gesture and print out the result
