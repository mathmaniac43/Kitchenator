# Kitchenator

* Kitchenator is powered by KitchenNet 

All software tested on MacOS Sierra Version 10.12.6

## Overview
The state is recorded and available on a server launched by `kitchennet.py`
The clients hook into this server and either update or check on the state by calling different HTTP methods
KitchenNet proceeds through a number of different states during an ingredient cycle. The states are set by a State Manager Client.

Information is passed between clients by updates to the states held by KitchenNet.
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
For now, this client will set the goal ingredient at random from the available ingredients based on a keypress.
COMIN REAL SOON
https://github.com/mozilla/DeepSpeech#using-the-python-package

### Visual User Interface:
Access at localhost:8080/userInterface
Future will include 
## Dependencies:
* Python2
* bottle
* httplib (Python3 requires a switch to http.client)
* json
* pygame (for keyboard input to the voiceClient)


## Operation

In one terminal, run: 
> python KitchenNet/kitchennet.py

In another terminal, run:
> python theClients/deepStateClient.py

This script will check the state every 250 ms, and update from standby to seek if the goal ingredient is not 'none'

In another terminal, run:
> python theClients/voiceClient.py

This script will set the goal ingredient to 'nutmeg' or 'ketamine' when you press any key. Pygame is a little glitchy, so it stops taking key inputs when you click outside of the terminal in which voiceClient.py is running.
