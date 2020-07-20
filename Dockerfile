FROM python:3.8-alpine

ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
	&& pip install --upgrade pip

COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN echo "SECRET_KEY=`python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`" >> web-variables.env
COPY . /code/
