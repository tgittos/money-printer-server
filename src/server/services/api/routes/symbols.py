from flask import Blueprint
from flask import request
import json

from core.repositories.stock_repository import *
from server.services.api.routes.decorators import authed


# define the blueprint for symbol routes
symbol_bp = Blueprint('symbols', __name__)

@symbol_bp.route('/v1/api/symbols/<symbol>/intraday', methods=['GET'])
@authed
def symbol_intraday(symbol):
    start = request.args.get('start')

    repo = get_repository()

    result = repo.historical_intraday(
        symbol=symbol,
        start=int(float(start)),
    )

    return {
        'success': True,
        'data': result.to_json(orient='records')
    }
