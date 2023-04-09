from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from registration.models import *
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView, CreateView

from .forms import *

@login_required
def index(request):
    user = request.user
    tasks = Task.objects.filter(player=user, is_daily = False)
    return render(request, 'main_page/index.html', { 'user': user, 'tasks': tasks })

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
    fields = { 'name', 'description', 'difficulty', 'due_date', 'categories', 'is_daily' }

    def get_object(self, queryset=None):
        slug = self.kwargs['task_slug']
        return get_object_or_404(Task, slug=slug)
    
    def form_valid(self, form):
        form.save()
        return redirect('main_page:home')
    
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
    success_url = 'main_page:home'

def habits_view(request):
    return HttpResponse("Habits")

def dailies_view(request):
    return HttpResponse("Dailies")


# class ShowHabit(DetailView):
#     model = Habit
#     template_name = 'main_page/show_habit.html'
#     slug_url_kwarg = 'habit_slug'
#     context_object_name = 'habit'