from marshmallow import EXCLUDE
from datetime import date, timedelta

from core.stores.mysql import MySql
from core.apis.plaid.investments import PlaidInvestments, PlaidInvestmentsConfig
from core.lib.logger import get_logger
from config import mysql_config, plaid_config
from core.actions.plaid.crud import get_plaid_item_by_id
from core.schemas.holding_schemas import CreateHoldingSchema
from core.schemas.security_schemas import CreateSecuritySchema
from core.repositories.repository_response import RepositoryResponse
from core.models.plaid_item import PlaidItem

# import all the facets so that consumers of the repo can access everything
from core.actions.security.crud import *
from core.actions.profile.crud import get_profile_by_id
from core.actions.account.crud import get_account_by_id


class SecurityRepository:

    logger = get_logger(__name__)
    db = MySql(mysql_config)

    def __init__(self):
        self.plaid_config = plaid_config

    def get_securities_by_profile_id(self, profile_id: int) -> RepositoryResponse:
        """
        Returns a list of securites that belong to holdings for the given profile ID
        """
        raise Exception("not implemented")

        # profile_result = get_profile_by_id(profile_id)
        # if not profile_result.success: return profile_result
        # profile = profile_result.data
        # with self.db.get_session() as session:
        #     data = session.query(Security).join_from()

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
