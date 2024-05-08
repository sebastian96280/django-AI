from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectogrado.settings')

app = Celery('proyectogrado')  # Replace 'your_project' with your project's name.
app.conf.enable_utc= False
app.conf.update(timezone = 'America/Bogota')
# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')