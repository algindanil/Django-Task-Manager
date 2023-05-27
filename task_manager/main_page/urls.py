from django.urls import path, include
from django.conf.urls.static import static

# from main_page.views import tasks_view, habits_view, logout_view, login_required, categories_view, reward_view, EditProfile, ShowHabit, ShowTask, add_task, add_habit, add_category, complete_task, tasks_archive
import main_page.views as views
from .api import urls as api_urls
from task_manager import settings


app_name = 'main_page'


urlpatterns = [
    path('tasks', views.tasks_view, name='tasks'),
    path('habits', views.habits_view, name='habits'),
    path('dailies', views.tasks_view, kwargs={'is_daily': True}, name='dailies'),
    path('logout', views.logout_view, name='logout'),
    path('categories', views.categories_view, name='categories'),
    path('reward', views.reward_view, name='reward'),
    path('profile/<slug:user_slug>', views.login_required(views.EditProfile.as_view()), name='profile'),
    path('task/<slug:task_slug>', views.login_required(views.ShowTask.as_view()), name='task'),
    path('habit/<slug:habit_slug>', views.login_required(views.ShowHabit.as_view()), name='habit'),
    path('add_task', views.add_task, name='add_task'),
    path('add_daily', views.add_task, kwargs={'is_daily': True}, name='add_daily'),
    path('add_category', views.add_category, name='add_category'),
    path('add_habit', views.add_habit, name='add_habit'),
    path('complete_task/<int:task_id>', views.complete_task, name='complete_task'),
    path('complete_daily/<int:task_id>', views.complete_task, kwargs={'is_daily': True}, name='complete_daily'),
    path('tasks_archive', views.tasks_archive, name='tasks_archive'),
    path('dailies_archive', views.tasks_archive, kwargs={ 'is_daily': True }, name='dailies_archive'),
    path('habit_add/<int:habit_id>', views.habit_control, kwargs={'counter_positive': True}, name='habit_add'),
    path('habit_sub/<int:habit_id>', views.habit_control, kwargs={'counter_positive': False}, name='habit_sub'),
    path('tasks/delete/<int:task_id>', views.login_required(views.delete_task), name='delete_task'),
    path('habits/delete/<int:habit_id>', views.login_required(views.delete_habit), name='delete_habit'),
    path('queries', views.logout_view, name='queries'),

    path('api/v1/', include(api_urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
