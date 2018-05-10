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
This MATLAB client listens on a button press and performs a cross-correlation against the known ingredients. It assigns the closest match to the user's speech as the goal ingredient.
https://github.com/mozilla/DeepSpeech#using-the-python-package

### Visual User Interface:
Access at 127.0.0.1:12346/userInterface
Access debug screen at 127.0.0.1:12346/uiDebug
Future will include 
## Dependencies:
* Python2
* bottle
* httplib (Python3 requires a switch to http.client)
* json


## Operation

In one terminal, run: 
> python KitchenNet/kitchennet.py
NOTE: If there are errors relating to the 'Enum' class, go to KitchenNet/callHandlers/states.py and change 'WORKING' from True to False (or vice versa)

In separate terminals, run:
> python theClients/manager.py
> python vision/k_webcam_shapes.py
Note: You need the orange/black - green/black - purple/black color tags displayed for this client to begin transmitting data to the server

In separate MATLAB instances, run:
> Myo/MyoGestureDetection.m

and 

> theClients/voiceClient

and 

> RobotArm/run_arm3



Locate the MATLAB window spawned by voice client, click on it, speak the ingredient ("nutmeg" or "flour"), and then sit back and watch the magic happen.


### States that the arm client can receive:
#### Color Poses from GET /getAllPoses

{
    {"purple": 
        {'x': 0, 'y': 0, 'z': 0, 'yaw': 0}
    },
    {"orange": 
        {'x': 0, 'y': 0, 'z': 0, 'yaw': 0}
    },
    {"blue": 
        {'x': 0, 'y': 0, 'z': 0, 'yaw': 0}
    }
}

#### Arm Goal States from GET /getArmGoals

{
    {"armGoalState": "go"/"stop"/"dump"/"undump" },
    {"gripperState": "open"/"close"/"same"},
    {"armGoalColor":
    "purple"/"orange"/"blue"}
}

