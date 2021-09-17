from flask import Blueprint, request

from server.services.api.routes.decorators import authed

holdings_bp = Blueprint('holding', __name__)


@holdings_bp.route('/v1/api/holding/<holding_id>/performance', methods=['GET'])
@authed
def holding_performance():
    return {
        'success': False
    }


@holdings_bp.route('/v1/api/holding/<holding_id>/forecast', methods=['GET'])
@authed
def holding_forecast():
    return {
        'success': False
    }

