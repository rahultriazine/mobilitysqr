from __future__ import absolute_import
import os
from celery import Celery
import django
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mobilitysqr_live.settings')
django.setup()
app = Celery('mobilitysqr_live')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        # 'task': 'mobility_apps.travel.task.myTask',
        'task': 'mobility_apps.employee.tasks.send_mailChatEveryDay',
        'schedule': 60.0,
        # 'args': (16, 16)
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')