import os
from typing import Union, Optional
from marshmallow import Schema, fields, EXCLUDE

import pandas as pd

from core.stores.mysql import MySql
from core.lib.logger import get_logger
from core.lib.types import StringList
from config import iex_config, mysql_config
from core.repositories.repository_response import RepositoryResponse
from core.schemas.security_schemas import ReadSecurityPriceSchema

# import all the actions so that consumers of the repo can access everything
from core.lib.utilities import wrap
from core.actions.stock.crud import *
from core.actions.stock.fetch import *


class RequestStockPriceSchema(Schema):
    class Meta:
        fields = ("symbol", "start", "end", "close_only")


class RequestStockPriceListSchema(Schema):
    class Meta:
        fields = ("symbols", "start", "end", "close_only")


class StockRepository:

    logger = get_logger(__name__)
    db = MySql(mysql_config)

    def __init__(self):
        # pull the IEX config and store the token in the IEX_TOKEN env var
        secret = iex_config['secret']
        os.environ['IEX_TOKEN'] = secret
        if iex_config['env'] == 'sandbox':
            os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
        self._init_facets()

    def _init_facets(self):
        self.on_iex_blacklist = wrap(on_iex_blacklist, self.db)
        self.get_historical_daily_security_prices = wrap(
            get_historical_daily_security_prices, self.db)
        self.get_historical_intraday_security_prices = wrap(
            get_historical_intraday_security_prices, self.db)
        self.fetch_historical_daily = wrap(fetch_historical_daily, self.db)
        self.fetch_historical_intraday = wrap(
            fetch_historical_intraday, self.db)
        self.create_historical_daily_security_price = wrap(
            create_historical_daily_security_price, self.db)
        self.create_historical_intraday_security_price = wrap(
            create_historical_intraday_security_price, self.db)

    def historical_daily(self, request: RequestStockPriceSchema) -> RepositoryResponse:
        """
        Gets the closing prices for the given symbol and the given time frame
        Defaults to the last 30 days
        """
        symbol = request['symbol']
        start = request['start']
        end = request['end']
        close_only = request['close_only']

        if self.on_iex_blacklist(symbol):
            return RepositoryResponse(
                success=False,
                message=f"Symbol {symbol} is on IEX blacklist"
            )
        stored = self.get_historical_daily_security_prices(symbol, start=start)
        if stored and len(stored) > 0:
            self.logger.debug(
                "found data in store already, returning existing data")
            return self._to_dataframe(stored)
        data = self.fetch_historical_daily(
            symbol, start=start, end=end, close_only=close_only)
        if data is not None and len(data) > 0:
            self.create_historical_daily_security_price(symbol, data)
        else:
            self.logger.warning("upstream didn't return an error, but it did return an empty dataset, symbol: "
                                "{0}, start: {1}, end: {2}".format(symbol, start, end))

        return RepositoryResponse(
            success=data is not None,
            data=data,
            message=f"No stock price data found locally or in remote upstream" if data is None else None
        )

    def historical_daily_all(self, request: RequestStockPriceListSchema) -> RepositoryResponse:
        """
        Gets the closing prices for the given list of symbols and the given time frame
        Defaults to the last 30 days for each symbol
        """
        symbol_data = pd.DataFrame()
        for symbol in request['symbols']:
            symbol_data = symbol_data.append(
                self.historical_daily(RequestStockPriceSchema(unknown=EXCLUDE).load({
                    **{'symbol': symbol}, **request
                }))
            )

        return RepositoryResponse(
            success=True,
            data=symbol_data
        )

    def historical_intraday(self, request: RequestStockPriceSchema) -> RepositoryResponse:
        """
        Gets the intraday prices for the given symbol, from the given start date to now
        This is limited to pulling the last 90 days of per-minute intraday data
        """
        if self.on_iex_blacklist(request['symbol']):
            return RepositoryResponse(
                success=False,
                data=f"Symbol {request['symbol']} cannot be resolved with IEX as configured"
            )

        stored = self.get_historical_intraday_security_prices(
            request['symbol'], start=request['start'])

        if stored and len(stored) > 0:
            self.logger.debug(
                "found data in store already, returning existing data")
            return RepositoryResponse(
                success=True,
                data=self._to_dataframe(stored)
            )

        self.logger.debug("local db miss, fetching time period from upstream")
        data = self.fetch_historical_intraday(
            request['symbol'], start=request['start'])

        if data is not None and len(data) > 0:
            self.create_historical_intraday_security_price(
                request['symbol'], data)
        else:
            self.logger.warning("upstream didn't return an error, but it did return an empty dataset, "
                                "symbol: {0} start: {1}" .format(request['symbol'], request['start']))

        return RepositoryResponse(
            success=data is not None,
            data=data,
            message=f"Could not find data for symbol {request['symbol']} locally or in upstream" if data is None else None
        )

    def previous(self, symbol: str) -> RepositoryResponse:
        """
        Gets the previous day's price for the given symbol
        """
        if symbol is None or symbol == "":
            return RepositoryResponse(
                success=False,
                message="Symbol cannot be None or empty"
            )

        if self.on_iex_blacklist(symbol):
            return RepositoryResponse(
                success=False,
                data=f"Symbol {symbol} cannot be resolved with IEX as configured"
            )

        start = datetime.today() - timedelta(days=1)
        # if the start is a weekend, walk it back to the last trading day
        start = get_last_bus_day(start)

        stored = self.get_historical_daily_security_prices(symbol, start)
        if stored and len(stored) > 0:
            self.logger.debug(
                "found data in store already, returning existing data")
            return RepositoryResponse(
                success=True,
                data=self._to_dataframe(stored)
            )

        data = self.fetch_historical_daily(symbol, start=start)
        if data is not None and len(data) > 0:
            self.create_historical_daily_security_price(symbol, data)
        else:
            self.logger.warning("upstream didn't return an error, but it did return an empty dataset, " +
                                "symbol: {0}, start: {1}" .format(symbol, start))
            # ok, so we can't fetch the price for today, and we dont have todays price in the db
            # so just return the latest price for this symbol that we do have
            with self.db.get_session() as session:
                last = session.query(SecurityPrice).where(
                    SecurityPrice.symbol == symbol).order_by(
                        SecurityPrice.date.desc()).first()
            self.logger.warning(
                "last effort to find a price, found last price in db: {0}".format(last))
            if last is not None:
                data = self._to_dataframe(last)

        return RepositoryResponse(
            success=data is not None,
            data=data,
            message=f"Could not find data for symbol {symbol} locally or in upstream" if data is None else None
        )

    def has_data(self, symbol: str) -> bool:
        """
        Does this symbol have any price data?
        """
        with self.db.get_session() as session:
            return session.query(SecurityPrice).filter(SecurityPrice.symbol == symbol).count() > 0

    def _to_dataframe(self, data: Union[SecurityPrice, list]) -> pd.DataFrame:
        """
        Converts a given SecurityPrice or list of SecurityPrices into a Pandas DataFrame
        """
        return pd.DataFrame.from_records([ReadSecurityPriceSchema(many=type(data) == list).dumps(data)])
