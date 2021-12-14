from core.models.plaid_item import PlaidItem
from core.repositories.balance_repository import BalanceRepository
from core.repositories.holding_repository import HoldingRepository
from core.repositories.scheduled_job_repository import ScheduledJobRepository, CreateInstantJobRequest
from core.stores.mysql import MySql
from core.apis.plaid.accounts import Accounts, AccountsConfig
from core.lib.utilities import wrap
from core.lib.logger import get_logger
from config import mysql_config, plaid_config

from core.lib.actions.account.crud import create_or_update_account
from core.lib.actions.plaid.crud import get_plaid_items_by_profile

# import all the actions so that consumers of the repo can access everything
from core.lib.actions.profile.crud import *
from core.lib.actions.profile.auth import *
from core.lib.actions.profile.requests import *
from core.lib.actions.profile.responses import *


class ProfileRepository:

    logger = get_logger(__name__)

    def __init__(self, store):
        self.db = store
        self._init_facets()

    def _init_facets(self):
        self.get_profile_by_id = wrap(get_profile_by_id, self.db)
        self.get_profile_by_email = wrap(get_profile_by_email, self.db)
        self.get_all_profiles = wrap(get_all_profiles, self.db)
        self.get_unauthenticated_user = wrap(get_unauthenticated_user, self.db)
        self.create_profile = wrap(create_profile, self.db)
        self.register = wrap(register, self.db)
        self.login = wrap(login, self.db)
        self.reset_password = wrap(reset_password, self.db)
        self.continue_reset_password = wrap(continue_reset_password, self.db)
        self.logout = wrap(logout, self.db)

    def schedule_profile_sync(self, profile: Profile):
        """
        Schedules an InstantJob to perform a full sync for a given account
        """
        if profile is None:
            self.logger.error("cannot schedule profile sync without Profile")
            return
        plaid_items = get_plaid_items_by_profile(self.db, profile)
        if plaid_items is None:
            self.logger.error("scheduled account sync for Profile, but no PlaidItems found")
            return

        for plaid_item in plaid_items:
            scheduled_job_repo = ScheduledJobRepository()
            scheduled_job_repo.create_instant_job(CreateInstantJobRequest(
                job_name='sync_accounts',
                args={
                    'plaid_item_id': plaid_item.id
                }
            ))

    def sync_all_accounts(self, plaid_item: PlaidItem):
        """
        Syncs the account state from Plaid for all accounts attached to the given Plaid Item
        This will pull:
          - account details
          - account balances
          - investment holdings
        """
        if plaid_item is None:
            self.logger.warning("Sync all accounts requested without PlaidItem")
            return

        self.logger.info("updating account state for PlaidItem {0}".format(plaid_item.id))

        balance_repo = BalanceRepository()
        holdings_repo = HoldingRepository()

        plaid_accounts_api = Accounts(AccountsConfig(
            plaid_config=plaid_config
        ))

        profile = self.get_profile_by_id(plaid_item.profile_id)

        if profile is None:
            self.logger.warning("couldn't find Profile attached to fetched PlaidItem: {0}".format(plaid_item.id))
            return

        plaid_accounts_dict = plaid_accounts_api.get_accounts(plaid_item.access_token)

        self.logger.info("updating {0} accounts".format(len(plaid_accounts_dict['accounts'])))

        accounts = []
        for account_dict in plaid_accounts_dict['accounts']:
            if 'account_id' in account_dict:
                self.logger.info("updating account details for profile {0}, account {1}"
                                 .format(profile.id, account_dict['account_id']))
                account = create_or_update_account(self.db,
                                                   profile=profile,
                                                   plaid_link=plaid_item,
                                                   account_dict=account_dict)
                accounts.append(account)
                self.logger.info("updating account balance for account {0}".format(account.id))
                balance_repo.sync_account_balance(account)
            else:
                self.logger.warning("upstream returned account response missing an id: {0}".format(account_dict))

        self.logger.info("fetching investment holdings for PlaidItem {0}".format(plaid_item.id))
        holdings_repo.update_holdings(plaid_item)

        self.logger.info("done updating accounts for profile {0}".format(profile.id))
