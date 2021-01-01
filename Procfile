web: gunicorn summarizer.wsgi:application --log-file -
worker: celery -A core worker --beat --loglevel=info