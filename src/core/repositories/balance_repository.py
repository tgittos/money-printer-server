from marshmallow import EXCLUDE

from core.apis.plaid.accounts import Accounts, AccountsConfig
from core.models.plaid_item import PlaidItem
from core.repositories.scheduled_job_repository import ScheduledJobRepository
from core.repositories.plaid_repository import PlaidRepository
from core.stores.mysql import MySql
from core.lib.logger import get_logger
from config import mysql_config, plaid_config, mailgun_config
from core.repositories.repository_response import RepositoryResponse
from core.schemas.create_schemas import CreateInstantJobSchema

# import all the actions so that consumers of the repo can access everything
from core.lib.utilities import wrap
from core.lib.actions.balance.crud import *
from core.lib.actions.plaid.crud import get_plaid_item_by_id
from core.lib.actions.account.crud import get_account_by_id


class BalanceRepository:

    logger = get_logger(__name__)
    db = MySql(mysql_config)

    def __init__(self):
        self.scheduled_job_repo = ScheduledJobRepository()
        self.plaid_repo = PlaidRepository()
        self._init_facets()

    def _init_facets(self):
        self.create_account_balance = wrap(create_account_balance, self.db)

    def schedule_update_all_balances(self, plaid_item_id: int) -> RepositoryResponse:
        """
        Schedules an instant job to update the balances of all accounts attached to a plaid Link item
        """
        plaid_result = get_plaid_item_by_id(self.db, plaid_item_id)
        if not plaid_result.success:
            self.logger.warning("requested schedule update all balances without PlaidItem")
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

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
        account_result = get_account_by_id(self.db, account_id)
        if not account_result.success:
            self.logger.warning("requested schedule update balance without Account")
            return RepositoryResponse(
                success=False,
                message=account_result.message
            )

        plaid_result = self.plaid_repo.get_plaid_item_by_id(account_result.data.plaid_item_id)
        if not plaid_result.success:
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

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
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        self.logger.info("syncing account balance/s for plaid item: {0}".format(plaid_result.data.id))

        with self.db.get_session() as session:
            accounts = session.query(Account).where(Account.plaid_item_id == plaid_result.data.id).all()

        if accounts and len(accounts) > 0:
            self.logger.info("found {0} accounts to update".format(len(accounts)))
            for account in accounts:
                self.sync_account_balance(account.id)
            self.logger.info("done updating balances for plaid item")
        else:
            self.logger.warning("requested account sync of plaid item {0} but no accounts found".format(plaid_result.data.id))
        
        return RepositoryResponse(
            success=True
        )

    def sync_account_balance(self, account_id: int) -> RepositoryResponse:
        """
        Fetches the latest balance for the given account from Plaid
        Returns None on any error
        """
        account_result = get_account_by_id(self.db, account_id)
        if not account_result.success:
            self.logger.warning("requested balance sync for account with no Account")
            return RepositoryResponse(
                success=False,
                message=account_result.message
            )

        self.logger.info("syncing account balance for account id: {0}".format(account_result.data.id))

        with self.db.get_session() as session:
            plaid_item = session.query(PlaidItem).where(PlaidItem.id == account_result.data.plaid_item_id).first()

        if plaid_item is None:
            self.logger.warning("could not find PlaidItem attached to account {0}".format(account_result.data.id))
            return RepositoryResponse(
                success=False,
                message=f"Could not find PlaidItem for Account with ID {account_id}"
            )

        api = Accounts(AccountsConfig(self.plaid_config))
        response_dict = api.get_account_balance(plaid_item.access_token, account_result.data.account_id)

        if response_dict is None or 'accounts' not in response_dict:
            self.logger.error("unusual response from upstream: {0}".format(response_dict))
            return RepositoryResponse(
                success=False,
                message=f"Could not find 'accounts' key on response from upstream"
            )

        balances = []

        for account_dict in response_dict['accounts']:
            balance_dict = account_dict['balances']

            schema = CreateAccountBalanceSchema(unknown=EXCLUDE).load({
                **{ 'account':account_result.data },
                **balance_dict
            })
            balance_result = create_account_balance(self.db, schema)

            if balance_result.success:
                balances.append(balance_result.data)
            else:
                self.logger.warning(f"account_balance creation failed with message {balance_result.message}")

        return RepositoryResponse(
            success=balances[0] is not None,
            data=balances[0],
            message= "Unknown error fetching balances" if balances[0] is None else None
        )
