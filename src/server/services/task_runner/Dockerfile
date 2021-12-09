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
COPY server/.secrets.json server/.secrets.json
COPY config* .

RUN mkdir logs

ENV MP_ENVIRONMENT=environment:-development
ENV PYTHONPATH=$PYTHONPATH:.

ENTRYPOINT python server/bin/task-runner.py && tail -f logs/mp.log
