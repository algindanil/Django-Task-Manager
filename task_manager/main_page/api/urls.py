from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, HabitViewSet, CategoryViewSet, RewardViewSet

task_router = DefaultRouter()
task_router.register(r'tasks', TaskViewSet)

habit_router = DefaultRouter()
habit_router.register(r'habits', HabitViewSet)

category_router = DefaultRouter()
category_router.register(r'categories', CategoryViewSet)

reward_router = DefaultRouter()
reward_router.register(r'rewards', RewardViewSet)


urlpatterns = [
    path('', include(task_router.urls)),
    path('', include(habit_router.urls)),
    path('', include(category_router.urls)),
    path('', include(reward_router.urls)),
]
