FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y gcc libc6-dev make


COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apt-get purge -y --auto-remove gcc libc6-dev

COPY . code
WORKDIR code

EXPOSE 8000

# Run the production server
CMD gunicorn --bind 0.0.0.0:8000 --access-logfile - summarizer.wsgi:application