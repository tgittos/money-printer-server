from core.models.plaid_item import PlaidItem
from core.repositories import AccountRepository, HoldingRepository
from core.repositories.scheduled_job_repository import ScheduledJobRepository
from core.apis.plaid.accounts import PlaidAccounts, PlaidAccountsConfig
from core.lib.logger import get_logger
from core.stores.mysql import MySql
from core.repositories.repository_response import RepositoryResponse
from config import mysql_config, plaid_config
from core.schemas.scheduler_schemas import CreateInstantJobSchema
from core.schemas.profile_schemas import *
from core.schemas.auth_schemas import *

from core.actions.account.crud import create_or_update_account
from core.actions.plaid.crud import get_plaid_items_by_profile_id, get_plaid_item_by_id
import core.actions.profile.crud as crud
import core.actions.profile.auth as auth


class ProfileRepository:

    db = MySql(mysql_config)
    logger = get_logger(__name__)
    account_repo = AccountRepository()
    holdings_repo = HoldingRepository()
    scheduled_job_repo = ScheduledJobRepository()
    plaid_accounts_api = PlaidAccounts(PlaidAccountsConfig(
        plaid_config=plaid_config
    ))

    def get_profile_by_id(self, profile_id: int) -> RepositoryResponse:
        """
        Retrieves a profile by it's primary key ID
        """
        return crud.get_profile_by_id(self.db, profile_id)

    def create_profile(self, request: CreateProfileSchema) -> RepositoryResponse:
        """
        Creates a new profile with the requested details
        """
        return crud.create_profile(self.db, request)

    def update_profile(self, request: UpdateProfileSchema) -> RepositoryResponse:
        """
        Updates a profile's details for the requested profile
        """
        return crud.update_profile(self.db, request)

    def register(self, request: RegisterProfileSchema) -> RepositoryResponse:
        """
        Register a new profile - functionally similar to `create_profile`
        """
        return crud.register(self.db, request)

    def login(self, request: LoginSchema) -> RepositoryResponse:
        """
        Authenticate profile credentials
        """
        return auth.login(self.db, request)

    def reset_password(self, email: str) -> RepositoryResponse:
        """
        Start the reset password process for the given profile
        """
        return auth.reset_password(self.db, email)

    def continue_reset_password(self, request: ResetPasswordSchema) -> RepositoryResponse:
        """
        Finalize the password reset with the secret token and the profile's new password
        """
        return auth.continue_reset_password(self.db, request)

    def schedule_profile_sync(self, profile_id: int) -> RepositoryResponse:
        """
        Schedules an InstantJob to perform a full sync for a given account
        """
        profile_result = crud.get_profile_by_id(self.db, profile_id)
        if not profile_result.success:
            self.logger.error("cannot schedule profile sync without Profile")
            return RepositoryResponse(
                success=False,
                message=profile_result.message
            )

        plaid_result = get_plaid_items_by_profile_id(self.db, profile_result.data.id)
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

    def sync_all_accounts(self, profile_id: int, plaid_item_id: int) -> RepositoryResponse:
        """
        Syncs the account state from Plaid for all accounts attached to the given Plaid Item
        This will pull:
          - account details
          - account balances
          - investment holdings
        """
        plaid_result = get_plaid_item_by_id(self.db, profile_id, plaid_item_id)
        if not plaid_result.success:
            self.logger.warning(
                "Sync all accounts requested without PlaidItem")
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        self.logger.info(
            "updating account state for PlaidItem {0}".format(plaid_item_id))

        profile_result = crud.get_profile_by_id(self.db, plaid_result.data.profile_id)

        if not profile_result.success or profile_result.data is None:
            self.logger.warning(
                "couldn't find Profile attached to fetched PlaidItem: {0}".format(plaid_item_id))
            return RepositoryResponse(
                success=False,
                message=profile_result.message
            )

        plaid_accounts_dict = self.plaid_accounts_api.get_accounts(plaid_result.data.access_token)

        self.logger.info("updating {0} accounts".format(
            len(plaid_accounts_dict['accounts'])))

        accounts = []
        for account_dict in plaid_accounts_dict['accounts']:
            if 'account_id' in account_dict:
                self.logger.info("updating account details for profile {0}, account {1}"
                                 .format(profile_result.data.id, account_dict['account_id']))
                account_result = create_or_update_account(self.db,
                                                          profile_id=profile_result.data.id,
                                                          plaid_link_id=plaid_result.data.id,
                                                          account_dict=account_dict)
                accounts.append(account_result.data)
                self.logger.info("updating account balance for account {0}".format(
                    account_result.data.id))
                self.account_repo.sync_account_balance(profile_id, account_result.data.id)
            else:
                self.logger.warning(
                    "upstream returned account response missing an id: {0}".format(account_dict))

        self.logger.info(
            "fetching investment holdings for PlaidItem {0}".format(plaid_result.data.id))
        self.holdings_repo.update_holdings(profile_id, plaid_result.data.id)

        self.logger.info("done updating accounts for profile {0}".format(
            profile_result.data.id))

        return RepositoryResponse(
            success=True
        )
