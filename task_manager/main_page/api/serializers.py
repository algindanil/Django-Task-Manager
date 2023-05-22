from rest_framework import serializers
from django.utils.text import slugify

from registration.models import Task, Habit, Category, Reward


class TaskSerializer(serializers.ModelSerializer):
    player = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_daily = serializers.BooleanField(default=False)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['is_completed', 'reward', 'create_date', 'completion_count', 'slug']

    def create(self, validated_data):
        is_daily = self.initial_data.get('is_daily', False).capitalize()
        validated_data['is_daily'] = is_daily
        categories_data = validated_data.pop('categories', [])
        test_slug = slugify(validated_data['name'])
        i = 1

        while True:
            try:
                Task.objects.get(slug=test_slug)
                test_slug = f"{slugify(task.name)}-{i}"
                i += 1
            except Task.DoesNotExist:
                validated_data['slug'] = test_slug
                break

        task = Task.objects.create(**validated_data)
        task.categories.set(categories_data)
        task.save()
        return task
    
    def validate_categories(self, categories):
        user = self.context['request'].user
        for category in categories:
            if category.player != user:
                raise serializers.ValidationError("One or more categories do not belong to the current user.")
        return categories
    

class HabitSerializer(serializers.ModelSerializer):
    player = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_good = serializers.BooleanField(default=True)

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['reward', 'tracking_meter', 'positive_behavior_count', 'negative_behavior_count', 'slug']

    def create(self, validated_data):
        is_good = self.initial_data.get('is_good', False).capitalize()
        validated_data['is_good'] = is_good
        categories_data = validated_data.pop('categories', [])
        test_slug = slugify(validated_data['name'])
        i = 1

        while True:
            try:
                Habit.objects.get(slug=test_slug)
                test_slug = f"{slugify(habit.name)}-{i}"
                i += 1
            except Habit.DoesNotExist:
                validated_data['slug'] = test_slug
                break

        habit = Habit.objects.create(**validated_data)
        habit.categories.set(categories_data)
        habit.save()
        return habit
    
    def validate_categories(self, categories):
        user = self.context['request'].user
        for category in categories:
            if category.player != user:
                raise serializers.ValidationError("One or more categories do not belong to the current user.")
        return categories
    

class CategorySerializer(serializers.ModelSerializer):
    player = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['progress meter']
    

class RewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reward
        fields = '__all__'
        read_only_fields = ['times_claimed', 'cost']
     