# django-summarizer


1st run:
sh```
python manage.py migrate
```

Always run celery in a different terminal
```
celery -A core worker -l info
```

Finally, run the web app
```
python manage.py runserver
```
