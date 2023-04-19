from django.forms import ModelForm
from django import forms

from registration.models import *

class HabitForm(ModelForm):
    class Meta:
        model = Habit
        fields = [ 'name', 'description', 'categories' ]

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [ 'name', 'description', 'difficulty', 'categories' ]
        