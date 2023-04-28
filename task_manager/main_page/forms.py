from django.forms import ModelForm

from registration.models import Habit, Task, Category


class HabitForm(ModelForm):
    
    class Meta:
        model = Habit
        fields = ['name', 'description', 'priority','categories',]


class TaskForm(ModelForm):
    
    class Meta:
        model = Task
        fields = ['name',
                  'description',
                  'difficulty',
                  'priority',
                  'categories',
                  ]
        
    def __init__(self, request, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        if request.user:
            self.fields['categories'].queryset = Category.objects.filter(player=request.user)
        

class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = [
            'name',
            'description',
        ]