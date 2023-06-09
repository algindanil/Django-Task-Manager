# Generated by Django 4.1.7 on 2023-05-22 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0028_habit_reward'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reward',
            name='player',
        ),
        migrations.CreateModel(
            name='UserReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times_completed', models.IntegerField(default=1)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.reward')),
            ],
            options={
                'verbose_name': 'User Reward',
                'verbose_name_plural': 'User Rewards',
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='rewards',
            field=models.ManyToManyField(blank=True, null=True, through='registration.UserReward', to='registration.reward'),
        ),
        migrations.AddField(
            model_name='reward',
            name='player',
            field=models.ManyToManyField(through='registration.UserReward', to=settings.AUTH_USER_MODEL),
        ),
    ]
