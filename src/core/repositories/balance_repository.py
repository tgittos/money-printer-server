from typing import Optional

from core.apis.plaid.accounts import Accounts, AccountsConfig
from core.models.account_balance import AccountBalance
from core.models.account import Account
from core.models.plaid_item import PlaidItem
from core.repositories.scheduled_job_repository import ScheduledJobRepository, CreateInstantJobRequest
from core.repositories.plaid_repository import PlaidRepository
from core.stores.mysql import MySql
from core.lib.logger import get_logger
from core.lib.types import AccountBalanceList
from config import mysql_config, plaid_config, mailgun_config

from .facets.balance.crud import get_balances_by_account, get_latest_balance_by_account, create_account_balance
from .facets.balance.requests import CreateAccountBalanceRequest, GetAccountBalanceRequest


class BalanceRepository:

    logger = get_logger(__name__)

    def __init__(self):
        db = MySql(mysql_config)
        self.db = db.get_session()
        self.mysql_config = mysql_config
        self.plaid_config = plaid_config
        self.mailgun_config = mailgun_config

        self.scheduled_job_repo = get_scheduled_job_repository(mailgun_config=self.mailgun_config,
                                                               mysql_config=self.mysql_config)
        self.plaid_repo = PlaidRepository()

        self._init_facets()

    def _init_facets(self):
        self.get_balances_by_account = get_balances_by_account
        self.get_latest_balance_by_account = get_latest_balance_by_account
        self.create_account_balance = create_account_balance

    def schedule_update_all_balances(self, plaid_item: PlaidItem):
        """
        Schedules an instant job to update the balances of all accounts attached to a plaid Link item
        """
        if plaid_item is None:
            self.logger.warning("requested schedule update all balances without PlaidItem")
            return
        self.scheduled_job_repo.create_instant_job(CreateInstantJobRequest(
            job_name='sync_balances',
            args={
                'plaid_item_id': plaid_item.id
            }
        ))

    def schedule_update_balance(self, account: Account):
        """
        Schedules an instant job to update the balance of a given Account
        """
        if account is None:
            self.logger.warning("requested schedule update balance without Account")
            return
        plaid_item = self.plaid_repo.get_plaid_item_by_id(account.plaid_item_id)
        self.scheduled_job_repo.create_instant_job(CreateInstantJobRequest(
            job_name='sync_balances',
            args={
                'plaid_item_id': plaid_item.id
            }
        ))

    def sync_all_balances(self, plaid_item: PlaidItem) -> Optional[AccountBalanceList]:
        """
        Fetches the latest balances for all accounts attached to a given PlaidItem
        Returns None on any error
        """
        if plaid_item is None:
            self.logger.warning("requested all balance sync with no PlaidItem")
            return None
        self.logger.info("syncing account balance/s for plaid item: {0}".format(plaid_item.id))
        accounts = self.db.query(Account).where(Account.plaid_item_id == plaid_item.id).all()
        if accounts and len(accounts) > 0:
            self.logger.info("found {0} accounts to update".format(len(accounts)))
            for account in accounts:
                self.sync_account_balance(account.id)
            self.logger.info("done updating balances for plaid item")
        else:
            self.logger.warning("requested account sync of plaid item {0} but no accounts found".format(plaid_item.id))

    def sync_account_balance(self, account: Account) -> Optional[AccountBalance]:
        """
        Fetches the latest balance for the given account from Plaid
        Returns None on any error
        """
        if account is None:
            self.logger.warning("requested balance sync for account with no Account")
            return
        self.logger.info("syncing account balance for account id: {0}".format(account.id))
        plaid_item = self.db.query(PlaidItem).where(PlaidItem.id == account.plaid_item_id).first()
        if plaid_item is None:
            self.logger.warning("could not find PlaidItem attached to account {0}".format(account.id))
            return None

        api = Accounts(AccountsConfig(self.plaid_config))
        response_dict = api.get_account_balance(plaid_item.access_token, account.account_id)

        if response_dict is None or 'accounts' not in response_dict:
            self.logger.error("unusual response from upstream: {0}".format(response_dict))
            return None

        balances = []

        for account_dict in response_dict['accounts']:
            balance_dict = account_dict['balances']

            new_balance = self.create_account_balance(CreateAccountBalanceRequest(
                account=account,
                current=balance_dict['current'],
                available=balance_dict['available'],
                iso_currency_code=balance_dict['iso_currency_code']
            ))

            balances.append(new_balance)

        return balances[0]
