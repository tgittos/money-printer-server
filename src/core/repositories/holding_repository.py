from typing import Optional

from core.models.account import Account
from core.models.plaid_item import PlaidItem
from core.models.holding import Holding
from core.stores.mysql import MySql
from core.repositories.scheduled_job_repository import ScheduledJobRepository, CreateInstantJobRequest
from core.repositories.security_repository import SecurityRepository
from core.lib.logger import get_logger
from config import mysql_config

from core.lib.actions.account.crud import get_accounts_by_plaid_item
from core.lib.actions.profile.crud import get_profile_by_id

# import all the actions so that consumers of the repo can access everything
# no actions right now!


class HoldingRepository:

    logger = get_logger(__name__)
    db = MySql(mysql_config)

    def __init__(self):
        self.scheduled_job_repo = ScheduledJobRepository()
        self.security_repo = SecurityRepository()

    def schedule_update_holdings(self, plaid_item: PlaidItem):
        """
        Creates an InstantJob to perform a sync_holdings job for all investment accounts attached to a PlaidItem
        """
        if plaid_item is None:
            self.logger.error("cannot schedule account holding sync without plaid item")
            return
        self.scheduled_job_repo.create_instant_job(CreateInstantJobRequest(
            job_name='sync_holdings',
            args={
                'plaid_item_id': plaid_item.id
            }
        ))

    def schedule_update_transactions(self, plaid_item: PlaidItem):
        """
        Creates an InstantJob to perform a sync_transactions job for all investment accounts attached to a PlaidItem
        """
        if plaid_item is None:
            self.logger.error("cannot schedule investment transaction sync without plaid item")
            return
        self.scheduled_job_repo.create_instant_job(CreateInstantJobRequest(
            job_name='sync_transactions',
            args={
                'plaid_item_id': plaid_item.id
            }
        ))

    def update_holdings(self, plaid_item: PlaidItem):
        """
        Performs a sync of all security holdings for accounts associated with a PlaidItem
        """
        if plaid_item is None:
            self.logger.warning("requested update holding but no PlaidItem given")
            return None
        accounts = self.db.with_session(
            lambda session: session.query(Account).filter(Account.plaid_item_id == plaid_item.id).all()
        )
        profile = None
        if accounts is None or len(accounts) == 0:
            self.logger.error("received request to update holdings with no corresponding accounts: {0}"
                              .format(plaid_item.id))
            return
        accounts_updated = 0
        for account in accounts:
            if profile is None:
                profile = get_profile_by_id(self, plaid_item.profile_id)
            self.logger.info("updating holdings for account: {0}".format(account.id))
            self.security_repo.sync_holdings(profile=profile, account=account)
            accounts_updated += 1
        self.logger.info("updated holdings for {0} accounts".format(accounts_updated))

    def update_transactions(self, plaid_item: PlaidItem):
        """
        Performs a sync of all security transactions for accounts associated with a PlaidItem
        """
        if plaid_item is None:
            self.logger.error("cannot update investment transactions without a valid plaid_item_id")
            return
        profile = get_profile_by_id(self, plaid_item.profile_id)
        accounts = get_accounts_by_plaid_item(self, plaid_item)
        if accounts is None or len(accounts) == 0:
            self.logger.error("received request to update investment transactions with no corresponding accounts: {0}"
                              .format(plaid_item.id))
            return
        accounts_updated = 0
        for account in accounts:
            self.logger.info("updating investment transactions for account: {0}".format(account.id))
            self.security_repo.sync_transactions(profile=profile, account=account)
            accounts_updated += 1
        self.logger.info("updated investment transactions for {0} accounts".format(accounts_updated))

    def calculate_performance(self, holding: Holding):
        # pull the holding
        # pull security_prices for holding
        # using cost basis of holding, at each security_price data point, calculate a rate of return
        raise Exception("Not implemented")

    def calculate_forecast(self, holding_id):
        raise Exception("Not implemented")

