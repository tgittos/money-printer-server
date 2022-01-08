from flask import Blueprint, request

from core.repositories import HoldingRepository
from auth.decorators import Authed, get_identity
from api.schemas import read_holdings_schema, read_holding_schema, read_holding_balances_schema
from api.views.base import BaseApi
from api.flask_app import db


class HoldingsApi(BaseApi):

    def __init__(self):
        super().__init__('/holdings', 'holding')

    def register_api(self, app):
        self.add_url(app, "/", self.get_holdings_by_profile)
        self.add_url(app, "/<holding_id>", self.get_holding)
        self.add_url(app, "/<holding_id>/balances", self.get_holding_balances)


    @Authed
    def get_holdings_by_profile(self):
        profile = get_identity()
        repo = HoldingRepository(db)
        result = repo.get_holdings_by_profile_id(profile['id'])
        if result.success:
            return {
                'success': True,
                'data': read_holdings_schema.dump(result.data)
            }
        return {
            'success': result.success,
            'message': result.message
        }, 404


    @Authed
    def get_holding(self, holding_id):
        profile = get_identity()
        repo = HoldingRepository(db)
        result = repo.get_holding_by_id(
            profile_id=profile['id'], holding_id=holding_id)
        if result.success:
            return {
                'success': True,
                'data': read_holding_schema.dump(result.data)
            }
        return {
            'success': result.success,
            'message': result.message
        }, 404


    @Authed
    def get_holding_balances(self, holding_id):
        profile = get_identity()
        repo = HoldingRepository(db)
        result = repo.get_holding_balances_by_holding_id(profile['id'], holding_id)
        if result.success:
            return {
                'success': True,
                'data': read_holding_balances_schema.dump(result.data)
            }
        return {
            'success': result.success,
            'message': result.message
        }, 404
