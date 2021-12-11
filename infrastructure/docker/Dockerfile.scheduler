#syntax=docker/dockerfile:1

FROM tgittos/money-printer:latest

ARG environment

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY core core
COPY server server
COPY .secrets.json .secrets.json
COPY config* .

RUN mkdir logs

ENV MP_ENVIRONMENT=environment:-development
ENV MP_REDIS__HOST=MP_REDIS__HOST:-localhost
ENV PYTHONPATH=$PYTHONPATH:.

ENTRYPOINT rqscheduler --host $MP_REDIS__HOST --port 6379 --db 0
