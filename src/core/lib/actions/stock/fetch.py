from datetime import datetime, timedelta, timezone
import traceback

from pandas import DataFrame
from iexfinance.stocks import get_historical_data, get_historical_intraday
from iexfinance.utils.exceptions import IEXQueryError

from core.lib.utilities import get_last_bus_day, is_bus_day

from .crud import add_to_iex_blacklist


def fetch_historical_daily(cls, symbol: str, start: datetime = None, end: datetime = None, close_only: bool = False)\
        -> DataFrame:
    """
    Gets the historical daily closing prices from IEX for the given time period for the given symbol
    """
    if start is None:
        start = get_last_bus_day(datetime.today() - timedelta(days=90))
    if end is None:
        end = get_last_bus_day(datetime.today())
    cls.logger.info("fetching historical daily prices for symbol {0}, {1} - {2} from upstream"
                     .format(symbol, start, end))
    try:
        df = get_historical_data(symbol,
                                 start=start,
                                 end=end,
                                 close_only=close_only)
        return df
    except IEXQueryError as ex:
        if ex.status == 404:
            cls.logger.warning("upstream provider couldn't resolve symbol {0}".format(symbol))
            add_to_iex_blacklist(cls, symbol)
        return None
    except Exception:
        cls.logger.exception("unexpected error from upstream provider fetching for symbol {0}: {1}"
                              .format(symbol, traceback.format_exc()))


def fetch_historical_intraday(cls, symbol: str, start: datetime = None) -> DataFrame:
    """
    Gets the per-minute historical intraday prices for the given day for the given symbol
    """
    if start is None:
        start = datetime.now(tz=timezone.utc) - timedelta(days=30)
    days = max((datetime.now(tz=timezone.utc) - start).days, 1)
    total_df = DataFrame()
    # walk the date range from the request (or default) start forward to now
    # requesting the daily intraday prices for that day
    # wrapped in a try/except to ensure we get as many data points as possible
    cls.logger.debug("starting historical intraday upstream walk, start: {0}, days: {1}"
                      .format(start, days))
    for i in range(days + 1):
        fetch_date = start + timedelta(days=i)
        # if this day is a non-business day, don't even try to fetch it, skip it
        if not is_bus_day(fetch_date.date()):
            cls.logger.debug("skipping historical intraday fetch for {0}, non business day".format(fetch_date))
            continue
        cls.logger.info("fetching historical intraday prices for symbol {0} on {1} from upstream"
                         .format(symbol, fetch_date))
        try:
            df = get_historical_intraday(symbol, date=fetch_date)
            total_df = total_df.append(df)
        except IEXQueryError as ex:
            if ex.status == 404:
                cls.logger.warning("upstream provider couldn't resolve symbol {0}".format(symbol))
                add_to_iex_blacklist(cls, symbol)
                return total_df
            else:
                cls.logger.warning("upstream provider returned an unknown error for symbol {0}: {1}"
                                    .format(symbol, traceback.format_exc()))
                continue
        except Exception:
            cls.logger.exception("unexpected error from upstream provider fetching for symbol {0}: {1}"
                                  .format(symbol, traceback.format_exc()))
            continue
    cls.logger.debug("returning {0} datapoints after upstream walk".format(len(total_df)))
    return total_df
