# Money Printer Core

The core code library for the Money Printer.

This is where all the data models, business logic and financial tooling is maintained. This project is designed to be
free of dependencies on other Money Printer projects, and only require dependencies to the 3rd party services used to
provide core functionality to the application.

### alembic

Contains all the data modelling scaffold for the SQL based storage for Money Printer. Obviously leverages Alembic.

### apis

Contains API code used to interact with 3rd party services. Currently supports:

- Plaid
- IEX
- Google Alerts (partially and broken)
- Mailgun
- Yahoo Finance (partially)

### lib

Business logic and financial tooling code. Some of the functionality support includes:

- Stock fundamentals analysis
- Options modeling using Black-Scholes model
- Various technical oscillators, including Stochastic, MACD, RSI, EMA

### models

The model definitions for `alembic`

### repositories

A repository pattern implementation for the Money Printer, encapsulating all the commonly performed actions by various
components of the Money Printer

### stores

Backing stores for data. Right now it only supports MySQL.

### templates

Notification templates for the `Mailgun` integration.