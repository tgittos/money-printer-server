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
COPY config* ./
COPY bin/money-printer bin/money-printer

RUN mkdir logs

ENV MP_ENVIRONMENT=environment:-development
ENV MP_HOST=0.0.0.0
ENV MP_PORT=8000

EXPOSE 8000

ENTRYPOINT bin/money-printer && tail -f logs/mp.log
