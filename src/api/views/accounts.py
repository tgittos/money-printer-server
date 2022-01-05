from flask import abort

from core.repositories import AccountRepository, SecurityRepository
from api.schemas import read_holdings_schema, read_accounts_schema, read_account_balances_schema
from api.views.decorators import authed, get_identity

from api.views.base import BaseApi
from api.lib.constants import API_PREFIX


class AccountsApi(BaseApi):

    def __init__(self):
        super().__init__('/accounts', 'accounts')

    def register_api(self, app):
        self.add_url(app, "/", self.list_accounts)
        self.add_url(app, '/<account_id>/sync', self.request_account_sync)
        self.add_url(app, "/<account_id>/balances", self.request_account_balances)
        self.add_url(app, "/<account_id>/holdings", self.list_holdings)


    @authed
    def list_accounts(self):
        """
        ---
        get:
            summary: Get a list of all accounts the belong to the signed in profile
            security:
                - jwt: []
            responses:
                200:
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    success:
                                        type: boolean
                                    data:
                                        type: array
                                        items: ReadAccountApiSchema
            tags:
                - Account
        """
        user = get_identity()
        account_repo = AccountRepository()
        accounts = account_repo.get_accounts_by_profile_id(profile_id=user['id'])
        if accounts.success and accounts.data is not None:
            return {
                'success': True,
                'data': read_accounts_schema().dump(accounts.data)
            }
        else:
            abort(404)


    @authed
    def request_account_sync(self, account_id: int):
        """
        ---
        post:
            summary: Schedule an immediate sync of specified account attached to the profile
            security:
                - jwt: []
            responses:
                200:
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    success:
                                        type: boolean
            tags:
                - Account
        """
        user = get_identity()
        account_repo = AccountRepository()
        result = account_repo.schedule_account_sync(user['id'], account_id)
        if result.success:
            return {
                'success': True
            }
        return {
            'success': False
        }, 400


    @authed
    def request_account_balances(self, account_id):
        """
        ---
        get:
            summary: Get a historical list of account balances for a given account
            security:
                - jwt: []
            responses:
                200:
                    description: Account balance object
                    content:
                        application/json:
                            type: object
                            properties:
                                success:
                                    type: boolean
                                data:
                                    type: array
                                    items: ReadAccountBalanceApiSchema
            tags:
                - Account
        """
        user = get_identity()
        account_repo = AccountRepository()
        balance_result = account_repo.get_balances_by_account_id(
            user['id'], account_id)
        if not balance_result or balance_result is None:
            abort(404)
        return {
            'success': True,
            'data': read_account_balances_schema.dump(balance_result.data)
        }


    @authed
    def list_holdings(self, account_id):
        """
        ---
        get:
            summary: Get a list of investment holdings for a given account
            security:
                - jwt: []
            responses:
                200:
                    description: Holding object
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    success:
                                        type: boolean
                                    data:
                                        type: array
                                        items: ReadHoldingApiSchema
            tags:
                - Account
        """
        user = get_identity()
        security_repo = SecurityRepository()
        holding_result = security_repo.get_holdings_by_profile_id_and_account_id(
            profile_id=user['id'], account_id=account_id)
        if not holding_result.success or holding_result.data is None:
            abort(404)
        return {
            'success': True,
            'data': read_holdings_schema.dump(holding_result.data)
        }
