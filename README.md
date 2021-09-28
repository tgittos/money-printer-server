# Money Printer

There's a not-so-invisible class war currently in progress in the US. It's the 1% vs the rest
of us. What's a lone person to do in such a world? How can you fight back in a system that's
rigged against you?

You print money. If you can't beat 'em, join 'em.

Money Printer aims to help you with that.

Money Printer is most accurately a personal wealth modeling platform, but that's not as catchy
'Money Printer'.

With Money Printer, you can:

- sync financial account balances and investment holdings
- live monitor investment holding price and performance
- perform fundamental & technical analysis on securities and derivatives (options only for now)
  to help screen investment decisions
- perform return analysis on holdings to identify best and worst performers
- perform probabilistic forecasting on current holdings to identify possible outcomes
- perform simulations on virtual holdings to plan future investments

In a nutshell, think Credit Karma, but for your investment performance instead of your credit score.

## Installation

Money Printer is available as a docker image, see [`tgittos/money-printer`](https://hub.docker.com/repository/docker/tgittos/money-printer) for tags and details

## Development

Money Printer consists of two main applications:

- `client` - a nodejs client built with React
- `server` - a Python server that hosts a RESTful API with websocket support

Details on setting up and working in the individual projects are in their respective `README` files

## Support

Right now support is minimal given how private this project is. Just email [hi@timgittos](mailto:hi@timgittos.com) with
questions and issues.