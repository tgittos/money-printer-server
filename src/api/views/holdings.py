from flask import Blueprint, request

from core.repositories import HoldingRepository
from api.schemas import read_holdings_schema, read_holding_schema, read_holding_balances_schema

from api.lib.constants import API_PREFIX
from api.routes.decorators import authed, get_identity
from api.views.base import BaseApi


class HoldingsApi(BaseApi):

    def __init__(self):
        super().__init__('/holdings')
    
    def register_api(self, app):
        self.add_url(app, "/", self.get_holdings_by_profile)
        self.add_url("/<holding_id>", self.get_holding)
        self.add_url("/<holding_id>/balances", self.get_holding_balances)


    @authed
    def get_holdings_by_profile():
        profile = get_identity()
        repo = HoldingRepository()
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


    @authed
    def get_holding(holding_id):
        profile = get_identity()
        repo = HoldingRepository()
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


    @authed
    def get_holding_balances(holding_id):
        profile = get_identity()
        repo = HoldingRepository()
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
