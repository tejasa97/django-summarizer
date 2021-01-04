# django-summarizer

This is the backend for https://nuggets.vercel.app/
More info coming soon

Python : tested with 3.7.3

1st run:
```sh
pip install -r requirements.txt
python -m spacy download en_core_web_sm
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
