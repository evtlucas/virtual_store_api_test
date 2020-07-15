FROM python:3.8-alpine

ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code

RUN apk add --no-cache --virtual .build-deps \
	&& pip install --upgrade pip

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/



