# Generated by Django 4.1.7 on 2023-04-23 12:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0021_remove_category_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.SmallIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
            preserve_default=False,
        ),
    ]
