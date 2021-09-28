from datetime import datetime

from core.models.account import Account


class GetAccountBalanceRequest:

    def __init__(self, account: Account, start: datetime = None, end: datetime = None):
        self.account = account
        self.start = start
        self.end = end


class CreateAccountBalanceRequest:

    def __init__(self, account: Account, available: float, current: float, iso_currency_code: str):
        self.account = account
        self.available = available
        self.current = current
        self.iso_currency_code = iso_currency_code
