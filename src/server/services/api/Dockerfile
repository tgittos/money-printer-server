#syntax=docker/dockerfile:1

FROM python:3

ARG environment

RUN apt update
RUN apt install -y nginx

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY core core
COPY server server
COPY bin/api bin/api

RUN chmod +x bin/api
RUN mkdir logs

EXPOSE 5000

ENV MP_ENVIRONMENT=environment:-development
ENV PYTHONPATH="${PYTHONPATH}:."

ENTRYPOINT python server/services/api/api_server.py