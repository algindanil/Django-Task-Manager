from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from registration.models import *
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView, CreateView

from .forms import *

@login_required
def index(request, is_daily=False):
    user = request.user
    tasks = Task.objects.filter(player=user, is_daily=is_daily)
    add_literal = 'Task'
    if is_daily:
        add_literal = 'Daily'
    return render(request, 'main_page/tasks.html', { 'user': user, 'tasks': tasks, 'is_daily': is_daily, 'add_literal': add_literal })

def habits_view(request):
    user = request.user
    habits = Habit.objects.filter(player=user)
    return render(request, 'main_page/habits.html', { 'user': user, 'habits': habits })


@login_required
def logout_view(request):
    logout(request)
    return redirect('registration:start_page')

@login_required
def categories_view(request):
    user = request.user
    categories = Category.objects.filter(player=user)
    return render(request, 'main_page/categories.html', { 'categories': categories })

@login_required
def achievements_view(request):
    return HttpResponse("achievements")

@login_required
def profile_view(request):
    return HttpResponse("profile")

# class ShowTask(DetailView):
#     model = Task
#     template_name = 'main_page/show_task.html'
#     slug_url_kwarg = 'task_slug'
#     context_object_name = 'task'

class ShowTask(UpdateView):
    model = Task
    template_name = 'main_page/show_task.html'
    fields = [ 'name', 'description', 'difficulty', 'due_date', 'categories', 'is_daily' ]

    def get_object(self, queryset=None):
        slug = self.kwargs['task_slug']
        return get_object_or_404(Task, slug=slug)
    
    def form_valid(self, form):
        form.save()
        return redirect('main_page:tasks')
    
class ShowHabit(UpdateView):
    model = Habit
    template_name = 'main_page/show_habit.html'
    fields = { 'name', 'description', 'categories' }

    def get_object(self, queryset=None):
        slug = self.kwargs['habit_slug']
        return get_object_or_404(Habit, slug=slug)
    
    def form_valid(self, form):
        form.save()
        return redirect('main_page:home')

class AddTask(CreateView):
    form_class = TaskForm
    template_name = 'main_page/add_task.html'
    success_url = 'main_page:tasks'

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        success_url = reverse('main_page:tasks')
        if form.is_valid():
            task = form.save(commit=False)
            task.player = request.user
            task.slug = task.name
            if task.is_daily:
                success_url = reverse('main_page:dailies')
            task.save()
            return redirect(success_url)
    else:
        form = TaskForm()
    return render(request, 'main_page/add_task.html', {'form': form})
    

class AddHabit(CreateView):
    form_class = HabitForm
    template_name = 'main_page/add_habit.html'
    success_url = 'main_page:habits'

# class ShowHabit(DetailView):
#     model = Habit
#     template_name = 'main_page/show_habit.html'
#     slug_url_kwarg = 'habit_slug'
#     context_object_name = 'habit'