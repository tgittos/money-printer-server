# Money Printer Server

The server application for the Money Printer, written in Python and backed to MySQL.

Consists of a handful of services:

- upstream server
- client hub
- task runner
- api

### Upstream Server

The upstream server is a threaded server that listens to client requests from the client hub and services them by
dispatching requests to a variety of upstream services, specifically IEX via SSE, and proxies the results back onto the
client hub.

### Client Hub

The client hub is a websocket server that facilitates real time communication from the client to the server. This is
used primarily for real time data streaming from the server to the client.

### Task Runner

A threaded server that services a work queue backed by Redis. Various services such as the API push jobs into the Redis
queue and the task runner pulls jobs off and executes them. Task runner state can be queried via the client hub.

### API

The main RESTful HTTP API server implemented in Flask that services the bulk of client requests. Provides JWT based authentication.

## Development setup

### 3rd Party Dependencies
Money Printer depends on the following 3rd party services, which you will need API keys for:

- IEXCloud
- Mailgun

### Environment setup

- install Python 3, redis, MySQL
- create a .venv with `python3 -m venv .venv`
- activate with `source .venv/bin/activate`
- `pip install -r requirements`
- copy `config.py.example` to `config.py`
- create a new schema, update `config.py` with SQL config, IEXCloud API keys and Mailgun keys
- update the MySql connection string in the `alembic.ini` inside `core`
- initialize the DB by running `alembic update head` from inside the `core` directory
- run `bin/money-printer`