from core.models.account import Account
from core.models.plaid_item import PlaidItem
from core.models.holding import Holding
from core.stores.mysql import MySql
from core.repositories.scheduled_job_repository import ScheduledJobRepository
from core.repositories.security_repository import SecurityRepository
from core.lib.logger import get_logger
from config import mysql_config
from core.repositories.repository_response import RepositoryResponse
from core.schemas.create_schemas import CreateInstantJobSchema

from core.lib.actions.account.crud import get_accounts_by_plaid_item
from core.lib.actions.profile.crud import get_profile_by_id
from core.lib.actions.plaid.crud import get_plaid_item_by_id

# import all the actions so that consumers of the repo can access everything
# no actions right now!


class HoldingRepository:

    logger = get_logger(__name__)
    db = MySql(mysql_config)

    def __init__(self):
        self.scheduled_job_repo = ScheduledJobRepository()
        self.security_repo = SecurityRepository()
    
    def get_holdings_by_profile_id(self, profile_id: int) -> RepositoryResponse:
        """
        Returns the holdings for a given profile ID
        """
        with self.db.get_session() as session:
            data = session.query(Holding).where(Holding.account.profile_id == profile_id).all()
        return RepositoryResponse(
            success=data is not None,
            data = data
        )

    def schedule_update_holdings(self, plaid_item_id: int) -> RepositoryResponse:
        """
        Creates an InstantJob to perform a sync_holdings job for all investment accounts attached to a PlaidItem
        """
        plaid_result = get_plaid_item_by_id(self.db, plaid_item_id)
        if not plaid_result.success:
            self.logger.error("cannot schedule account holding sync without plaid item")
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        return self.scheduled_job_repo.create_instant_job(CreateInstantJobSchema(
            job_name='sync_holdings',
            args={
                'plaid_item_id': plaid_result.data.id
            }
        ))

    def schedule_update_transactions(self, plaid_item_id: int) -> RepositoryResponse:
        """
        Creates an InstantJob to perform a sync_transactions job for all investment accounts attached to a PlaidItem
        """
        plaid_result = get_plaid_item_by_id(self.db, plaid_item_id)
        if not plaid_result.success:
            self.logger.error("cannot schedule investment transaction sync without plaid item")
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        return self.scheduled_job_repo.create_instant_job(CreateInstantJobSchema(
            job_name='sync_transactions',
            args={
                'plaid_item_id': plaid_item.id
            }
        ))

    def update_holdings(self, plaid_item_id: int) -> RepositoryResponse:
        """
        Performs a sync of all security holdings for accounts associated with a PlaidItem
        """
        plaid_result = get_plaid_item_by_id(self.db, plaid_item_id)
        if not plaid_result.success:
            self.logger.warning("requested update holding but no PlaidItem given")
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        with self.db.get_session() as session:
            accounts = session.query(Account).filter(Account.plaid_item_id == plaid_result.data.id).all()

        profile = None
        if accounts is None or len(accounts) == 0:
            self.logger.error("received request to update holdings with no corresponding accounts: {0}"
                              .format(plaid_result.data.id))
            return RepositoryResponse(
                success=False,
                message=f"Could not find Accounts for PlaidItem with ID {plaid_item_id}"
            )

        accounts_updated = 0
        for account in accounts:
            if profile is None:
                profile = get_profile_by_id(self, plaid_result.data.profile_id)
            self.logger.info("updating holdings for account: {0}".format(account.id))
            self.security_repo.sync_holdings(profile=profile, account=account)
            accounts_updated += 1

        self.logger.info("updated holdings for {0} accounts".format(accounts_updated))

        return RepositoryResponse(
            success=True
        )

    def update_transactions(self, plaid_item_id: int) -> RepositoryResponse:
        """
        Performs a sync of all security transactions for accounts associated with a PlaidItem
        """
        plaid_result = get_plaid_item_by_id(self.db, plaid_item_id)
        if not plaid_result.success:
            self.logger.error("cannot update investment transactions without a valid plaid_item_id")
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        profile_result = get_profile_by_id(self, plaid_result.data.profile_id)
        accounts_result = get_accounts_by_plaid_item(self, plaid_result.data)
        if not profile_result.success or not accounts_result.success:
            self.logger.error("received request to update investment transactions with no corresponding accounts: {0}"
                              .format(plaid_result.data.id))
            return RepositoryResponse(
                success=False,
                message=f"Either no Profile for PlaidItem {plaid_item_id} found, or no Accounts for PlaidItem found"
            )

        accounts_updated = 0
        for account in accounts_result.data:
            self.logger.info("updating investment transactions for account: {0}".format(account.id))
            self.security_repo.sync_transactions(profile=profile_result.data, account=account)
            accounts_updated += 1
        self.logger.info("updated investment transactions for {0} accounts".format(accounts_updated))

        return RepositoryResponse(
            success=True
        )

    def calculate_performance(self, holding_it: int) -> RepositoryResponse:
        # pull the holding
        # pull security_prices for holding
        # using cost basis of holding, at each security_price data point, calculate a rate of return
        raise Exception("Not implemented")

    def calculate_forecast(self, holding_id: int) -> RepositoryResponse:
        raise Exception("Not implemented")

