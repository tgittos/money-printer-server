import sys
sys.path.append('./../../src')

from os import path
from flask import send_from_directory, request
from flask_cors import cross_origin
from datetime import datetime

from server import app
from lib.stores.mysql import Mysql
from lib.oscillators import macd, rsi


# candle data
@app.route('/v1/candles/<symbol>')
def get_candles(symbol):
    start = datetime.fromtimestamp(int(float(request.args.get('start'))))
    end = datetime.fromtimestamp(int(float(request.args.get('end'))))
    db = _get_db()
    if start != None and end != None:
        data = db.get_candles_by_symbol_in_window(symbol, start, end, debug=True)
    else:
        data = db.get_candles_by_symbol(symbol)
    return {
        'success': True,
        'data': list([{
            'symbol': symbol,
            'candles': data.to_json()
        }])
    }