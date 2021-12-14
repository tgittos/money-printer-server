from datetime import datetime

from pandas import DataFrame
from sqlalchemy import and_

from core.models.security_price import SecurityPrice
from core.models.iex_blacklist import IexBlacklist
from core.lib.utilities import sanitize_float, local_to_utc
from core.lib.types import SecurityPriceList


def create_stock_price(cls, symbol: str, resolution: str, dfs: DataFrame) -> SecurityPriceList:
    """
    Stores a SecurityPrice record in the database from a Pandas DataFrame
    """
    records = []
    indices = dfs.to_dict(orient='index')
    for date_index in indices:
        df = indices[date_index]

        # we're tracking this time period already, ignore it
        if not cls.has_data_point(symbol, resolution, date_index):
            price = SecurityPrice()

            # guaranteed data
            price.symbol = symbol
            price.high = sanitize_float(df['high'])
            price.low = sanitize_float(df['low'])
            price.open = sanitize_float(df['open'])
            price.close = sanitize_float(df['close'])
            price.volume = int(df['volume'])
            price.date = local_to_utc(date_index)
            price.resolution = resolution
            price.timestamp = datetime.utcnow()

            # data that seems to be optional based on endpoint
            if 'uHigh' in df: price.u_high = sanitize_float(df['uHigh'])
            if 'uLow' in df: price.u_low = sanitize_float(df['uLow'])
            if 'uOpen' in df: price.u_open = sanitize_float(df['uOpen'])
            if 'uClose' in df: price.u_close = sanitize_float(df['uClose'])
            if 'uVolume' in df: price.u_volume = sanitize_float(df['uVolume'])
            if 'change' in df: price.change = sanitize_float(df['change'])
            if 'changePercent' in df: price.change_percent = sanitize_float(df['changePercent'])
            if 'changeOverTime' in df: price.change_over_time = sanitize_float(df['changeOverTime'])
            if 'marketChangeOverTime' in df: price.market_change_over_time = sanitize_float(df['marketChangeOverTime'])

            def create(session):
                session.add(price)
                session.commit()

            cls.db.with_session(create)

            records.append(price)

    return records


def get_historical_intraday_security_prices(cls, symbol: str, start: datetime = None) -> SecurityPriceList:
    """
    Searches the database for all per-minute intraday SecurityPrices for a given symbol on a given day
    """
    if hasattr(cls, 'logger'):
        cls.logger.debug("searching db intraday resolution symbol/s for {0} from {1} to now".format(symbol, start))
    records = cls.db.with_session(lambda session: session.query(SecurityPrice)
                                  .filter(and_(
                                      SecurityPrice.symbol == symbol,
                                      SecurityPrice.resolution == "intraday",
                                      start is None or SecurityPrice.date >= start
                                  )).all()
                                  )
    return records


def get_historical_daily_security_prices(cls, symbol: str, start: datetime = None, end: datetime = None) -> SecurityPriceList:
    """
    Searches the database for the daily close SecurityPrices for a given symbol in a given date range
    """
    if hasattr(cls, 'logger'):
        cls.logger.debug("searching db daily resolution symbol/s for {0} from {1} - {2}".format(symbol, start, end))
    records = cls.db.with_session(lambda session: session.query(SecurityPrice)
                                  .filter(and_(
                                      SecurityPrice.symbol == symbol,
                                      SecurityPrice.resolution == "daily",
                                      start is None or SecurityPrice.date >= start,
                                      end is None or SecurityPrice.date <= end,
                                  )).all()
                                  )
    return records


def create_historical_intraday_security_price(cls, symbol: str, dfs: DataFrame) -> SecurityPriceList:
    """
    Creates a day's worth of historical per-minute intraday SecurityPrice from a Pandas DataFrame
    """
    return create_stock_price(cls, symbol, "intraday", dfs)


def create_historical_daily_security_price(cls, symbol: str, dfs: DataFrame) -> SecurityPriceList:
    """
    Creates a day's closing price SecurityPrice from a Pandas DataFrame
    """
    return create_stock_price(cls, symbol, "daily", dfs)


def add_to_iex_blacklist(cls, symbol: str) -> bool:
    """
    Add a symbol to the IEX blacklist, preventing MP from trying to request it from IEX
    """
    if on_iex_blacklist(cls, symbol):
        return None
    iex_bl = IexBlacklist()
    iex_bl.symbol = symbol
    iex_bl.timestamp = datetime.utcnow()

    def create(session):
        session.add(iex_bl)
        session.commit()

    cls.db.with_session(create)


def on_iex_blacklist(cls, symbol: str) -> bool:
    """
    Is this symbol on the IEX blacklist?
    """
    return cls.db.with_session(lambda session: session.query(IexBlacklist)
                               .filter(IexBlacklist.symbol == symbol).count() == 1
                               )
