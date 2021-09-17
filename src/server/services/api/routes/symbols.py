from datetime import datetime, timedelta
import json

from flask import Blueprint
from flask import request

from core.repositories.stock_repository import get_repository as get_stock_repository
from server.services.api.routes.decorators import authed

from server.services.api import load_config
app_config = load_config()

mysql_config = app_config['db']
iex_config = app_config['iexcloud']

# define the blueprint for symbol routes
symbol_bp = Blueprint('symbols', __name__)


@symbol_bp.route('/v1/api/symbols/<symbol>/previous', methods=['GET'])
@authed
def symbol_current(symbol):
    repo = get_stock_repository(iex_config=iex_config, mysql_config=mysql_config)

    # result is a data frame
    result = repo.previous(symbol)

    if result is None:
        return {
            'success': False,
            'message': 'last previous for symbol not found'
        }

    return {
        'success': True,
        'data': result.to_dict(orient='records')
    }


@symbol_bp.route('/v1/api/symbols/<symbol>/intraday', methods=['GET'])
@authed
def symbol_intraday(symbol):
    start = request.args.get('start')
    repo = get_stock_repository(iex_config=iex_config, mysql_config=mysql_config)

    result = repo.historical_intraday(
        symbol=symbol,
        start=int(float(start)),
    )

    return {
        'success': True,
        'data': result.to_json(orient='records')
    }


@symbol_bp.route('/v1/api/symbols/<symbol>/eod', methods=['GET'])
@authed
def symbol_eod(symbol):
    start = request.args.get('start')
    if start is None:
        start = datetime.utcnow() - timedelta(days=7)
        start = start.timestamp()
    else:
        start = int(float(start))

    end = request.args.get('end')
    if end is None:
        end = datetime.utcnow().timestamp()
    else:
        end = int(float(end))

    repo = get_stock_repository(iex_config=iex_config, mysql_config=mysql_config)

    result = repo.historical_daily(symbol, start=start, end=end)

    return {
        'success': True,
        'data': result.to_json(orient='records')
    }
