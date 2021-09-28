from datetime import datetime, timedelta, timezone

from flask import Blueprint
from flask import request

from core.repositories.stock_repository import StockRepository
from .decorators import authed
from config import mysql_config, iex_config

# define the blueprint for symbol routes
symbol_bp = Blueprint('symbols', __name__)


@symbol_bp.route('/v1/api/symbols/<symbol>/previous', methods=['GET'])
@authed
def symbol_previous(symbol):
    repo = StockRepository()

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
    repo = StockRepository()
    # parse given start date
    start_date = datetime.fromtimestamp(float(start), tz=timezone.utc)

    result = repo.historical_intraday(
        symbol=symbol,
        start=start_date,
    )

    if result is None:
        return {
            'success': False,
            'message': 'no data found for symbol {0} over time period {1} - {2}'.format(
                symbol,
                start_date,
                "now"
            )
        }, 404

    return {
        'success': True,
        'data': result.to_dict(orient='records')
    }


@symbol_bp.route('/v1/api/symbols/<symbol>/eod', methods=['GET'])
@authed
def symbol_eod(symbol):
    start = request.args.get('start')
    if start is None:
        start = datetime.now(tz=timezone.utc) - timedelta(days=30)
    else:
        start = datetime.fromtimestamp(float(start), tz=timezone.utc)

    end = request.args.get('end')
    if end is None:
        end = datetime.now(tz=timezone.utc)
    else:
        end = datetime.fromtimestamp(float(end), tz=timezone.utc)

    repo = StockRepository()
    result = repo.historical_daily(symbol, start=start, end=end)

    if result is None:
        return {
            'success': False,
            'message': 'no data found for symbol {0} over time period {1} - {2}'.format(
                symbol,
                start,
                end
            )
        }, 404

    return {
        'success': True,
        'data': result.to_dict(orient='records')
    }
