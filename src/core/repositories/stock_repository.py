import os
from datetime import timedelta, datetime, timezone
import traceback

import pandas as pd
from sqlalchemy import and_
from iexfinance.stocks import get_historical_data, get_historical_intraday
from iexfinance.utils.exceptions import IEXQueryError
import numpy as np

from core.stores.mysql import MySql
from core.models.security import Security
from core.models.security_price import SecurityPrice
from core.models.iex_blacklist import IexBlacklist
from core.lib.logger import get_logger


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
        self.logger = get_logger(__name__)
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
    def historical_daily(self, symbol, start=None, end=None, close_only=False):
        if symbol is None:
            return
        if self.__on_iex_blacklist(symbol):
            return
        stored = self.__get_stored_historical_daily(symbol, start=start)
        if self.__verify_daily_dataset(stored, start=start, end=end):
            self.logger.debug("found data in store already, returning existing data")
            return self.__to_dataframe(stored)
        data = self.__fetch_historical_daily(symbol, start=start, end=end, close_only=close_only)
        if data is not None and len(data) > 0:
            self.__store_historical_daily(symbol, data)
        else:
            self.logger.warning(" * upstream didn't return an error, but it did return an empty dataset, symbol: {0}, start: {1}, end: {2}".format(symbol, start, end))
        return data

    def historical_daily_all(self, symbols, start=None, end=None, close_only=False):
        symbol_data = []
        for symbol in symbols:
            symbol_data.append(
                self.historical_daily(symbol, start, end, close_only)
            )
        return symbol_data

    # gets historical intraday prices for the given symbol
    # defaults to the last day
    # start date can be specified for custom date ranges (within the last 90 days)
    # returns a pandas DataFrame
    def historical_intraday(self, symbol, start=None):
        if symbol is None:
            return
        if self.__on_iex_blacklist(symbol):
            return
        stored = self.__get_stored_historical_intraday(symbol, start=start)
        if self.__verify_intraday_dataset(stored, start):
            self.logger.debug("found data in store already, returning existing data")
            return self.__to_dataframe(stored)
        data = self.__fetch_historical_intraday(symbol, start=start)
        if data is not None and len(data) > 0:
            self.__store_historical_intraday(symbol, data)
        else:
            self.logger.warning("upstream didn't return an error, but it did return an empty dataset, symbol: {0} start: {1}" .format(symbol, start))
        return data

    # gets the previous trading day's prices for the given symbol
    def previous(self, symbol):
        if symbol is None:
            return None
        if self.__on_iex_blacklist(symbol):
            return
        start = datetime.today() - timedelta(days=1)
        # if the start is a weekend, walk it back to the last trading day
        start = self.__get_last_bus_day(start)
        stored = self.__get_stored_historical_daily(symbol, start)
        if stored and len(stored) > 0 and self.__verify_daily_dataset(stored, start, datetime.today()):
            self.logger.debug("found data in store already, returning existing data")
            return self.__to_dataframe(stored)
        data = self.__fetch_historical_daily(symbol, start=start)
        if data is not None and len(data) > 0:
            self.__store_historical_daily(symbol, data)
        else:
            self.logger.warning("upstream didn't return an error, but it did return an empty dataset, " +
                                "symbol: {0}, start: {1}" .format(symbol, start))
            # ok, so we can't fetch the price for today, and we dont have todays price in the db
            # so just return the latest price for this symbol that we do have
            last = self.db.query(SecurityPrice).where(SecurityPrice.symbol == symbol)\
                .order_by(SecurityPrice.date.desc()).first()
            self.logger.warning("last effort to find a price, found last price in db: {0}".format(last))
            if last is not None:
                return self.__to_dataframe(last)
        return data

    # looks in the DB store to see if we have these historical intraday data already
    # if so, return our local version
    # if not, fetch from the upstream API the store locally
    def __get_stored_historical_intraday(self, symbol, start=None):
        self.logger.debug("searching db intraday resolution symbol/s for {0} from {1} to now".format(symbol, start))
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
        self.logger.debug(" * searching db daily resolution symbol/s for {0} from {1} - {2}".format(symbol, start, end))
        records = self.db.query(SecurityPrice).filter(and_(
            SecurityPrice.symbol == symbol,
            SecurityPrice.resolution == "daily",
            start is None or SecurityPrice.date >= start,
            end is None or SecurityPrice.date <= end,
        )).all()
        return records

    def __store_historical_intraday(self, symbol, dfs):
        return self.__store_stock_price(symbol, "intraday", dfs)

    def __store_historical_daily(self, symbol, dfs):
        return self.__store_stock_price(symbol, "daily", dfs)

    def has_data(self, symbol):
        return self.db.query(SecurityPrice).filter(
            SecurityPrice.symbol == symbol
        ).count() > 0

    def has_data_point(self, symbol, resolution, timestamp):
        if resolution == 'intraday':
            return self.db.query(SecurityPrice).filter(and_(
                SecurityPrice.symbol == symbol,
                SecurityPrice.date == timestamp
            )).count() > 0
        if resolution == 'daily':
            return self.db.query(SecurityPrice).filter(and_(
                SecurityPrice.symbol == symbol,
                SecurityPrice.date == timestamp.date()
            )).count() > 0

    def __store_stock_price(self, symbol, resolution, dfs):
        records = []
        indices = dfs.to_dict(orient='index')
        for date_index in indices:
            df = indices[date_index]

            # we're tracking this time period already, ignore it
            if not self.has_data_point(symbol, resolution, date_index):
                price = SecurityPrice()

                # guaranteed data
                price.symbol = symbol
                price.high = self.__sanitize_float(df['high'])
                price.low = self.__sanitize_float(df['low'])
                price.open = self.__sanitize_float(df['open'])
                price.close = self.__sanitize_float(df['close'])
                price.volume = int(df['volume'])
                price.date = self.__local_to_utc(date_index)
                price.resolution = resolution
                price.timestamp = datetime.utcnow()

                # data that seems to be optional based on endpoint
                if 'uHigh' in df: price.u_high = self.__sanitize_float(df['uHigh'])
                if 'uLow' in df: price.u_low = self.__sanitize_float(df['uLow'])
                if 'uOpen' in df: price.u_open = self.__sanitize_float(df['uOpen'])
                if 'uClose' in df: price.u_close = self.__sanitize_float(df['uClose'])
                if 'uVolume' in df: price.u_volume = self.__sanitize_float(df['uVolume'])
                if 'change' in df: price.change = self.__sanitize_float(df['change'])
                if 'changePercent' in df: price.change_percent = self.__sanitize_float(df['changePercent'])
                if 'changeOverTime' in df: price.change_over_time = self.__sanitize_float(df['changeOverTime'])
                if 'marketChangeOverTime' in df: price.market_change_over_time = self.__sanitize_float(df['marketChangeOverTime'])

                self.db.add(price)
                self.db.commit()

                records.append(price)

        return records

    def __fetch_historical_daily(self, symbol, start=None, end=None, close_only=False):
        if start is None:
            start = self.__get_last_bus_day(datetime.today() - timedelta(days=30))
        if end is None:
            end = self.__get_last_bus_day(datetime.today())
        self.logger.info("fetching historical daily prices for symbol {0}, {1} - {2} from upstream"
                         .format(symbol, start, end))
        try:
            df = get_historical_data(symbol,
                                     start=start,
                                     end=end,
                                     close_only=close_only)
            return df
        except IEXQueryError as ex:
            if ex.status == 404:
                self.logger.warning("upstream provider couldn't resolve symbol {0}".format(symbol))
                self.__add_to_iex_blacklist(symbol)
            return None
        except Exception:
            self.logger.exception("unexpected error from upstream provider fetching for symbol {0}: {1}"
                  .format(symbol, traceback.format_exc()))
            return None

    def __fetch_historical_intraday(self, symbol, start=None):
        start = start or datetime.today() - timedelta(days=7)
        today = datetime.today()
        try:
            days = min((today - start).days, 1)
            total_df = pd.DataFrame()
            for i in range(days+1):
                fetch_date = start + timedelta(days=i)
                self.logger.info("fetching historical intraday prices for symbol {0} on {1} from upstream".format(symbol, fetch_date))
                df = get_historical_intraday(symbol, date=fetch_date)
                total_df = total_df.append(df)
            return total_df
        except IEXQueryError as ex:
            if ex.status == 404:
                self.logger.warning("upstream provider couldn't resolve symbol {0}".format(symbol))
                self.__add_to_iex_blacklist(symbol)
            return None
        except Exception:
            self.logger.exception("unexpected error from upstream provider fetching for symbol {0}: {1}"
                  .format(symbol, traceback.format_exc()))
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

    def __to_dataframe(self, data):
        if type(data) == list:
            return pd.DataFrame.from_records([d.to_dict() for d in data])
        return pd.DataFrame.from_records([data.to_dict()])

    def __add_tz(self, val):
        if val is None:
            return val
        local_tz = datetime.now(timezone.utc).astimezone().tzinfo
        return val.replace(tzinfo=local_tz)

    def __local_to_utc(self, val):
        if val is None:
            return val
        tz_val = self.__add_tz(val)
        utc_val = tz_val.astimezone(tz=timezone.utc)
        return utc_val

    def __verify_daily_dataset(self, dataset, start, end):
        return len(dataset) > 0
        # the below doesnt work because it doesnt take into account trading holidays
        # it's always false, always making us double fetch our data
        # days = np.busday_count(start, end)
        # return len(dataset) >= days

    def __verify_intraday_dataset(self, dataset, start):
        # todo - figure out this
        return len(dataset) > 0

    def __sanitize_float(self, val):
        if np.isnan(val):
            return 0
        return float(val)

    def __get_last_bus_day(self, date):
        return np.busday_offset(date.date(), 0, roll='backward').astype(datetime)

