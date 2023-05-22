from rest_framework import status
from rest_framework.test import APITestCase

from .serializers import CategorySerializer, TaskSerializer, HabitSerializer
from registration.models import CustomUser, Task, Habit, Category, Reward

class v1APITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testUser')
        self.user.save()
        self.category = Category.objects.create(player=self.user, name='test_category')
        self.category.save()
        self.reward = Reward.objects.create(name='test_reward', cost=1)
        self.reward.player.set((self.user, ))
        self.reward.save()
        self.task = Task.objects.create(player=self.user, name='test_task', difficulty=1,
                                        priority=1, slug='test-task')
        self.task.categories.set((self.category, ))
        self.task.save()
        self.daily = Task.objects.create(player=self.user, name='test_daily', difficulty=1,
                                        priority=1, is_daily=True, slug='test-daily')
        self.daily.categories.set((self.category, ))
        self.daily.save()
        self.habit = Habit.objects.create(player=self.user, name='test_habit', 
                                          difficulty=1, priority=1, slug='test-habit')
        self.habit.categories.set((self.category, ))
        self.habit.save()

        self.categories_url = 'http://localhost:8000/api/v1/categories/'
        self.tasks_url = 'http://localhost:8000/api/v1/tasks/'
        self.habits_url = 'http://localhost:8000/api/v1/habits/'
        self.rewards_url = 'http://localhost:8000/api/v1/rewards/'

    def authenticate_user(self):
        self.client.force_authenticate(user=self.user)

    # Category objects tests:
    def test_get_category_list(self):
        self.authenticate_user()
        response = self.client.get(self.categories_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_category_detail(self):
        url = self.categories_url + f'{self.category.id}/'
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.category.name)
 
    def test_category_list_fail_unauthorized(self):
        response = self.client.get(self.categories_url)
        self.assertEqual(response.status_code, 403)

    def test_post_category(self):
        self.authenticate_user()
        data = {
            'player': self.user.id,
            'name': 'test_post',
        }        
        response = self.client.post(self.categories_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        category = Category.objects.get(id=response.data['id'])
        serializer = CategorySerializer(category)
        self.assertEqual(response.data, serializer.data)

    
    # Task object tests:
    def test_get_task_list(self):
        self.authenticate_user()
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, 200)

    def test_task_detail(self):
        url = self.tasks_url + f'{self.task.id}/'
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.task.name)
 
    def test_task_list_fail_unauthorized(self):
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, 403)

    def test_post_task(self):
        self.authenticate_user()
        data = {
            'player': self.user.id,
            'name': 'test_post',
            'difficulty': 1,
            'priority': 1,
            'categories': self.category.id,
            'is_daily': False,
        }        
        response = self.client.post(self.tasks_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task = Task.objects.get(id=response.data['id'])
        serializer = TaskSerializer(task)
        self.assertEqual(response.data, serializer.data)

    def test_daily_post(self):
        self.authenticate_user()
        data = {
            'player': self.user.id,
            'name': 'test_post',
            'difficulty': 1,
            'priority': 1,
            'categories': self.category.id,
            'is_daily': True,
        }        
        response = self.client.post(self.tasks_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task = Task.objects.get(id=response.data['id'])
        serializer = TaskSerializer(task)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(serializer.data['is_daily'], True)

    
    # Habit object tests:
    def test_get_habit_list(self):
        self.authenticate_user()
        response = self.client.get(self.habits_url)
        self.assertEqual(response.status_code, 200)

    def test_habit_detail(self):
        url = self.habits_url + f'{self.habit.id}/'
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.habit.name)
 
    def test_habit_list_fail_unauthorized(self):
        response = self.client.get(self.habits_url)
        self.assertEqual(response.status_code, 403)

    def test_post_habit(self):
        self.authenticate_user()
        data = {
            'player': self.user.id,
            'name': 'test_post',
            'difficulty': 1,
            'priority': 1,
            'categories': self.category.id,
            'is_good': True,
        }        
        response = self.client.post(self.habits_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        habit = Habit.objects.get(id=response.data['id'])
        serializer = HabitSerializer(habit)
        self.assertEqual(response.data, serializer.data)

