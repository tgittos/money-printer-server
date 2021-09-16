import os
from datetime import time, date, timedelta, datetime

from pandas import DataFrame
from sqlalchemy import and_
from iexfinance.stocks import get_historical_data, get_historical_intraday
from iexfinance.utils.exceptions import IEXQueryError

from core.stores.mysql import MySql
from core.models.security import Security
from core.models.security_price import SecurityPrice


def get_repository(iex_config, mysql_config):
    repo = StockRepository(StockRepositoryConfig(
        iex_config=iex_config,
        mysql_config=mysql_config
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
        if config.iex_config['env'] == 'sandbox':
            os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
        db = MySql(mysql_config)
        self.db = db.get_session()

    # gets historical prices for the given symbol
    # defaults to the last 30 days of closing prices only
    # start and end dates can be specified for custom date ranges
    # close_only can be set to false to pull other data points for that symbol/date
    # returns a pandas DataFrame
    def historical_daily(self, symbol, security_id=None, start=None, end=None, close_only=False):
        if symbol is None:
            return
        if security_id is None:
            security = self.db.query(Security).where(Security.ticker_symbol == symbol).first()
            if security is None:
                raise Exception("could not find tracked security for requested symbol", symbol)
            security_id = security.id
        stored = self.__get_stored_historical_daily(symbol, start=start)
        if len(stored) > 0:
            print(" * found data in store already, returning existing data", flush=True)
            return self.__to_dataframe(stored)
        data = self.__fetch_historical_daily(symbol, start=start, end=end, close_only=close_only)
        if data is not None and len(data) > 0:
            self.__store_historical_daily(security_id, symbol, data)
        return data

    # gets historical intraday prices for the given symbol
    # defaults to the last day
    # start date can be specified for custom date ranges (within the last 90 days)
    # returns a pandas DataFrame
    def historical_intraday(self, symbol, security_id=None, start=None):
        if symbol is None:
            return
        if security_id is None:
            security = self.db.query(Security).where(Security.ticker_symbol == symbol).first()
            if security is None:
                raise Exception("could not find tracked security for requested symbol", symbol)
            security_id = security.id
        stored = self.__get_stored_historical_intraday(symbol, start=start)
        if len(stored) > 0:
            print(" * found data in store already, returning existing data", flush=True)
            return self.__to_dataframe(stored)
        data = self.__fetch_historical_intraday(symbol, start=start)
        if data is not None and len(data) > 0:
            self.__store_historical_intraday(security_id, symbol, data)
        return data

    # gets the previous trading day's prices for the given symbol
    def previous(self, symbol, security_id=None):
        if symbol is None:
            return
        if security_id is None:
            security = self.db.query(Security).where(Security.ticker_symbol == symbol).first()
            if security is None:
                raise Exception("could not find tracked security for requested symbol", symbol)
            security_id = security.id
        start = datetime.utcnow() - timedelta(days=1)
        stored = self.__get_stored_historical_daily(symbol, start)
        if stored is not None:
            return self.__to_dataframe(stored)
        data = self.__fetch_historical_daily(symbol, start=start.timestamp())
        if data is not None and len(data) > 0:
            self.__store_historical_daily(security_id, symbol, data)
        return data

    # returns if we have any data for this symbol
    def has_data(self, symbol):
        return self.db.query(SecurityPrice).filter(SecurityPrice.symbol == symbol).count() > 0

    # looks in the DB store to see if we have these historical intraday data already
    # if so, return our local version
    # if not, fetch from the upstream API the store locally
    def __get_stored_historical_intraday(self, symbol, start=None):
        records = self.db.query(SecurityPrice).filter(and_(
            SecurityPrice.symbol == symbol,
            start is None or SecurityPrice.date >= start
        )).all()
        return records

    # looks in the DB store to see if we have these historical data already
    # if so, return our local version
    # if not, fetch from the upstream API the store locally
    def __get_stored_historical_daily(self, symbol, start=None, end=None):
        records = self.db.query(SecurityPrice).filter(and_(
            SecurityPrice.symbol == symbol,
            start is None or SecurityPrice.date >= start,
            end is None or SecurityPrice.date <= end
        )).all()
        return records

    def __store_historical_intraday(self, security_id, symbol, dfs):
        return self.__store_stock_price(security_id, symbol, "intraday", dfs)

    def __store_historical_daily(self, security_id, symbol, dfs):
        return self.__store_stock_price(security_id, symbol, "daily", dfs)

    def __store_stock_price(self, security_id, symbol, resolution, dfs):
        records = []
        indices = dfs.to_dict(orient='index')
        for date_index in indices:
            df = indices[date_index]
            price = SecurityPrice()
            price.security_id = security_id
            price.symbol = symbol
            price.high = df['high']
            price.low = df['low']
            price.open = df['open']
            price.close = df['close']
            price.volume = df['volume']
            if 'uHigh' in df: price.u_high = df['uHigh']
            if 'uLow' in df: price.u_low = df['uLow']
            if 'uOpen' in df: price.u_open = df['uOpen']
            if 'uClose' in df: price.u_close = df['uClose']
            if 'uVolume' in df: price.u_volume = df['uVolume']
            price.date = date_index
            price.change = df['change']
            price.change_percent = df['changePercent']
            price.change_over_time = df['changeOverTime']
            price.market_change_over_time = df['marketChangeOverTime']
            price.resolution = resolution
            price.timestamp = datetime.utcnow()

            self.db.add(price)

            records.append(price)

        self.db.commit()
        return records

    def __fetch_historical_daily(self, symbol, start=None, end=None, close_only=False):
        end = end is not None and datetime.fromtimestamp(end) or date.today()
        start = start is not None and datetime.fromtimestamp(start) or end - timedelta(days=30)
        print(" * fetching historical daily prices for symbol {0}, {1} - {2}".format(symbol, start, end), flush=True)
        try:
            df = get_historical_data(symbol, start=start, end=end, close_only=close_only)
            return df
        except IEXQueryError as ex:
            if ex.status == 404:
                print(" * upstream provider couldn't resolve symbol {0}".format(symbol), flush=True)
            return None
        except Exception:
            print(" * unexpected error from upstream provider fetching for symbol {0}".format(symbol), flush=True)
            return None

    def __fetch_historical_intraday(self, symbol, start=None):
        start = datetime.fromtimestamp(start) or date.today()
        # df = get_historical_intraday(symbol, start)
        print(" * fetching historical intraday prices for symbol {0} since {1}".format(symbol, start), flush=True)
        try:
            df = get_historical_intraday(symbol)
            return df
        except IEXQueryError as ex:
            if ex.status == 404:
                print(" * upstream provider couldn't resolve symbol {0}".format(symbol), flush=True)
            return None
        except Exception:
            print(" * unexpected error from upstream provider fetching for symbol {0}".format(symbol), flush=True)
            return None

    def __to_dataframe(self, data):
        return data
