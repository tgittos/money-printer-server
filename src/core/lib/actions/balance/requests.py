from datetime import datetime

from core.models.account import Account


class GetAccountBalanceRequest:

    def __init__(self, account: Account, start: datetime = None, end: datetime = None):
        self.account = account
        self.start = start
        self.end = end
