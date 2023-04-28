from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, CreateView
from django.utils.text import slugify
from django.db.models import Prefetch

from .forms import TaskForm, HabitForm, CategoryForm
from registration.models import CustomUser, Category, Reward, Task, Habit
from registration.forms import CustomUserChangeForm


@login_required
def tasks_view(request, is_daily=False):
    
    user = request.user
    tasks = Task.objects.filter(player=user, is_daily=is_daily, is_completed=False)
    return render(request, 'main_page/tasks.html', { 'user': user, 'tasks': tasks, 'is_daily': is_daily })


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
    categories = Category.objects.filter(player=user).prefetch_related(
        Prefetch('task_set', queryset=Task.objects.filter(is_completed=False)),
                 'habit_set'
    ).all()

    print(categories)
    # for c in categories:
    #     for t in c.task_set.all():
    #         print(t.name)

    return render(request, 'main_page/categories.html', { 'categories': categories })


@login_required
def reward_view(request):
    
    return HttpResponse("reward")


class EditProfile(UpdateView):
    
    model = CustomUser
    template_name = 'main_page/profile.html'
    fields = ['first_name', 'profile_pic', ]

    def form_valid(self, form):
        form.save()
        return redirect('main_page:tasks')

    def get_object(self, queryset=None):
        slug = self.kwargs['user_slug']
        return get_object_or_404(CustomUser, slug=slug)


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


# class AddTask(CreateView):
    
#     form_class = TaskForm
#     template_name = 'main_page/add_task.html'
#     success_url = 'main_page:tasks'


@login_required
def add_task(request, is_daily=False):
    
    task_type = 'DAILY' if is_daily else 'TASK'
    
    if request.method == 'POST':
        form = TaskForm(request, request.POST)
        success_url = reverse('main_page:tasks')
        if form.is_valid():
            task = form.save(commit=False)
            task.player = request.user
            task.reward = 5.0 * task.difficulty
            task.is_daily = is_daily
            test_slug = slugify(task.name)
            i = 1

            while True:
                try:
                    Task.objects.get(slug=test_slug)
                    test_slug = f"{slugify(task.name)}-{i}"
                    i += 1
                except Task.DoesNotExist:
                    task.slug = test_slug
                    break

            if is_daily:
                success_url = reverse('main_page:dailies')
            task.save()
            form.save_m2m()
            return redirect(success_url)
    else:
        form = TaskForm(request)
    
    return render(request, 'main_page/add_task.html', {'form': form, 'task_type': task_type, })


@login_required    
def add_habit(request):

    if request.method == 'POST':
        form = HabitForm(request.POST)
        success_url = reverse('main_page:habits')
        if form.is_valid():
            habit = form.save(commit=False)
            habit.player = request.user
            test_slug = slugify(habit.name)
            i = 1
            
            while True:
                try:
                    Habit.objects.get(slug=test_slug)
                    test_slug = f"{slugify(habit.name)}-{i}"
                    i += 1
                except Habit.DoesNotExist:
                    habit.slug = test_slug
                    break
            
            habit.save()
            form.save_m2m()
            return redirect(success_url)
    else:
        form = HabitForm()
    
    return render(request, 'main_page/add_habit.html', {'form': form})


@login_required
def add_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        success_url = reverse('main_page:tasks')
        if form.is_valid():
            category = form.save(commit=False)
            category.player = request.user
            category.save()
            return redirect(success_url)
        
    else:
        form = CategoryForm()

    return render(request, 'main_page/add_category.html', {'form': form})



@login_required
def complete_task(request, task_id, is_daily=False):
    
    task = get_object_or_404(Task, id=task_id)
    user = request.user
    categories = task.categories.all()
    for c in categories:
        c.progress_meter += task.reward
        c.save()
    user.currency_amount += task.reward
    task.completion_count += 1
    task.is_completed = True
    task.save()
    user.save()
    return redirect('main_page:tasks') if not is_daily else redirect('main_page:dailies')


@login_required
def tasks_archive(request, is_daily=False):
    
    user = request.user
    tasks = Task.objects.filter(player=user, is_daily=is_daily, is_completed=True)
    return render(request, 'main_page/tasks_archive.html',
                  { 'user': user, 'tasks': tasks, 'is_daily': is_daily })    
