from bottle import get
import json 
from . import states

'''
    Shows the user a screen
'''
@get('/userInterface')
def serveTheUser():
	htmlStrang = """<div style='background-color: tomato; font-size: 40px; text-align: center; height: 100%; width: 100%;'>
	<p style='font-family:Courier;'>
		<b>K I T C H E N A T O R</b>
	</p>
	<p style='font-size: 14 px;'>
		goal ingredient: {}
	<p>
	<p>
		<img alt='How may I take your order?' src="http://i.somethingawful.com/inserts/articlepics/photoshop/08-06-04-terminators/DeltaAttack2go.jpg">
	</p>
	</div>""".format(states.goalIngredient)
	return htmlStrang