import os
from pandas import DataFrame
from datetime import time, date, timedelta
from iexfinance.stocks import get_historical_data, get_historical_intraday

from core.stores.mysql import MySql


def get_repository():
    from server.services.api import load_config
    app_config = load_config()
    repo = StockRepository(StockRepositoryConfig(
        iex_config=app_config['iexcloud'],
        mysql_config=app_config['db']
    ))
    return repo


class StockRepositoryConfig(object):

    def __init__(self, iex_config, mysql_config):
        self.iex_config = iex_config
        self.mysql_config = mysql_config


class StockRepository:

    def __init__(self, config):
        # pull the IEX config and store the token in the IEX_TOKEN env var
        secret = config.iex_config['secret']
        mysql_config = config.mysql_config
        os.environ['IEX_TOKEN'] = secret
        db = MySql(mysql_config)
        self.db = db.get_session()

    # gets historical prices for the given symbol
    # defaults to the last 30 days of closing prices only
    # start and end dates can be specified for custom date ranges
    # close_only can be set to false to pull other data points for that symbol/date
    # returns a pandas DataFrame
    def historical_daily(self, symbol, start=None, end=None, close_only=True):
        stored = self.__get_stored_historical_daily(symbol, start=start)
        if stored is not None:
            return self.__to_dataframe(stored)
        return self.__fetch_historical_daily(symbol, start=start)

    # looks in the DB store to see if we have these historical data already
    # if so, return our local version
    # if not, fetch from the upstream API the store locally
    def __get_stored_historical_daily(self, symbol, start=None, end=None, close_only=True):
        return None

    def __fetch_historical_daily(self, symbol, start=None, end=None, close_only=True):
        start = start or date.today()
        end = end or start - timedelta(days=30)
        df = get_historical_data(symbol, start=start, end=end, close_only=close_only)
        return df

    # gets historical intraday prices for the given symbol
    # defaults to the last day
    # start date can be specified for custom date ranges (within the last 90 days)
    # returns a pandas DataFrame
    def historical_intraday(self, symbol, start=None):
        stored = self.__get_stored_historical_intraday(symbol, start=start)
        if stored is not None:
            return self.__to_dataframe(stored)
        return self.__fetch_historical_intraday(symbol, start=start)

    # looks in the DB store to see if we have these historical intraday data already
    # if so, return our local version
    # if not, fetch from the upstream API the store locally
    def __get_stored_historical_intraday(self, symbol, start=None):
        return None

    def __fetch_historical_intraday(self, symbol, start=None):
        start = start or date.today() - timedelta(days=1)
        df = get_historical_intraday(symbol, start)
        return df

    def __to_dataframe(self, data):
        return data

