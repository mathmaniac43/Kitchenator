# Kitchenator

* Kitchenator is powered by KitchenNet *

Requirements: Python 3.6, VirtualEnv

All software tested on MacOS Sierra Version 10.12.6

Kitchenator is a Django framework for serving up the Kitchenator UI and maintaining python processes running all the hardware

## Installation: (bear with me here)

Clone this repo.
Then run:
> cd Kitchenator
> virtualenv venv -p python3

This will create a VirtualEnv directory 'venv'
From this directory, run:
> source venv/bin/activate

This will set up your VirtualEnv
You should see the prefix (venv) in your command terminal
(To exit this virtual environment, type 'deactivate')

With your VirtualEnv activated, perform the following:
>pip install django


## Running the Server
With virtualenv activated,
Run:
>python manage.py runserver

You can view the current interface in a web browser at http://127.0.0.1:8000
