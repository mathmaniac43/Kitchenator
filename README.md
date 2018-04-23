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
Checks KitchenNet to see if it should be 'going somewhere' (and if so, where to), at rest, or paused

### Vision Client:
Checks KitchenNet for a desired target, if so updates the target arm pose

### Voice Command Client:
COMIN REAL SOON

### Visual User Interface:
Back-burner priority, but will display basic Kitchenator state information, error messages, or maybe debug information

## Dependencies:
* Python2
* bottle
* httplib (Python3 requires a switch to http.client)
* json


## Operation

In one terminal, run: 
> python kitchennet.py

In another terminal, run:
> python gestureClient.py

In yet another terminal, run:
> python armClient.py

... and so on until all your clients are active