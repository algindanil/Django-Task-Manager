from celery import shared_task

from task_manager.celery import app
from registration.models import Task


@shared_task
def reset_dailies():
    for d in Task.objects.filter(is_daily=True):
        if d.is_completed:
            d.completion_count += 1
        d.is_completed = False    
