from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'summarizer.settings')
celery = Celery('core')

# Using a string here means the worker will not have to pickle the object when using Windows.
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
celery.conf.broker_transport_options = {'visibility_timeout': 43200}  # 12 hours.
