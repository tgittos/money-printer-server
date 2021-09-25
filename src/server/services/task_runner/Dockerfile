#syntax=docker/dockerfile:1

FROM python:3

WORKDIR /app

RUN apt update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY server/requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY core core
COPY server server