from typing import Optional

from core.models.account import AccountSchema
from core.stores.mysql import MySql
from core.repositories.scheduled_job_repository import ScheduledJobRepository, CreateInstantJobRequest
from core.lib.logger import get_logger
from config import mysql_config

# import all the actions so that consumers of the repo can access everything
from core.lib.utilities import wrap
from core.lib.actions.account.crud import *


class AccountRepository:

    logger = get_logger(__name__)
    db = MySql(mysql_config)

    def __init__(self):
        self._init_facets()

    def _init_facets(self):
        self.create_account = wrap(create_account, self.db)
        self.update_account = wrap(update_account, self.db)
        self.get_account_by_id = wrap(get_account_by_id, self.db)
        self.get_account_by_account_id = wrap(
            get_account_by_account_id, self.db)
        self.get_accounts_by_profile = wrap(get_accounts_by_profile, self.db)

    def get_accounts_by_profile_with_balances(self, profile: Profile):
        """
        Returns a list of accounts augmented with their latest synced balances for a given profile
        """
        if profile is None:
            self.logger.error(
                "requested accounts by profile without a valid Profile")
            return None
        account_records = self.get_accounts_by_profile(profile)
        return AccountSchema(many=True).dumps(account_records)

    def get_account_by_profile_with_balance(self, profile: Profile, account_id: int):
        """
        Returns the requested Account with it's latest synced balance for a given profile
        """
        if profile is None:
            self.logger.error(
                "requested account by profile without a valid Profile")
            return None
        if account_id is None:
            self.logger.error(
                "requested account by profile without a valid account_id")
            return None
        account = self.get_account_by_account_id(profile, account_id)
        return AccountSchema().dumps(account)

    def schedule_account_sync(self, account: Account):
        """
        Schedules an InstantJob to perform a full sync for a given account
        """
        if account is None:
            self.logger.error("cannot schedule account sync without account")
            return

        with self.db.get_session() as session:
            plaid_item = session.query(PlaidItem).where(
                PlaidItem.id == account.plaid_item_id).first()

        if plaid_item is None:
            self.logger.error(
                "scheduled account sync for plaid item, but no PlaidItem found")
            return

        scheduled_job_repo = ScheduledJobRepository()

        scheduled_job_repo.create_instant_job(CreateInstantJobRequest(
            job_name='sync_accounts',
            args={
                'plaid_item_id': plaid_item.id
            }
        ))
