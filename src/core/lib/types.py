from typing import List

from core.models.account import Account
from core.models.account_balance import AccountBalance
from core.models.holding import Holding
from core.models.holding_balance import HoldingBalance
from core.models.iex_blacklist import IexBlacklist
from core.models.investment_transaction import InvestmentTransaction
from core.models.plaid_item import PlaidItem
from core.models.profile import Profile
from core.models.reset_token import ResetToken
from core.models.scheduler.scheduled_job import ScheduledJob
from core.models.security import Security
from core.models.security_price import SecurityPrice

StringList = List[str]

AccountList = List[Account]
AccountBalanceList = List[AccountBalance]
HoldingList = List[Holding]
HoldingBalanceList = List[HoldingBalance]
IexBlacklistList = List[IexBlacklist]
InvestmentTransactionList = List[InvestmentTransaction]
PlaidItemList = List[PlaidItem]
ProfileList = List[Profile]
ResetTokenList = List[ResetToken]
ScheduledJobList = List[ScheduledJob]
SecurityList = List[Security]
SecurityPriceList = List[SecurityPrice]


class RepositoryResponse:
    def __init__(self, success: bool = True, message: str = None, data: dict = None):
        self.success = success
        self.message = message
        self.data = data
