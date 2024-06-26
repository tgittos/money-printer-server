import random
import string
from datetime import date, datetime, timezone
from typing import Optional
import numpy as np
import re

email_validation_re = re.compile(
    r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

# https://www.python-course.eu/currying_in_python.php


def curry(func):
    # to keep the name of the curried function:
    curry.__curried_func_name__ = func.__name__
    f_args, f_kwargs = [], {}

    def f(*args, **kwargs):
        nonlocal f_args, f_kwargs
        if args or kwargs:
            f_args += args
            f_kwargs.update(kwargs)
            return f
        else:
            result = func(*f_args, *f_kwargs)
            f_args, f_kwargs = [], {}
            return result

    return f


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


def add_tz(val: datetime) -> datetime:
    """
    Converts a time to a UTC datetime
    """
    if val is None:
        return val
    local_tz = datetime.now(tz=timezone.utc).astimezone().tzinfo
    return val.replace(tzinfo=local_tz)


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


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/
def is_valid_email(email):
    return re.fullmatch(email_validation_re, email)


# https://stackoverflow.com/questions/1305532/convert-nested-python-dict-to-object
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def to_dict(self):
        return self.__dict__
