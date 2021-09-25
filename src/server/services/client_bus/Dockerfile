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
COPY bin/client-bus bin/client-bus

RUN chmod +x bin/api
RUN mkdir logs

EXPOSE 8000

ENV MP_ENVIRONMENT=environment:-development

ENTRYPOINT ["python", "server/services/client_bus/websocket_server.py"]
