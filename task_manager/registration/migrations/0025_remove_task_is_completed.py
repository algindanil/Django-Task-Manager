# Generated by Django 4.1.7 on 2023-04-24 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0024_alter_customuser_options_task_completion_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_completed',
        ),
    ]
