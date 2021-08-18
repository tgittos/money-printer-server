import sys
sys.path.append('./../../src')

from os import path
from flask import send_from_directory, request
from flask_cors import cross_origin
from datetime import datetime

from server import app
from lib.stores.mysql import Mysql
from lib.oscillators import macd, rsi

@app.route('/v1/symbols', methods = ['POST'])
def track_symbol():
    json_data = request.get_json(force=True)
    print(json_data)
    db = _get_db()
    symbol = json_data['symbol']
    data = db.add_to_sync(symbol, 30)
    return {
        'success': True,
        'data': list([{
            'symbol': sync.symbol,
            'last_update': sync.last_update
        } for sync in data])
    }

@app.route('/v1/symbols', methods = ['GET'])
def get_tracked_symbols():
    db = _get_db()
    data = db.get_sync()
    return {
        'success': True,
        'data': list([{
            'symbol': sync.symbol,
            'last_update': sync.last_update
        } for sync in data])
    }

@app.route('/v1/symbols/<symbol>', methods = ['DELETE'])
def untrack_symbol(symbol):
    db = _get_db()
    db.remove_from_sync(symbol)
    return {
        'success': True
    }
