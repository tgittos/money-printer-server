import sys
sys.path.append('./../../src')

from os import path
from flask import send_from_directory, request
from flask_cors import cross_origin
from datetime import datetime

from server import app
from lib.stores.mysql import Mysql
from lib.oscillators import macd, rsi

# oscillators
@app.route('/v1/oscillators/<oscillator>/<symbol>')
def get_oscillator(oscillator, symbol):
    db = _get_db()
    data = db.get_candles_by_symbol(symbol)
    try:
        vals = getattr(self, oscillator)(data)
        return {
            'success': True,
            'data': list([{
                'symbol': symbol,
                oscillator: vals.to_json()
            }])
        }
    except:
        return {
            'success': False
        }