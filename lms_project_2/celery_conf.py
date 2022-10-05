import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project_2.settings')
app = Celery('lms_project_2')

app.autodiscover_tasks()
app.conf.broker_url = 'redis://'
app.conf.result_backend = 'redis://'
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['json', 'pickle']
app.conf.result_expires = timedelta(days=1)
app.conf.task_always_eager = False
app.conf.worker_prefetch_multiplier = 4
