#syntax=docker/dockerfile:1

FROM python:3

RUN apt update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY core core
COPY server server

ENTRYPOINT ["bash", "server/bin/data-server"]