#syntax=docker/dockerfile:1

FROM python:3

ARG environment

RUN apt update
RUN apt -y install redis

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY core core
COPY server server
COPY server/.secrets.json server/.secrets.json

RUN mkdir logs

ENV MP_ENVIRONMENT=environment:-development

RUN nohup redis-server &

ENTRYPOINT python server/services/monolith.py
