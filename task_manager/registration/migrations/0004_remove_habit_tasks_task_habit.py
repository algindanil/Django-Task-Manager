# Generated by Django 4.1.7 on 2023-03-18 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_alter_customuser_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habit',
            name='tasks',
        ),
        migrations.AddField(
            model_name='task',
            name='habit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.habit'),
        ),
    ]
