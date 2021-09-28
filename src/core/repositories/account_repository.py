from core.models.account import Account
from core.models.profile import Profile
from core.models.plaid_item import PlaidItem
from core.presentation.account_presenters import AccountPresenter, AccountWithBalance, AccountWithBalanceList
from core.stores.mysql import MySql
from core.repositories.scheduled_job_repository import ScheduledJobRepository, CreateInstantJobRequest
from core.lib.logger import get_logger
from config import mysql_config, plaid_config, mailgun_config, iex_config

from .facets.account.crud import create_account, update_account, get_account_by_account_id, get_account_by_id,\
    get_accounts_by_profile


class AccountRepository:

    logger = get_logger(__name__)

    def __init__(self):
        db = MySql(mysql_config)
        self.db = db.get_session()

        self.mysql_config = mysql_config
        self.plaid_config = plaid_config
        self.mailgun_config = mailgun_config
        self.iex_config = iex_config

        self.presenter = AccountPresenter(self.db)

        self._init_facets()

    def _init_facets(self):
        self.create_account = create_account
        self.update_account = update_account
        self.get_account_by_id = get_account_by_id
        self.get_account_by_account_id = get_account_by_account_id
        self.get_accounts_by_profile = get_accounts_by_profile

    def get_accounts_by_profile_with_balances(self, profile: Profile) -> AccountWithBalanceList:
        """
        Returns a list of accounts augmented with their latest synced balances for a given profile
        """
        account_records = self.get_accounts_by_profile(profile)
        return self.presenter.with_balances(account_records)

    def get_account_by_profile_with_balance(self, profile: Profile, account_id: int) -> AccountWithBalanceList:
        """
        Returns the requested Account with it's latest synced balance for a given profile
        """
        account = self.get_account_by_account_id(profile, account_id)
        return self.presenter.with_balances([account])

    def schedule_account_sync(self, account: Account):
        """
        Schedules an InstantJob to perform a full sync for a given account
        """
        if account is None:
            self.logger.error("cannot schedule account sync without account")
            return
        plaid_item = self.db.query(PlaidItem).where(PlaidItem.id == account.plaid_item_id).first()
        if plaid_item is None:
            self.logger.error("scheduled account sync for plaid item, but no PlaidItem found")
            return

        scheduled_job_repo = ScheduledJobRepository()

        scheduled_job_repo.create_instant_job(CreateInstantJobRequest(
            job_name='sync_accounts',
            args={
                'plaid_item_id': plaid_item.id
            }
        ))
