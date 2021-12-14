import os
from typing import Union, Optional

import pandas as pd

from core.stores.mysql import MySql
from core.lib.logger import get_logger
from core.lib.types import StringList
from config import iex_config, mysql_config

# import all the actions so that consumers of the repo can access everything
from core.lib.utilities import wrap
from core.lib.actions.stock.crud import *
from core.lib.actions.stock.fetch import *


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
        self.on_iex_blacklist = wrap(on_iex_blacklist, self)
        self.get_historical_daily_security_prices = wrap(get_historical_daily_security_prices, self)
        self.get_historical_intraday_security_prices = wrap(get_historical_intraday_security_prices, self)
        self.fetch_historical_daily = wrap(fetch_historical_daily, self)
        self.fetch_historical_intraday = wrap(fetch_historical_intraday, self)
        self.create_historical_daily_security_price = wrap(create_historical_daily_security_price, self)
        self.create_historical_intraday_security_price = wrap(create_historical_intraday_security_price, self)

    def historical_daily(self, symbol: str, start: datetime = None, end: datetime = None, close_only: bool = False)\
            -> Optional[pd.DataFrame]:
        """
        Gets the closing prices for the given symbol and the given time frame
        Defaults to the last 30 days
        """
        if symbol is None:
            return None
        if self.on_iex_blacklist(symbol):
            return None
        stored = self.get_historical_daily_security_prices(symbol, start=start)
        if stored and len(stored) > 0:
            self.logger.debug("found data in store already, returning existing data")
            return self._to_dataframe(stored)
        data = self.fetch_historical_daily(symbol, start=start, end=end, close_only=close_only)
        if data is not None and len(data) > 0:
            self.create_historical_daily_security_price(symbol, data)
        else:
            self.logger.warning("upstream didn't return an error, but it did return an empty dataset, symbol: "
                                "{0}, start: {1}, end: {2}".format(symbol, start, end))
        return data

    def historical_daily_all(self, symbols: StringList, start=None, end=None, close_only=False) -> pd.DataFrame:
        """
        Gets the closing prices for the given list of symbols and the given time frame
        Defaults to the last 30 days for each symbol
        """
        symbol_data = pd.DataFrame()
        for symbol in symbols:
            symbol_data = symbol_data.append(
                self.historical_daily(symbol, start, end, close_only)
            )
        return symbol_data

    def historical_intraday(self, symbol: str, start: datetime = None) -> Optional[pd.DataFrame]:
        """
        Gets the intraday prices for the given symbol, from the given start date to now
        This is limited to pulling the last 90 days of per-minute intraday data
        """
        if symbol is None:
            return None
        if self.on_iex_blacklist(symbol):
            return None
        stored = self.get_historical_intraday_security_prices(symbol, start=start)
        if stored and len(stored) > 0:
            self.logger.debug("found data in store already, returning existing data")
            return self._to_dataframe(stored)
        self.logger.debug("local db miss, fetching time period from upstream")
        data = self.fetch_historical_intraday(symbol, start=start)
        if data is not None and len(data) > 0:
            self.create_historical_intraday_security_price(symbol, data)
        else:
            self.logger.warning("upstream didn't return an error, but it did return an empty dataset, "
                                "symbol: {0} start: {1}" .format(symbol, start))
        return data

    def previous(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        Gets the previous day's price for the given symbol
        """
        if symbol is None:
            return None
        if self.on_iex_blacklist(symbol):
            return
        start = datetime.today() - timedelta(days=1)
        # if the start is a weekend, walk it back to the last trading day
        start = get_last_bus_day(start)
        stored = self.get_historical_daily_security_prices(symbol, start)
        if stored and len(stored) > 0:
            self.logger.debug("found data in store already, returning existing data")
            return self._to_dataframe(stored)
        data = self.fetch_historical_daily(symbol, start=start)
        if data is not None and len(data) > 0:
            self.create_historical_daily_security_price(symbol, data)
        else:
            self.logger.warning("upstream didn't return an error, but it did return an empty dataset, " +
                                "symbol: {0}, start: {1}" .format(symbol, start))
            # ok, so we can't fetch the price for today, and we dont have todays price in the db
            # so just return the latest price for this symbol that we do have
            last = self.db.with_session(lambda session: session.query(SecurityPrice)
                                        .where(SecurityPrice.symbol == symbol)
                                        .order_by(SecurityPrice.date.desc()).first()
                                        )
            self.logger.warning("last effort to find a price, found last price in db: {0}".format(last))
            if last is not None:
                return self._to_dataframe(last)
        return data

    def has_data(self, symbol: str) -> bool:
        """
        Does this symbol have any price data?
        """
        return self.db.with_session(lambda session: session.query(SecurityPrice)
                                    .filter(SecurityPrice.symbol == symbol).count() > 0
                                    )

    def has_data_point(self, symbol: str, resolution: str, timestamp: datetime) -> bool:
        """
        Does this symbol have this resolution datapoint for this timestamp?
        """
        if resolution == 'intraday':
            return self.db.with_session(lambda session: session.query(SecurityPrice)
                                        .filter(and_(
                                            SecurityPrice.symbol == symbol,
                                            SecurityPrice.date == timestamp
                                        )).count() > 0
                                        )
        if resolution == 'daily':
            return self.db.with_session(lambda session: session.query(SecurityPrice)
                                        .filter(and_(
                                            SecurityPrice.symbol == symbol,
                                            SecurityPrice.date == timestamp.date()
                                        )).count() > 0
                                        )

    def _to_dataframe(self, data: Union[SecurityPrice, SecurityPriceList]) -> pd.DataFrame:
        """
        Converts a given SecurityPrice or list of SecurityPrices into a Pandas DataFrame
        """
        if type(data) == list:
            return pd.DataFrame.from_records([d.to_dict() for d in data])
        return pd.DataFrame.from_records([data.to_dict()])
