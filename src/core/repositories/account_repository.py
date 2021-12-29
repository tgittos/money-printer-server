from marshmallow import Schema, fields, EXCLUDE

from core.repositories.scheduled_job_repository import ScheduledJobRepository
from core.repositories.plaid_repository import PlaidRepository
from core.repositories.repository_response import RepositoryResponse
from core.schemas import CreateInstantJobSchema, CreateAccountBalanceSchema
from core.apis.plaid.accounts import PlaidAccounts, PlaidAccountsConfig
from core.stores.mysql import MySql
from core.lib.logger import get_logger
from config import mysql_config, plaid_config

# import all the actions so that consumers of the repo can access everything
import core.actions.account.crud as account_crud
import core.actions.balance.crud as balance_crud
from core.actions.profile.crud import get_profile_by_id
from core.actions.plaid.crud import get_plaid_item_by_id


class AccountRepository:

    logger = get_logger(__name__)
    db = MySql(mysql_config)
    plaid_repo = PlaidRepository()
    scheduled_job_repo = ScheduledJobRepository()
    plaid_accounts_api = PlaidAccounts(PlaidAccountsConfig(
        plaid_config=plaid_config
    ))

    def get_accounts_by_profile_id(self, profile_id: int) -> RepositoryResponse:
        """
        Returns a list of accounts for a given profile ID
        """
        profile_result = get_profile_by_id(self.db, profile_id)
        return profile_result

    def get_accounts_by_profile_with_balances(self, profile_id: int) -> RepositoryResponse:
        """
        Returns a list of accounts augmented with their latest synced balances for a given profile
        """
        profile_result = get_profile_by_id(self.db, profile_id)
        if not profile_result.success:
            return profile_result
        action_result = self.get_accounts_by_profile(profile_result.data)
        return RepositoryResponse(success=action_result.success, data=action_result.data, message=action_result.message)

    def get_account_by_profile_with_balance(self, profile_id: int, account_id: int) -> RepositoryResponse:
        """
        Returns the requested Account with it's latest synced balance for a given profile
        """
        profile_result = get_profile_by_id(self.db, profile_id)
        if not profile_result.success:
            return profile_result
        action_result = self.get_account_by_account_id(
            profile_result.data, account_id)
        return RepositoryResponse(success=action_result.success, data=action_result.data, message=action_result.message)

    def schedule_account_sync(self, account_id: int) -> RepositoryResponse:
        """
        Schedules an InstantJob to perform a full sync for a given account
        """
        account_result = self.get_account_by_id(account_id)

        if not account_result.success:
            self.logger.error("cannot schedule account sync without account")
            return RepositoryResponse(
                success=False,
                message=account_result.message
            )

        plaid_item_result = get_plaid_item_by_id(
            account_result.data.plaid_item_id)

        if not plaid_item_result.success or plaid_item_result.data is None:
            self.logger.error(
                "scheduled account sync for plaid item, but no PlaidItem found")
            return plaid_item_result

        plaid_item = plaid_item_result.data

        return self.scheduled_job_repo.create_instant_job(CreateInstantJobSchema(
            job_name='sync_accounts',
            args={
                'plaid_item_id': plaid_item.id
            }
        ))

    def schedule_update_all_balances(self, plaid_item_id: int) -> RepositoryResponse:
        """
        Schedules an instant job to update the balances of all accounts attached to a plaid Link item
        """
        plaid_result = get_plaid_item_by_id(self.db, plaid_item_id)
        if not plaid_result.success:
            self.logger.warning(
                "requested schedule update all balances without PlaidItem")
            return plaid_result

        return self.scheduled_job_repo.create_instant_job(CreateInstantJobSchema(
            job_name='sync_balances',
            args={
                'plaid_item_id': plaid_result.data.id
            }
        ))

    def schedule_update_balance(self, account_id: int) -> RepositoryResponse:
        """
        Schedules an instant job to update the balance of a given Account
        """
        account_result = account_crud.get_account_by_id(self.db, account_id)
        if not account_result.success:
            self.logger.warning(
                "requested schedule update balance without Account")
            return account_result

        plaid_result = self.plaid_repo.get_plaid_item_by_id(
            account_result.data.plaid_item_id)
        if not plaid_result.success:
            return plaid_result

        return self.scheduled_job_repo.create_instant_job(CreateInstantJobSchema(
            job_name='sync_balances',
            args={
                'plaid_item_id': plaid_result.data.id
            }
        ))

    def sync_all_balances(self, plaid_item_id: int) -> RepositoryResponse:
        """
        Fetches the latest balances for all accounts attached to a given PlaidItem
        Returns None on any error
        """
        plaid_result = get_plaid_item_by_id(self.db, plaid_item_id)
        if not plaid_result.success:
            self.logger.warning("requested all balance sync with no PlaidItem")
            return plaid_result

        self.logger.info(
            "syncing account balance/s for plaid item: {0}".format(plaid_result.data.id))

        accounts_result = account_crud.get_accounts_by_plaid_item_id(
            plaid_result.data.id)
        if accounts_result.success and len(accounts_result.data) > 0:
            accounts = accounts_result.data
            self.logger.info(
                "found {0} accounts to update".format(len(accounts)))
            for account in accounts:
                self.sync_account_balance(account.id)
            self.logger.info("done updating balances for plaid item")
        else:
            self.logger.warning(
                "requested account sync of plaid item {0} but no accounts found".format(plaid_result.data.id))
            return RepositoryResponse(
                success=False,
                message=f"Could not found accounts belonging to Plaid Item ID {plaid_item_id}"
            )

        return RepositoryResponse(
            success=True
        )

    def sync_account_balance(self, account_id: int) -> RepositoryResponse:
        """
        Fetches the latest balance for the given account from Plaid
        Returns None on any error
        """
        account_result = account_crud.get_account_by_id(self.db, account_id)
        if not account_result.success:
            self.logger.warning(
                "requested balance sync for account with no Account")
            return account_result

        self.logger.info("syncing account balance for account id: {0}".format(
            account_result.data.id))

        plaid_item_result = get_plaid_item_by_id(
            self.db, account_result.data.plaid_item_id)

        if not plaid_item_result.success or plaid_item_result.data is None:
            self.logger.warning("could not find PlaidItem attached to account {0}".format(
                account_result.data.id))
            return plaid_item_result

        plaid_item = plaid_item_result.data
        # make Plaid API request
        response_dict = self.plaid_accounts_api.get_account_balance(
            plaid_item.access_token, account_result.data.account_id)

        if response_dict is None or 'accounts' not in response_dict:
            self.logger.error(
                "unusual response from upstream: {0}".format(response_dict))
            return RepositoryResponse(
                success=False,
                message=f"Could not find 'accounts' key on response from upstream"
            )

        balances = []

        for account_dict in response_dict['accounts']:
            balance_dict = account_dict['balances']

            schema = CreateAccountBalanceSchema(unknown=EXCLUDE).load({
                **{'account': account_result.data},
                **balance_dict
            })
            balance_result = balance_crud.create_account_balance(
                self.db, schema)

            if balance_result.success:
                balances.append(balance_result.data)
            else:
                self.logger.warning(
                    f"account_balance creation failed with message {balance_result.message}")

        return RepositoryResponse(
            success=balances[0] is not None,
            data=balances[0],
            message="Unknown error fetching balances" if balances[0] is None else None
        )
