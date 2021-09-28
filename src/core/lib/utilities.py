from typing import Optional
from datetime import date, datetime, timezone

import numpy as np


def sanitize_float(val) -> float:
    """
    Ensure that the given value is really a float
    Returns None if None given, 0 if NaN, float otherwise
    """
    if val is None:
        return 0
    if np.isnan(val):
        return 0
    return float(val)


def add_tz(val: date) -> datetime:
    """
    Converts a time to a UTC datetime
    """
    if val is None:
        return val
    local_tz = datetime.now(tz=timezone.utc).astimezone().tzinfo
    return datetime(date).replace(tzinfo=local_tz)


def local_to_utc(val: date) -> Optional[datetime]:
    """
    Converts a datetime in the local timezone to a UTC datetime
    """
    if val is None:
        return val
    tz_val = add_tz(val)
    utc_val = tz_val.astimezone(tz=timezone.utc)
    return utc_val


def get_last_bus_day(d: datetime) -> datetime:
    """
    Given a datetime, return a datetime representing the last business day
    Excludes weekends, doesn't exclude bank holidays
    """
    return np.busday_offset(d.date(), 0, roll='backward').astype(datetime)


def is_bus_day(d: date) -> bool:
    """
    Is this date a business day?
    """
    return np.is_busday(d)
