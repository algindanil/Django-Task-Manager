from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    last_name = None
    first_name = models.CharField(max_length=32, null=True)
    profile_pic = models.ImageField(upload_to='images/%Y/%m/%d/', default='images/default_pfp.jpg')
    currency_amount = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    lvl = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    time_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['time_joined', 'first_name']

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=50)
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=512, null=True)
    progress_meter = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    priority = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        user = CustomUser.objects.get(id=self.player.id)
        return self.name + 'Made by player' + user.username
    
class Achievement(models.Model):
    name = models.CharField(max_length=50)
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=512, null=True)
    reward = models.FloatField(validators=[MinValueValidator(0)])
    requirement = models.BooleanField()
    is_claimed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=100)
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=512, null=True)
    is_completed = models.BooleanField(default=False)
    difficulty = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    due_date = models.DateTimeField(null=True)
    categories = models.ManyToManyField('Category', null=True)
    reward = models.FloatField(validators=[MinValueValidator(0.0)])
    create_date = models.DateTimeField(auto_now_add=True)
    is_daily = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # habit = models.ForeignKey('Habit', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('main_page:task', kwargs={'task_slug': self.slug})

class Habit(models.Model):
    name = models.CharField(max_length=100)
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=512, null=True)
    is_good = models.BooleanField(default=True)
    tracking_meter = models.FloatField(default=50.0, validators=[MinValueValidator(-100.0), MaxValueValidator(100.0)])
    categories = models.ManyToManyField('Category', null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    difficulty = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    positive_behavior_count = models.IntegerField(default=0)
    negative_behavior_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main_page:habit', kwargs={ 'habit_slug': self.slug })