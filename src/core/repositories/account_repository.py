from marshmallow import Schema, fields

from core.repositories.scheduled_job_repository import ScheduledJobRepository
from core.repositories.repository_response import RepositoryResponse
from core.schemas.read_schemas import ReadAccountSchema
from core.schemas.create_schemas import CreateInstantJobSchema
from core.stores.mysql import MySql
from core.lib.logger import get_logger
from config import mysql_config

# import all the actions so that consumers of the repo can access everything
from core.lib.utilities import wrap
from core.lib.actions.account.crud import *
from core.lib.actions.profile.crud import get_profile_by_id


class GetAccountSchema(Schema):
    class Meta:
        fields=("profile_id", "account_id")

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

    def get_accounts_by_profile_with_balances(self, request: GetAccountSchema) -> RepositoryResponse:
        """
        Returns a list of accounts augmented with their latest synced balances for a given profile
        """
        profile_result = get_profile_by_id(self.db, request['profile_id'])
        if not profile_result.success: return profile_result
        action_result = self.get_accounts_by_profile(profile_result.data)
        return RepositoryResponse(success=action_result.success, data=action_result.data, message=action_result.message)

    def get_account_by_profile_with_balance(self, request: GetAccountSchema) -> RepositoryResponse:
        """
        Returns the requested Account with it's latest synced balance for a given profile
        """
        profile_result = get_profile_by_id(self.db, request['profile_id'])
        if not profile_result.success: return profile_result
        action_result = self.get_account_by_account_id(profile_result.data, request['account_id'])
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

        with self.db.get_session() as session:
            plaid_item = session.query(PlaidItem).where(
                PlaidItem.id == account_result.data.plaid_item_id).first()

        if plaid_item is None:
            self.logger.error(
                "scheduled account sync for plaid item, but no PlaidItem found")
            return RepositoryResponse(
                success=False,
                message=f"Could not find plaid item for account"
            )

        scheduled_job_repo = ScheduledJobRepository()

        return scheduled_job_repo.create_instant_job(CreateInstantJobSchema(
            job_name='sync_accounts',
            args={
                'plaid_item_id': plaid_item.id
            }
        ))
