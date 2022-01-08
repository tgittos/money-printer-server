from flask import Blueprint, request, redirect, abort, send_from_directory
from datetime import datetime, timezone, timedelta

from constants import STONK_PREFIX
from auth import authed

from .repositories import StockRepository


prices_bp = Blueprint('prices', __name__)


@prices_bp.route(f'/{STONK_PREFIX}/prices/<symbol>/previous', methods=['GET'])
@authed
def symbol_previous(symbol):
    repo = StockRepository(db)

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


@prices_bp.route(f'/{STONK_PREFIX}/prices/<symbol>/intraday', methods=['GET'])
@authed
def symbol_intraday(symbol):
    start = request.args.get('start')
    repo = StockRepository(db)
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


@prices_bp.route(f'/{STONK_PREFIX}/prices/<symbol>/eod', methods=['GET'])
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

    repo = StockRepository(db)
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