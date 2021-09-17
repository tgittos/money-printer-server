import os
from datetime import time, date, timedelta, datetime, timezone
import pytz
import traceback

from pandas import DataFrame
from sqlalchemy import and_
from iexfinance.stocks import get_historical_data, get_historical_intraday
from iexfinance.utils.exceptions import IEXQueryError
import numpy as np

from core.stores.mysql import MySql
from core.models.security import Security
from core.models.security_price import SecurityPrice
from core.models.iex_blacklist import IexBlacklist


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
        if self.__on_iex_blacklist(symbol):
            return
        if security_id is None:
            security = self.db.query(Security).where(Security.ticker_symbol == symbol).first()
            if security is None:
                raise Exception("could not find tracked security for requested symbol", symbol)
            security_id = security.id
        stored = self.__get_stored_historical_daily(symbol, start=start)
        if self.__verify_daily_dataset(stored, start, end):
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
        if self.__on_iex_blacklist(symbol):
            return
        if security_id is None:
            security = self.db.query(Security).where(Security.ticker_symbol == symbol).first()
            if security is None:
                raise Exception("could not find tracked security for requested symbol", symbol)
            security_id = security.id
        stored = self.__get_stored_historical_intraday(symbol, start=start)
        if self.__verify_intraday_dataset(stored, start):
            print(" * found data in store already, returning existing data", flush=True)
            return self.__to_dataframe(stored)
        data = self.__fetch_historical_intraday(symbol, start=start)
        if data is not None and len(data) > 0:
            self.__store_historical_intraday(security_id, symbol, data)
        return data

    # gets the previous trading day's prices for the given symbol
    def previous(self, symbol, security_id=None):
        if symbol is None:
            return None
        if self.__on_iex_blacklist(symbol):
            return
        if security_id is None:
            security = self.db.query(Security).where(Security.ticker_symbol == symbol).first()
            if security is None:
                raise Exception("could not find tracked security for requested symbol", symbol)
            security_id = security.id
        start = datetime.utcnow() - timedelta(days=1)
        stored = self.__get_stored_historical_daily(symbol, start)
        if self.__verify_daily_dataset(stored, start.date(), datetime.utcnow().date()):
            print(" * found data in store already, returning existing data", flush=True)
            return self.__to_dataframe(stored)
        data = self.__fetch_historical_daily(symbol, start=start.timestamp())
        if data is not None and len(data) > 0:
            self.__store_historical_daily(security_id, symbol, data)
        return data

    # returns if we have any data for this symbol
    def has_data(self, symbol) -> bool:
        return self.db.query(SecurityPrice).filter(SecurityPrice.symbol == symbol).count() > 0

    # looks in the DB store to see if we have these historical intraday data already
    # if so, return our local version
    # if not, fetch from the upstream API the store locally
    def __get_stored_historical_intraday(self, symbol, start=None):
        print(" * searching db intraday resolution symbol/s for {0} from {1} to now".format(symbol, start))
        records = self.db.query(SecurityPrice).filter(and_(
            SecurityPrice.symbol == symbol,
            SecurityPrice.resolution == "intraday",
            start is None or SecurityPrice.date >= start
        )).all()
        return records

    # looks in the DB store to see if we have these historical data already
    # if so, return our local version
    # if not, fetch from the upstream API the store locally
    def __get_stored_historical_daily(self, symbol, start=None, end=None):
        real_start = start
        if start is not None:
            real_start = start.date()
        real_end = end
        if end is not None:
            real_end = end.date()
        print(" * searching db daily resolution symbol/s for {0} from {1} - {2}".format(symbol, real_start, real_end))
        records = self.db.query(SecurityPrice).filter(and_(
            SecurityPrice.symbol == symbol,
            SecurityPrice.resolution == "daily",
            real_start is None or SecurityPrice.date >= real_start,
            real_end is None or SecurityPrice.date <= real_end,
        )).all()
        return records

    def __store_historical_intraday(self, security_id, symbol, dfs):
        return self.__store_stock_price(security_id, symbol, "intraday", dfs)

    def __store_historical_daily(self, security_id, symbol, dfs):
        return self.__store_stock_price(security_id, symbol, "daily", dfs)

    def __store_stock_price(self, security_id, symbol, resolution, dfs) -> SecurityPrice:
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

    def __fetch_historical_daily(self, symbol, start=None, end=None, close_only=False) -> DataFrame:
        end = end is not None and datetime.fromtimestamp(end) or (datetime.utcnow() - timedelta(minutes=15))
        start = start is not None and datetime.fromtimestamp(start) or end - timedelta(days=30)
        real_start = self.__utc_to_eastern(start).date()
        real_end = self.__utc_to_eastern(end).date()
        print(" * fetching historical daily prices for symbol {0}, {1} - {2}".format(symbol, real_start, real_end), flush=True)
        try:
            df = get_historical_data(symbol,
                                     start=real_start,
                                     end=real_end,
                                     close_only=close_only)
            return df
        except IEXQueryError as ex:
            if ex.status == 404:
                print(" * upstream provider couldn't resolve symbol {0}".format(symbol), flush=True)
                self.__add_to_iex_blacklist(symbol)
            return None
        except Exception:
            print(" * unexpected error from upstream provider fetching for symbol {0}: {1}"
                  .format(symbol, traceback.format_exc()), flush=True)
            return None

    def __fetch_historical_intraday(self, symbol, start=None) -> DataFrame:
        start = datetime.fromtimestamp(start) or (datetime.utcnow() - timedelta(minutes=5))
        print(" * fetching historical intraday prices for symbol {0} since {1}".format(symbol, start), flush=True)
        try:
            # convert dates from default utc to ET
            df = get_historical_intraday(symbol, date=self.__utc_to_eastern(start))
            return df
        except IEXQueryError as ex:
            if ex.status == 404:
                print(" * upstream provider couldn't resolve symbol {0}".format(symbol), flush=True)
                self.__add_to_iex_blacklist(symbol)
            return None
        except Exception:
            print(" * unexpected error from upstream provider fetching for symbol {0}: {1}"
                  .format(symbol, traceback.format_exc()), flush=True)
            return None

    def __add_to_iex_blacklist(self, symbol):
        if self.__on_iex_blacklist(symbol):
            return None
        iex_bl = IexBlacklist()
        iex_bl.symbol = symbol
        iex_bl.timestamp = datetime.utcnow()
        self.db.add(iex_bl)
        self.db.commit()
        return None

    def __on_iex_blacklist(self, symbol):
        return self.db.query(IexBlacklist).filter(IexBlacklist.symbol == symbol).count() == 1

    def __to_dataframe(self, data) -> DataFrame:
        if type(data) == list:
            return DataFrame.from_records([d.to_dict() for d in data])
        return DataFrame.from_dict(data.to_dict())

    def __utc_to_eastern(self, date):
        # convert UTC to Eastern
        # tz_aware = date.replace(tzinfo=timezone.utc).astimezone(tz=pytz.timezone('America/New_York'))
        # convert UTC to server local
        tz_aware = date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        # remove TZ info, retaining raw date val
        tz_naiive = tz_aware.replace(tzinfo=None)
        return tz_naiive

    def __verify_daily_dataset(self, dataset, start, end):
        days = np.busday_count(start, end)
        return len(dataset) >= days

    def __verify_intraday_dataset(self, dataset, start):
        # todo - figure out this
        return len(dataset) > 0

