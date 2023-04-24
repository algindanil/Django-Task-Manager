from django.urls import path

# from main_page import views as main_views
from main_page.views import *
from task_manager import settings

from django.conf.urls.static import static

app_name = 'main_page'

urlpatterns = [
    path('tasks', tasks_view, name='tasks'),
    path('habits', habits_view, name='habits'),
    path('dailies', tasks_view, kwargs={'is_daily': True}, name='dailies'),
    path('logout', logout_view, name='logout'),
    path('categories', categories_view, name='categories'),
    path('reward', reward_view, name='reward'),
    path('profile/<slug:user_slug>', login_required(EditProfile.as_view()), name='profile'),
    path('task/<slug:task_slug>', login_required(ShowTask.as_view()), name='task'),
    path('habit/<slug:habit_slug>', login_required(ShowHabit.as_view()), name='habit'),
    path('add_task', add_task, name='add_task'),
    path('add_daily', add_task, kwargs={'is_daily': True}, name='add_daily'),
    path('add_habit', add_habit, name='add_habit'),
    path('complete_task/<int:task_id>', complete_task, name='complete_task'),
    path('complete_daily/<int:task_id>', complete_task, kwargs={'is_daily': True}, name='complete_daily'),
    path('tasks_archive', tasks_archive, name='tasks_archive'),
    path('dailies_archive', tasks_archive, kwargs={ 'is_daily': True }, name='dailies_archive'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
