# Generated by Django 4.1.7 on 2023-04-09 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0016_remove_task_habit_habit_difficulty_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='categories',
            field=models.ManyToManyField(to='registration.category'),
        ),
        migrations.AlterField(
            model_name='task',
            name='categories',
            field=models.ManyToManyField(to='registration.category'),
        ),
    ]
