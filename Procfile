web: gunicorn summarizer.wsgi:application --log-file -
worker: celery -A core worker --loglevel=info