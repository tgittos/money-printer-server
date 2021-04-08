import sys
sys.path.append('./../../src')

from os import path
from flask import send_from_directory, request
from flask_cors import cross_origin
from datetime import datetime

from server import app
from lib.stores.mysql import Mysql
from lib.oscillators import macd, rsi

root_dir = path.abspath(path.join(path.dirname(__file__), '../client'))

# static client site routes
@app.route('/v1/')
@app.route('/v1/index')
def serve_client():
    return send_from_directory(root_dir, 'index.html')

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

def _get_db():
    mysql = Mysql()
    return mysql