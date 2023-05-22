from rest_framework import viewsets

from registration.models import Task, Habit, Category, Reward
from .serializers import TaskSerializer, HabitSerializer, CategorySerializer, RewardSerializer
from .permissions import IsOwner, IsAdminOrReadOnly


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsOwner, )

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)

    def get_queryset(self):
        return Task.objects.filter(player=self.request.user)


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsOwner, )

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)

    def get_queryset(self):
        return Habit.objects.filter(player=self.request.user)
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsOwner, )

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)

    def get_queryset(self):
        return Category.objects.filter(player=self.request.user)


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = (IsAdminOrReadOnly, )

