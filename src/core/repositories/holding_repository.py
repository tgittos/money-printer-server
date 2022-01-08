from sqlalchemy import and_

from core.models import Account, Holding, Security
from core.stores.database import Database
from core.repositories.scheduled_job_repository import ScheduledJobRepository
from core.repositories.repository_response import RepositoryResponse
from core.schemas import CreateInstantJobSchema
from core.lib.logger import get_logger
from core.apis.plaid.investments import PlaidInvestments, PlaidInvestmentsConfig

import core.actions.holding.holding_crud as crud
from core.actions.account.crud import get_accounts_by_plaid_item_id, get_account_by_id
from core.actions.profile.crud import get_profile_by_id
from core.actions.plaid.crud import get_plaid_item_by_id

import config

class HoldingRepository:

    logger = get_logger(__name__)
    scheduled_job_repo = ScheduledJobRepository()
    plaid_config = config.plaid

    def __init__(self, db):
        self.db = db

    def get_holding_by_id(self, profile_id: int, holding_id: int) -> RepositoryResponse:
        return crud.get_holding_by_id(self.db, profile_id, holding_id)

    def get_holdings_by_profile_id(self, profile_id: int) -> RepositoryResponse:
        return crud.get_holdings_by_profile_id(self.db, profile_id)

    def get_holding_balances_by_holding_id(self, profile_id: int, holding_id: int) -> RepositoryResponse:
        return crud.get_holding_balances_by_holding_id(self.db, profile_id, holding_id)

    def schedule_update_holdings(self, profile_id: int, plaid_item_id: int) -> RepositoryResponse:
        """
        Creates an InstantJob to perform a sync_holdings job for all investment accounts attached to a PlaidItem
        """
        plaid_result = get_plaid_item_by_id(self.db, profile_id, plaid_item_id)
        if not plaid_result.success:
            self.logger.error(
                "cannot schedule account holding sync without plaid item")
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        return self.scheduled_job_repo.create_instant_job(CreateInstantJobSchema().load({
            'job_name': 'sync_holdings',
            'json_args': {
                'plaid_item_id': plaid_result.data.id
            }
        }))

    def schedule_update_transactions(self, profile_id: int, plaid_item_id: int) -> RepositoryResponse:
        """
        Creates an InstantJob to perform a sync_transactions job for all investment accounts attached to a PlaidItem
        """
        plaid_result = get_plaid_item_by_id(self.db, profile_id, plaid_item_id)
        if not plaid_result.success:
            self.logger.error(
                "cannot schedule investment transaction sync without plaid item")
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        return self.scheduled_job_repo.create_instant_job(CreateInstantJobSchema().load({
            'job_name': 'sync_transactions',
            'json_args': {
                'plaid_item_id': plaid_item_id
            }
        }))

    def update_holdings(self, profile_id: int, plaid_item_id: int) -> RepositoryResponse:
        """
        Performs a sync of all security holdings for accounts associated with a PlaidItem
        """
        plaid_result = get_plaid_item_by_id(self.db, profile_id, plaid_item_id)
        if not plaid_result.success:
            self.logger.warning(
                "requested update holding but no PlaidItem given")
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        with self.db.get_session() as session:
            accounts = session.query(Account).filter(
                Account.plaid_item_id == plaid_result.data.id).all()

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
            self.logger.info(
                "updating holdings for account: {0}".format(account.id))
            self.security_repo.sync_holdings(profile=profile, account=account)
            accounts_updated += 1

        self.logger.info(
            "updated holdings for {0} accounts".format(accounts_updated))

        return RepositoryResponse(
            success=True
        )

    def update_transactions(self, profile_id, plaid_item_id: int) -> RepositoryResponse:
        """
        Performs a sync of all security transactions for accounts associated with a PlaidItem
        """
        plaid_result = get_plaid_item_by_id(self.db, profile_id, plaid_item_id)
        if not plaid_result.success:
            self.logger.error(
                "cannot update investment transactions without a valid plaid_item_id")
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        profile_result = get_profile_by_id(self, plaid_result.data.profile_id)
        accounts_result = get_accounts_by_plaid_item_id(
            self, profile_id, plaid_result.data.id)
        if not profile_result.success or not accounts_result.success:
            self.logger.error("received request to update investment transactions with no corresponding accounts: {0}"
                              .format(plaid_result.data.id))
            return RepositoryResponse(
                success=False,
                message=f"Either no Profile for PlaidItem {plaid_item_id} found, or no Accounts for PlaidItem found"
            )

        accounts_updated = 0
        for account in accounts_result.data:
            self.logger.info(
                "updating investment transactions for account: {0}".format(account.id))
            self.security_repo.sync_transactions(
                profile=profile_result.data, account=account)
            accounts_updated += 1
        self.logger.info(
            "updated investment transactions for {0} accounts".format(accounts_updated))

        return RepositoryResponse(
            success=True
        )

    def calculate_performance(self, profile_id: int, holding_id: int) -> RepositoryResponse:
        # pull the holding
        # pull security_prices for holding
        # using cost basis of holding, at each security_price data point, calculate a rate of return
        raise Exception("Not implemented")

    def calculate_forecast(self, profile_id: int, holding_id: int) -> RepositoryResponse:
        raise Exception("Not implemented")


    def get_holdings_by_profile_id_and_account_id(self, profile_id: int, account_id: int) -> RepositoryResponse:
        """
        Returns all the holdings that belong to the given account
        """
        return crud.get_holdings_by_profile_id_and_account_id(self.db, profile_id, account_id)

    def sync_holdings(self, profile_id: int, account_id: int) -> RepositoryResponse:
        profile_result = get_profile_by_id(self.db, profile_id)
        if not profile_result.success:
            self.logger.error(
                "requested holdings sync on account with no Profile given")
            return RepositoryResponse(
                success=False,
                message=profile_result.message
            )

        account_result = get_account_by_id(self.db, account_id)
        if not account_result.success:
            self.logger.error(
                "requested holdings sync on account with no Account given")
            return RepositoryResponse(
                success=False,
                message=account_result.message
            )

        plaid_result = get_plaid_item_by_id(
            self, account_result.data.plaid_item_id)
        if not plaid_result.success:
            self.logger.error("requested holdings sync on account but couldn't find plaid_item: {0}"
                              .format(account_id))
            return RepositoryResponse(
                success=False,
                message=plaid_result.message
            )

        api = PlaidInvestments(PlaidInvestmentsConfig(self.plaid_config))
        investment_dict = api.get_investments(plaid_result.data.access_token)

        # update securities from this account
        # these might not be account specific, but institution specific
        # so there's a chance I can detach it from the profile/account and just
        # link it in from the holdings
        for security_dict in investment_dict["securities"]:
            security_result = self.get_security_by_security_id(
                plaid_security_id=security_dict['security_id'])
            if not security_result.success:
                schema = CreateSecuritySchema(unknown=EXCLUDE).load({
                    **{'profile': plaid_result.data, 'account': account_result.data},
                    **security_dict
                })
                security = self.create_security(schema)

        # update the holdings
        for holding_dict in investment_dict["holdings"]:
            security_result = self.get_security_by_security_id(
                holding_dict['security_id'])
            holding_result = self.get_holding_by_plaid_account_id_and_plaid_security_id(
                holding_dict["account_id"],
                holding_dict["security_id"])
            if not holding_result.success:
                self.create_holding(CreateHoldingSchema(unknown=EXCLUDE).load({
                    **{'account': account_result.data, 'security': security_result.data},
                    **holding_dict
                }))
            else:
                self.update_holding_balance(UpdateHoldingSchema(unknown=EXCLUDE).load({
                    ** {'holding': holding_result.data},
                    **holding_dict
                }))

        return RepositoryResponse(
            success=True
        )

    def sync_transactions(self, profile_id: int, account_id: int) -> RepositoryResponse:
        account_result = get_account_by_id(self.db, account_id)
        if not account_result.success:
            self.logger.error(
                "requested holdings sync on account that couldn't be found: {0}".format(account_id))
            return RepositoryResponse(
                success=False,
                message=account_result.message
            )

        with self.db.get_session() as session:
            plaid_item = session.query(PlaidItem).where(
                PlaidItem.id == account_result.data.plaid_item_id).first()

        if plaid_item is None:
            self.logger.error(
                "requested holdings sync on account but couldn't find plaid_item: {0}".format(account_result.data.plaid_item_id))
            return RepositoryResponse(
                success=False,
                message=f"No PlaidItem found with ID {account_result.data.plaid_item_id}"
            )

        api = PlaidInvestments(PlaidInvestmentsConfig(self.plaid_config))

        # if we have no transactions for this account, try and pull the last years
        # otherwise, we probably got a notification from a webhook to update, so just
        # update the last week's worth of transactions
        start = date.today()
        end = start - timedelta(days=365)

        if self._has_transactions(account_result.data):
            end = start - timedelta(days=7)

        transactions_dict = api.get_transactions(
            plaid_item.access_token, start=start, end=end)

        if 'transactions' not in transactions_dict:
            self.logger.info("upstream provider returned 0 transactions for date period {0} - {1}"
                             .format(start, end))
            return

        transactions = []

        for transaction_dict in transactions_dict:
            if 'account_id' not in transaction_dict:
                self.logger.error("upstream gave investment transaction result with missing account id: {0}",
                                  transaction_dict)
                continue

            investment_transaction = self._get_investment_transaction_by_investment_transaction_id(
                transaction_dict['investment_transaction_id'])

            if investment_transaction is None:
                investment_transaction = self.create_investment_transaction(
                    CreateInvestmentTransactionSchema(unknown=EXCLUDE).load({
                        **{'account': account_result.data},
                        **transaction_dict
                    }))

            transactions.append(transactions)

        return RepositoryResponse(
            success=True,
            data=transactions
        )

    def _has_transactions(self, account: Account) -> bool:
        with self.db.get_session() as session:
            r = session.query(InvestmentTransaction).filter(
                InvestmentTransaction.account_id == account.id).count() > 0

        return r

    def _get_investment_transaction_by_investment_transaction_id(self, investment_transaction_id):
        with self.db.get_session() as session:
            return session.query(InvestmentTransaction).filter(
                InvestmentTransaction.investment_transaction_id == investment_transaction_id
            ).first()