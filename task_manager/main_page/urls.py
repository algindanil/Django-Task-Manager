from django.urls import path

# from main_page import views as main_views
from main_page.views import *
from task_manager import settings

from django.conf.urls.static import static

app_name = 'main_page'

urlpatterns = [
    path('tasks', index, name='home'),
    path('logout', logout_view, name='logout'),
    path('categories', categories_view, name='categories'),
    path('achievements', achievements_view, name='achievements'),
    path('profile', profile_view, name='profile'),
    path('task/<slug:task_slug>', ShowTask.as_view(), name='task'),
    path('habit/<slug:habit_slug>', ShowHabit.as_view(), name='habit'),
    path('add_task', AddTask.as_view(), name='add_task'),
    path('habits', habits_view, name='habits'),
    path('dailies', dailies_view, name='dailies'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
