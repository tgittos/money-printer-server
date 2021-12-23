from core.models.plaid_item import PlaidItem
from core.repositories.balance_repository import BalanceRepository
from core.repositories.holding_repository import HoldingRepository
from core.repositories.scheduled_job_repository import ScheduledJobRepository
from core.apis.plaid.accounts import Accounts, AccountsConfig
from core.lib.utilities import wrap
from core.lib.logger import get_logger
from core.stores.mysql import MySql
from core.repositories.repository_response import RepositoryResponse
from config import mysql_config, plaid_config
from core.schemas.create_schemas import CreateInstantJobSchema

from core.lib.actions.account.crud import create_or_update_account
from core.lib.actions.plaid.crud import get_plaid_items_by_profile, get_plaid_item_by_id

# import all the actions so that consumers of the repo can access everything
from core.lib.actions.profile.crud import *
from core.lib.actions.profile.auth import *


class ProfileRepository:

    db = MySql(mysql_config)
    logger = get_logger(__name__)
    balance_repo = BalanceRepository()
    holdings_repo = HoldingRepository()
    scheduled_job_repo = ScheduledJobRepository()
    plaid_accounts_api = Accounts(AccountsConfig(
        plaid_config=plaid_config
    ))

    def __init__(self):
        self._init_facets()

    def _init_facets(self):
        self.get_profile_by_id = wrap(get_profile_by_id, self.db)
        self.get_all_profiles = wrap(get_all_profiles, self.db)
        self.get_unauthenticated_user = wrap(get_unauthenticated_user, self.db)
        self.create_profile = wrap(create_profile, self.db)
        self.register = wrap(register, self.db)
        self.login = wrap(login, self.db)
        self.reset_password = wrap(reset_password, self.db)
        self.continue_reset_password = wrap(continue_reset_password, self.db)
        self.logout = wrap(logout, self.db)

    def schedule_profile_sync(self, profile_id: int) -> RepositoryResponse:
        """
        Schedules an InstantJob to perform a full sync for a given account
        """
        profile_result = get_profile_by_id(self.db, profile_id)
        if not profile_result.success:
            self.logger.error("cannot schedule profile sync without Profile")
            return RepositoryResponse(
                success=False,
                message=profile_result.message
            )

        plaid_result = get_plaid_items_by_profile(self.db, profile_result.data)
        if not plaid_result.success or len(plaid_result.data) == 0:
            self.logger.error(
                "scheduled account sync for Profile, but no PlaidItems found")
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        for plaid_item in plaid_result.data:
            self.scheduled_job_repo.create_instant_job(CreateInstantJobSchema().load({
                'job_name': 'sync_accounts',
                'json_args': {
                    'plaid_item_id': plaid_item.id
                }
            }))

        return RepositoryResponse(success=True)

    def sync_all_accounts(self, plaid_item_id: int) -> RepositoryResponse:
        """
        Syncs the account state from Plaid for all accounts attached to the given Plaid Item
        This will pull:
          - account details
          - account balances
          - investment holdings
        """
        plaid_result = get_plaid_item_by_id(self.db, plaid_item_id)
        if not plaid_result.success:
            self.logger.warning(
                "Sync all accounts requested without PlaidItem")
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        self.logger.info(
            "updating account state for PlaidItem {0}".format(plaid_item_id))

        profile_result = get_profile_by_id(
            self.db, plaid_result.data.profile_id)

        if not profile_result.success or profile_result.data is None:
            self.logger.warning(
                "couldn't find Profile attached to fetched PlaidItem: {0}".format(plaid_item_id))
            return RepositoryResponse(
                success=False,
                message=profile_result.message
            )

        plaid_accounts_dict = self.plaid_accounts_api.get_accounts(
            plaid_result.data.access_token)

        self.logger.info("updating {0} accounts".format(
            len(plaid_accounts_dict['accounts'])))

        accounts = []
        for account_dict in plaid_accounts_dict['accounts']:
            if 'account_id' in account_dict:
                self.logger.info("updating account details for profile {0}, account {1}"
                                 .format(profile_result.data.id, account_dict['account_id']))
                account_result = create_or_update_account(self.db,
                                                          profile=profile_result.data,
                                                          plaid_link=plaid_result.data,
                                                          account_dict=account_dict)
                accounts.append(account_result.data)
                self.logger.info("updating account balance for account {0}".format(
                    account_result.data.id))
                self.balance_repo.sync_account_balance(account_result.data)
            else:
                self.logger.warning(
                    "upstream returned account response missing an id: {0}".format(account_dict))

        self.logger.info(
            "fetching investment holdings for PlaidItem {0}".format(plaid_result.data.id))
        self.holdings_repo.update_holdings(plaid_result.data.id)

        self.logger.info("done updating accounts for profile {0}".format(
            profile_result.data.id))

        return RepositoryResponse(
            success=True
        )
