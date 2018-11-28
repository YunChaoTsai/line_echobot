from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'line_echobot.settings')

app = Celery('line_echobot')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')


# TODO: move the settings into 'celeryconfig.py'
# - http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
app.conf.update(
    result_backend='redis://localhost:6379/',
    broker_url='redis://localhost:6379/'
)


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
