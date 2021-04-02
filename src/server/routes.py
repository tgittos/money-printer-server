import sys
sys.path.append('./../../src')

from os import path
from flask import send_from_directory
from flask_cors import cross_origin

from server import app
from lib.stores.mysql import Mysql;

root_dir = path.abspath(path.join(path.dirname(__file__), '../client'))

# static client site routes
@app.route('/v1/')
@app.route('/v1/index')
def serve_client():
    return send_from_directory(root_dir, 'index.html')

# tracking symbols
@app.route('/v1/symbols', methods = ['GET'])
@cross_origin()
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

@app.route('/v1/symbols', methods = ['POST'])
@cross_origin()
def track_symbol(symbol):
    db = _get_db()
    data = db.add_to_sync(symbol, 30)
    return data

@app.route('/v1/symbols', methods = ['DELETE'])
@cross_origin()
def untrack_symbol(symbol):
    db = _get_db()
    db.remove_from_sync(symbol)

# candle data
def get_candles(symbol):
    db = _get_db()
    data = db.get_candles_by_symbol(symbol)
    return data

# oscillators

#

def _get_db():
    mysql = Mysql()
    return mysql