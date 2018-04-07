# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class IngredientLibrary(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=100)

class ActionQueue(models.Model):
    description = models.CharField(max_length=100)

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=5)
    requested_at = models.DateTimeField(auto_now_add=True)
    ingredientLibrary = models.ForeignKey(IngredientLibrary, related_name='ingredient')
    actionQueue = models.ForeignKey(ActionQueue, related_name='ingredient')