from flask import Blueprint, request

from core.repositories import HoldingRepository
from core.schemas.holding_schemas import *

from api.lib.constants import API_PREFIX
from api.routes.decorators import authed, get_identity

holdings_bp = Blueprint('holding', __name__)


@holdings_bp.route(f"/{API_PREFIX}/holdings", methods=['GET'])
@authed
def get_holdings_by_profile():
    profile = get_identity()
    repo = HoldingRepository()
    print(profile)
    result = repo.get_holdings_by_profile_id(profile['id'])
    print(result.success)
    print(result.data)
    print(result.message)
    if result.success:
        return {
            'success': True,
            'data': ReadHoldingSchema(many=True).dump(result.data)
        }
    return {
        'success': result.success,
        'message': result.message
    }, 404


@holdings_bp.route(f"/{API_PREFIX}/holdings/<holding_id>", methods=['GET'])
@authed
def get_holding(holding_id):
    repo = HoldingRepository()
    result = repo.get_holding_by_id(holding_id=holding_id)
    if result.success:
        return {
            'success': True,
            'data': ReadHoldingSchema().dump(result.data)
        }
    return {
        'success': result.success,
        'message': result.message
    }, 404


@holdings_bp.route(f"/{API_PREFIX}/holdings/<holding_id>/balances", methods=['GET'])
@authed
def get_holding_balances(holding_id):
    repo = HoldingRepository()
    result = repo.get_holding_balances_by_holding_id(holding_id)
    if result.success:
        return {
            'success': True,
            'data': ReadHoldingBalanceSchema(many=True, exclude=("holding",)).dump(result.data)
        }
    return {
        'success': result.success,
        'message': result.message
    }, 404


@holdings_bp.route(f"/{API_PREFIX}/holdings/<holding_id>/performance", methods=['GET'])
@authed
def holding_performance():
    return {}, 404


@holdings_bp.route(f"/{API_PREFIX}/holdings/<holding_id>/forecast", methods=['GET'])
@authed
def holding_forecast():
    return {}, 404
