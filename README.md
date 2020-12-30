# django-summarizer


1st run:
```sh
python manage.py migrate
```

Always run celery in a different terminal
```sh
celery -A core worker -l info
```

Finally, run the web app
```sh
python manage.py runserver
```
