# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def home(request):
	return HttpResponse('''
	<div style='background-color: tomato; font-size: 40px; text-align: center; height: 100%; width: 100%;'>
		<p style='font-family:Courier;'>
			<b>K I T C H E N A T O R</b>
		</p>
		<p>
			<img alt='How may I take your order?' src="http://i.somethingawful.com/inserts/articlepics/photoshop/08-06-04-terminators/DeltaAttack2go.jpg">
		</p>
		<input type='button' value='P R O C E E D'></input>
		<input type='button' value='F L E E'></input>
	</div>''')
