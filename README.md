# Money Printer Server

The server application for the Money Printer, written in Python and backed to MySQL, using Redis as a transport backbone.

Consists of a handful of services:

- data server
- task runner
- api

### Data Server

The data server is a threaded server that listens to client requests from the api and services them by
dispatching requests to a variety of upstream services, specifically IEX via SSE, and proxies the results back to the
api, backboned by Redis.

### Task Runner

A threaded server that services a work queue backed by Redis. Various services such as the API push jobs into the Redis
queue and the task runner pulls jobs off and executes them. 

The task runner server is also responsible for scheduling and running tasks from stored jobs. These are scheduled as
messages onto the task runner queue.

### API

The main RESTful HTTP API server implemented in Flask that services the bulk of client requests. Supports RESTful
and web socket requests. All private resources secured by  JWT based authentication.

## Development setup

### 3rd Party Dependencies
Money Printer depends on the following 3rd party services, which you will need API keys for:

- IEXCloud
- Mailgun
- Plaid

#### IEXCloud ####

Money Printer uses IEX Cloud for both historical stock market price querying and real time stock market price streaming.
This is a pretty fundamental part of the application and is required.

#### Mailgun ####

Money Printer uses email to communicate non-real time messages. Failing to provide valid Mailgun creds will result in
initialization failing to deliver your password, but that can be worked around with minimal effort in the source.

#### Plaid ####

Plaid is used to sync account holdings and balances for the more wealth planning feature set. This can be optionally
written out if you're willing to keep your own accounts in sync, though no UI exists for that yet. Nor API endpoints.

### Environment setup

#### The Easy Way

- install Docker Desktop
- run `docker-compose -f docker-compose.microservices.yml up` to run in microservice mode (recommended),
or `docker-compose -f docker-compose.monolith.yml up` to run as a monolith (matches AWS deployment)

#### The Hard Way

- install Python 3, redis, MySQL
- create a .venv with `python3 -m venv .venv`
- activate with `source .venv/bin/activate`
- `pip install -r requirements`
- fill `config.json` with values that make sense for your project
- decrypt the secrets using `git-secret` if working on this project, else create your own `.secrets.json` file with
the following format: TODO
- create the schema you wish to use in MySQL, add config to appropriate places
- initialize the DB by running `alembic update head`
- run `bin/money-printer` to run the app as a monolith, or run each individual service in its own terminal window/
sub-process for microservices mode

## Deploying

Money Printer uses AWS ElasticBeanstalk to deploy itself into the development environment.
The Money Printer application is set up as a Docker application, with a custom base docker image.

If you add additional `pip` dependencies, depending on how long they take to install, you may need to move them into
the `platform/Dockerfile` and rebuild, tag and deploy a new base Money Printer docker image.

Otherwise, you can functionally ignore the `platform/Dockerfile` unless you're doing work on the application infrastructure.

### Deploy Command

`eb deploy` - this will deploy the environment into development