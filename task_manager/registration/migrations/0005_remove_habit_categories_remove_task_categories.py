# Generated by Django 4.1.7 on 2023-03-18 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_remove_habit_tasks_task_habit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habit',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='task',
            name='categories',
        ),
    ]
