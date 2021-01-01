from __future__ import absolute_import
from django.conf import settings
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'summarizer.settings')
celery = Celery('core')

# Using a string here means the worker will not have to pickle the object when using Windows.
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
celery.conf.broker_transport_options = {'visibility_timeout': 43200}  # 12 hours.

celery.conf.beat_schedule = {
    'delete_unsaved_summaries': {
        'task': 'summarizer_app.tasks.delete_unsaved_summaries',
        'schedule': 3600,
    },
}
