# Generated by Django 4.1.7 on 2023-04-17 13:26

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0019_alter_task_reward'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('cost', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('times_claimed', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to='award_pics/%Y/%m/%d/')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='slug',
            field=models.SlugField(default=9999, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Achievement',
        ),
        migrations.AddField(
            model_name='reward',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
