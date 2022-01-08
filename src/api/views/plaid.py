from flask import Blueprint
from flask import request

from core.repositories.account_repository import AccountRepository
from core.repositories.plaid_repository import PlaidRepository, PLAID_PRODUCTS_STRINGS
from auth.decorators import authed, get_identity
from api.metrics.plaid_metrics import *
from api.views.base import BaseApi
from flask_app import db


class PlaidApi(BaseApi):

    def __init__(self):
        super().__init__("/plaid", 'plaid')

    def register_api(self, app):
        self.add_url(app, "/info", self.info)
        self.add_url(app, "/link", self.create_link_token, methods=['POST',])
        self.add_url(app, "/access", self.get_access_token, methods=['POST',])


    @authed
    @PERF_PLAID_INFO.time()
    def info(self):
        """
        ---
        get:
            summary: Retrieve the current Profile's Plaid auth token
            responses:
                200:
                    content:
                        application/json:
                            type: object
                            schema:
                                item_id:
                                    type: string
                                access_token:
                                    type: string
                                products:
                                    type: array
                                    items:
                                        type: string
                400:
                    content:
                        application/json:
                            type: object
                            schema:
                                success:
                                    type: boolean
                                message:
                                    type: string
            tags:
                - Plaid
        """
        user = get_identity()
        repo = PlaidRepository(db)
        result = repo.info(user['id'])
        if result.success:
            return result.data

        return {
            'item_id': None,
            'access_token': None,
            'products': PLAID_PRODUCTS_STRINGS
        }


    @authed
    @PERF_PLAID_LINK.time()
    def create_link_token(self):
        """
        ---
        post:
            summary: Generate a link token for the user to auth on our behalf.
            responses:
                200:
                    content:
                        application/json:
                            type: object
                            schema:
                                item_id:
                                    type: string
                                products:
                                    type: array
                                    items:
                                        type: string
                400:
                    content:
                        application/json:
                            type: object
                            schema:
                                success:
                                    type: boolean
                                message:
                                    type: string
            tags:
                - Plaid
        """
        profile = get_identity()
        base_url = request.base_url
        repo = PlaidRepository(db)
        result = repo.create_link_token(profile['id'], base_url)
        if result.success:
            return result.data
        return {
            'success': False,
            'message': result.message
        }, 400


    @authed
    @PERF_PLAID_ACCESS.time()
    def get_access_token(self):
        """
        ---
        post:
            summary: Exchange a user's public request token for a private access token
            requestBody:
                content:
                    application/json:
                        type: object
                        schema:
                            public_token:
                                type: string
            responses:
                200:
                    content:
                        application/json:
                            type: object
                            schema:
                                success:
                                    type: boolean
                                message:
                                    type: string
                400:
                    content:
                        application/json:
                            type: object
                            schema:
                                success:
                                    type: boolean
                                message:
                                    type: string
            tags:
                - Plaid
        """

        profile = get_identity()
        public_token = request.json['public_token']

        repo = PlaidRepository(db)
        access_token_result = repo.get_access_token(profile['id'], public_token)
        if not access_token_result.success:
            return {
                'success': access_token_result.success,
                'message': access_token_result.message
            }, 400

        account_repo = AccountRepository(db)
        schedule_result = account_repo.schedule_account_sync(profile_id=profile['id'], plaid_item=access_token_result.data)

        if not schedule_result.success:
            return {
                'success': schedule_result.success,
                'message': schedule_result.message
            }, 500

        return {
            'success': access_token_result is not None,
            'message': 'Fetching accounts'
        }
