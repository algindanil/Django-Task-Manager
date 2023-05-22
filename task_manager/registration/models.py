from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify


class CustomUser(AbstractUser):
    
    # Required fields:
    first_name = models.CharField(max_length=32, null=True)

    # Optional fields and fields with default values:
    last_name = None
    profile_pic = models.ImageField(upload_to='images/%Y/%m/%d/', default='images/default_pfp.jpg')
    currency_amount = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    lvl = models.SmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    time_joined = models.DateTimeField(auto_now_add=True)
    rewards = models.ManyToManyField('Reward', through='UserReward', blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['time_joined']

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('main_page:profile', kwargs={'user_slug': self.slug})
    
    def save(self, **kwargs):
        super(CustomUser, self).save()

        if not self.slug:
            self.slug = slugify(self.pk)
            super(CustomUser, self).save()


class Category(models.Model):

    # Required fields:
    name = models.CharField(max_length=50)
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # Optional fields and fields with default values:
    description = models.CharField(max_length=512, null=True, blank=True)
    progress_meter = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    
class Reward(models.Model):

    # Required fields:
    player = models.ManyToManyField('CustomUser', through='UserReward')
    name = models.CharField(max_length=50)
    cost = models.FloatField(validators=[MinValueValidator(0.0)])

    # Optional fields and fields with default values:
    description = models.CharField(max_length=512, null=True, blank=True)
    times_claimed = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Task(models.Model):
    
    def validate_due_date(value):
        if value and value < timezone.now():
            raise ValidationError('Due date cannot be in the past.')
    
    # Required fields:
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    difficulty = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    priority = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    categories = models.ManyToManyField('Category')
    
    # Optional fields and fields with default values:
    description = models.CharField(max_length=512, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True, validators=[validate_due_date])
    reward = models.FloatField(validators=[MinValueValidator(0.0)], default=1.0)
    create_date = models.DateTimeField(auto_now_add=True)
    is_daily = models.BooleanField(default=False)
    completion_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('main_page:task', kwargs={'task_slug': self.slug})

    def get_completion_url(self):
        if not self.is_daily:
            return reverse('main_page:complete_task', kwargs={'task_id': self.pk}) 
        else:
            return reverse('main_page:complete_daily', kwargs={'task_id': self.pk}) 
        

class Habit(models.Model):

    # Required fields:
    name = models.CharField(max_length=100)
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category')
    difficulty = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    priority = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    # Optional fields and fields with default values:
    description = models.CharField(max_length=512, null=True, blank=True)
    is_good = models.BooleanField(default=True)
    reward = models.FloatField(validators=[MinValueValidator(0.0)], default=1.0)
    tracking_meter = models.FloatField(default=0.0, validators=[MinValueValidator(-100.0), MaxValueValidator(100.0)])
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    positive_behavior_count = models.IntegerField(default=0)
    negative_behavior_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main_page:habit', kwargs={'habit_slug': self.slug})
    
    def get_add_url(self):
        return reverse('main_page:habit_add', kwargs={'habit_id': self.pk})
        
    def get_sub_url(self):
        return reverse('main_page:habit_sub', kwargs={'habit_id': self.pk})
        

class UserReward(models.Model):
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    times_completed = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'User Reward'
        verbose_name_plural = 'User Rewards'

    def __str__(self):
        return f'{self.player.username} - {self.reward.name}'