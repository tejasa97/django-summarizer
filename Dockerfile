FROM python:3.7-alpine

# Install dependencies required for psycopg2 python package
# RUN apk update && apk add libpq
# RUN apk update && apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev 
RUN apk update && apk add --virtual .build-deps gcc python3-dev musl-dev g++ gfortran
# RUN apk add --no-cache --virtual=build_deps g++ gfortran
# pip install --no-cache-dir spacy
# RUN apk add python-dev -y && \
#     apk add python3-dev -y && \
#     apk add libevent-dev  && \

# install new gcc
# apk update && \
# apk add build-essential software-properties-common -y && \
# add-apt-repository ppa:ubuntu-toolchain-r/test -y && \
# apk update && \
# apk add gcc-snapshot -y && \
# apk update && \
# apk add gcc-6 g++-6 -y && \
# update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-6 && \
# apk add gcc-4.8 g++-4.8 -y && \
# update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8;

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
# RUN mv wait-for /bin/wait-for

RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir -r text_summarizer/requirements.txt
RUN python -m spacy download en_core_web_sm

# Remove dependencies only required for psycopg2 build
RUN apk del .build-deps

EXPOSE 8000

CMD ["gunicorn", "mysite.wsgi", "0:8000"]