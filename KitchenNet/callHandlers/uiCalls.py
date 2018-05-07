from bottle import get
import json 
from . import states

'''
    Shows the user a screen
'''
@get('/userInterface')
def serveTheUser():
	if states.goalIngredient is "none":
		htmlStrang = """<div style='background-color: tomato; font-size: 40px; text-align: center; height: 100%; width: 100%;'>
		<p style='font-family:Courier;'>
			<b>K I T C H E N A T O R</b>
		</p>
		<p>
			<img alt='How may I take your order?' src="http://i.somethingawful.com/inserts/articlepics/photoshop/08-06-04-terminators/DeltaAttack2go.jpg">
		</p>
		<p style='font-size: 14 px; font-family:Courier;'>
			WAITING FOR INGREDIENT REQUEST
		<p>
		</div>"""
	else:
			htmlStrang = """<div style='background-color: tomato; font-size: 40px; text-align: center; height: 100%; width: 100%;'>
			<p style='font-family:Courier;'>
				<b>K I T C H E N A T O R</b>
			</p>
			<p>
				<img alt='How may I take your order?' src="http://i.somethingawful.com/inserts/articlepics/photoshop/08-06-04-terminators/DeltaAttack2go.jpg">
			</p>
			<p style='font-size: 14 px; font-family:Courier;'>
				Fetching your '{}'
			<p>
			</div>""".format(states.goalIngredient)

	return htmlStrang

@get('/uiDebug')
def serveUIDebug():
	kstate = states.kitchenatorState
	htmlStrang = """<div style='background-color: tomato; font-size: 40px; text-align: left; height: 100%; width: 100%;'>
			<p style='font-family:Courier;'>
				<b>K I T C H E N A T O R</b>
				<b> D E B U G </b>
			</p>
			
			<p style='font-size: 10px; font-family:Courier;'>
				<h3> Kitchenator </h3>
				Kitchenator State: '{}' <br />
				Goal Ingredient: '{}' <br />
				<h3> Arm </h3>
				Current Arm State: '{}' <br />
				Arm Target State: '{}' <br />
				Arm Stop/Go: '{}' <br />
				Waiting to Continue: '{}' <br />
				<h3> Gesture </h3>
				{} <br />
				<h3> Colors & Poses </h3>
				{} <br />

			<p>
			</div>""".format(kstate,
				states.goalIngredient,
				states.armCurrentState,
				states.armTargetState,
                states.armStopGo,
				states.waitingToContinue,
				states.gesture,
				states.colorPoses
				)

	return htmlStrang