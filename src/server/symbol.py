import sys
sys.path.append('./../../src')

from flask_restful import Resource, reqparse

from lib.stores.mysql import Mysql;

def get_db(self):
    db = Mysql()
    return db.get_session()

class Tracking(Resource):
    
    def get(self):
        db = get_db()
        data = db.get_sync()
        return data
        
    def post(self, symbol):
        db = get_db()
        data = db.add_to_sync(symbol, 30)
        return data
    
    def delete(self, symbol):
        db = get_db()
        db.remove_from_sync(symbol)

class Candles(Resource):
    
    def get(self, symbol):
        db = get_db()
        data = db.get_candles_by_symbol(symbol)
        return data