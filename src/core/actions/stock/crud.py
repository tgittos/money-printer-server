from datetime import datetime

from pandas import DataFrame
from sqlalchemy import and_

from core.models.security_price import SecurityPrice
from core.models.iex_blacklist import IexBlacklist
from core.lib.utilities import sanitize_float, local_to_utc
from core.actions.action_response import ActionResponse


def create_stock_price(db, symbol: str, resolution: str, dfs: DataFrame) -> ActionResponse:
    """
    Stores a SecurityPrice record in the database from a Pandas DataFrame
    """
    records = []
    indices = dfs.to_dict(orient='index')
    for date_index in indices:
        df = indices[date_index]

        # we're tracking this time period already, ignore it
        if not has_data_point(symbol, resolution, date_index):
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
            if 'uHigh' in df:
                price.u_high = sanitize_float(df['uHigh'])
            if 'uLow' in df:
                price.u_low = sanitize_float(df['uLow'])
            if 'uOpen' in df:
                price.u_open = sanitize_float(df['uOpen'])
            if 'uClose' in df:
                price.u_close = sanitize_float(df['uClose'])
            if 'uVolume' in df:
                price.u_volume = sanitize_float(df['uVolume'])
            if 'change' in df:
                price.change = sanitize_float(df['change'])
            if 'changePercent' in df:
                price.change_percent = sanitize_float(df['changePercent'])
            if 'changeOverTime' in df:
                price.change_over_time = sanitize_float(df['changeOverTime'])
            if 'marketChangeOverTime' in df:
                price.market_change_over_time = sanitize_float(
                    df['marketChangeOverTime'])

            with db.get_session() as session:
                session.add(price)
                session.commit()

            records.append(price)

    return ActionResponse(
        success=True,
        data=records,
    )


def get_historical_intraday_security_prices(db, symbol: str, start: datetime = None) -> ActionResponse:
    """
    Searches the database for all per-minute intraday SecurityPrices for a given symbol on a given day
    """
    with db.get_session() as session:
        records = session.query(SecurityPrice).filter(and_(
            SecurityPrice.symbol == symbol,
            SecurityPrice.resolution == "intraday",
            start is None or SecurityPrice.date >= start
        )).all()

    return ActionResponse(
        success=records is not None,
        data=records
    )


def get_historical_daily_security_prices(db, symbol: str, start: datetime = None, end: datetime = None) -> ActionResponse:
    """
    Searches the database for the daily close SecurityPrices for a given symbol in a given date range
    """
    with db.get_session() as session:
        records = session.query(SecurityPrice).filter(and_(
            SecurityPrice.symbol == symbol,
            SecurityPrice.resolution == "daily",
            start is None or SecurityPrice.date >= start,
            end is None or SecurityPrice.date <= end,
        )).all()

    return ActionResponse(
        success=records is not None,
        data=records
    )


def create_historical_intraday_security_price(db, symbol: str, dfs: DataFrame) -> ActionResponse:
    """
    Creates a day's worth of historical per-minute intraday SecurityPrice from a Pandas DataFrame
    """
    return create_stock_price(db, symbol, "intraday", dfs)


def create_historical_daily_security_price(db, symbol: str, dfs: DataFrame) -> ActionResponse:
    """
    Creates a day's closing price SecurityPrice from a Pandas DataFrame
    """
    return create_stock_price(db, symbol, "daily", dfs)


def add_to_iex_blacklist(db, symbol: str) -> bool:
    """
    Add a symbol to the IEX blacklist, preventing MP from trying to request it from IEX
    """
    if on_iex_blacklist(db, symbol):
        return None

    iex_bl = IexBlacklist()

    iex_bl.symbol = symbol
    iex_bl.timestamp = datetime.utcnow()

    with db.get_session() as session:
        session.add(iex_bl)
        session.commit()


def on_iex_blacklist(db, symbol: str) -> bool:
    """
    Is this symbol on the IEX blacklist?
    """
    with db.get_session() as session:
        return session.query(IexBlacklist).filter(IexBlacklist.symbol == symbol).count() == 1


def has_data_point(db, symbol: str, resolution: str, timestamp: datetime) -> bool:
    """
    Does this symbol have this resolution datapoint for this timestamp?
    """
    with db.get_session() as session:
        if resolution == 'intraday':
            return session.query(SecurityPrice).filter(and_(
                SecurityPrice.symbol == symbol,
                SecurityPrice.date == timestamp
            )).count() > 0
        if resolution == 'daily':
            return session.query(SecurityPrice).filter(and_(
                SecurityPrice.symbol == symbol,
                SecurityPrice.date == timestamp.date()
            )).count() > 0