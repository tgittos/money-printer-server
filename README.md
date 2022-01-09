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

Money Printer provides both a full REST-full API service, and a more limited GraphQL API service.

The REST-full service is intended to fulfill all internal application and external integrating partner needs.

The GraphQL service provides read-only access to the authed user's app specific data.

#### REST

The main RESTful HTTP API server implemented in Flask that services the bulk of client requests. Supports RESTful
and web socket requests. All private resources secured by  JWT based authentication.

Documentation for the api can be found at `http://localhost/api/v1/` via SwaggerUI when the application is running in a
non `production` mode.

#### GraphQL

GraphQL is integrated through `graphene`, and the GraphQL endpoint can be found at `http://localhost/api/v1/graphql`.

When the application is running in a non `production` mode, the GraphQL serves a GraphQLi web query interface.

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

## Development

Money Printer is a containerized application, most of the dev tasks should be easily accomplishable with Docker.

This server project also includes a `package.json` file that defines tasks that enable you to easily work with Docker.

Regardless of how you choose to interact with Docker, this project has a separate definition for development vs. production.
By running the `docker-compose.dev.yml` file, you'll receive:

- a local, persistant MySQL database server
- a local redis server
- local `/src` directory mounted to enable hot code reloading
- an automatic `ngrok` tunnel to ensure webhook integration with Plaid works properly in local development
- a full production style, auto-configured stack for `Prometheus` and `Matomo` to test metrics and stats tracking

### ngrok

`Plaid` uses webhooks to keep integration consumers up to date with their client's token statuses, such as when the user has
changed their auth passwords or closed accounts.

The nature of working on a local development machine presents challenges when working with webhooks, hence ngrok.

ngrok will open a tunnel to the public internet to the API running on your local machine, and the API code looks for the
`MP_WEBHOOK_HOST` environment variable to determine how to link the webhooks up for Plaid. This will enable Plaid to send webhooks
from their test environment into your local development environment.

ngrok also offers a UI from which you can observe a log of incoming requests.

This is a development specific service, so will not run when the application is launched in `production` mode.

The ngrok UI is available at `http://localhost:4040/` when running.

### Prometheus

Prometheus is integrated as a way of tracking internal app performance metrics.

Money Printer has been instrumented with Prometheus to track the performance of all public API endpoints and most internal
discrete `repository` level commands. A subset of `actions` has also been instrumented.

Instrumentation is not free, and while we should ensure we have a good idea of how the various parts of the application
are performing, we shouldn't instrument it so much that the instrumentation affects performance.

Prometheus is available at `http://localhost:9090/` when running.

### Matomo

Matomo provides Google Analytics style tracking through our application, but it's all local and much more respective of the
user's privacy.

We use Matomo to track performance of various UX elements and flows through out the application. The goal of the Matomo analytics
is to improve the functionality and UX of the application, not to mine data about the users to sell.

As part of tracking for marketing purposes, we do collect some demographic information about our user base, but that information is private.

Matomo is available at `http://localhost:8080/` when running.

### Environment setup

- install Docker Desktop
- install any recent-ish version of Node for task management (optional)
- ensure you've build the docker images in `money-printer-infrastructure`
- edit hosts file (below) to access services through the reverse proxy
- either run `npm run start` or `docker compose -f docker-compose.dev.yml up -d`

#### Hosts

* Windows *

In an Administrator privilleged text editor, open the `C:\Windows32\drives\etc\hosts` file and add the following entries:

```
127.0.0.1 mp-ngrok.local
127.0.0.1 mp-matomo.local
127.0.0.1 mp-prometheus.local
127.0.0.1 mp-hasura.local
127.0.0.1 mp-api.local
127.0.0.1 mp-stonks.local
```

* Unix/Mac OS*

In a `sudo` text editor, open `/etc/hosts` and add the following entries:

```
127.0.0.1 mp-ngrok.local
127.0.0.1 mp-matomo.local
127.0.0.1 mp-prometheus.local
127.0.0.1 mp-hasura.local
127.0.0.1 mp-api.local
127.0.0.1 mp-stonks.local
```

### Available npm commands

- `npm run start` - start the Docker compose project
- `npm run stop` - stop and pull down the Docker compose project
- `npm run build` - build the Docker compose project
- `npm run recycle` - stop, down, build, start the Docker compose project
- `npm run db:init` - initialize the db, only useful when initially setting up the project
- `npm run db:migrate` - create a new migration for the database against the `db` container
- `npm run db:update` - apply all pending updates to a running `db` container
- `npm run test` - run the entire server test suite
- `npm run test:focus` - run tests marked with `@pytest.mark.focus`, useful for isolating troublesome tests
- `npm run gendoc` - run the OpenAPI spec generation on a running API
- `npm run clean` - remove all local pycache and pre-compiled Python objects

The `start`, `stop`, `build`, and `recycle` tasks have `:prod` variants that can be used to stand up the application
in production mode. This is useful for testing behavioral differences when running locally vs. prod, however the prod
`docker-compose.prod.yml` file won't create a local DB, so ensure your `.env.dev` file is pointing to a valid and accessible
Money Printer development database server.

## Deploying

TBD