# Generated by Django 4.1.7 on 2023-04-23 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0020_reward_customuser_slug_delete_achievement_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='priority',
        ),
    ]
