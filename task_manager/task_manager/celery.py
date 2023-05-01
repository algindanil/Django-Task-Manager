import os
from datetime import time

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

app = Celery('task_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'reset-dailies': {
        'task': 'main_page.tasks.reset_dailies',
        #'schedule': time(hour=16, minute=45),
        'schedule': 60.0,
    }
}

app.autodiscover_tasks()
