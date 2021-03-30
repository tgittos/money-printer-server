from flask import Flask
from flask_restful import Api

from symbol import Tracking as SymbolTracking

app = Flask(__name__)
api = Api(app)

# add endpoints
api.add_resource(SymbolTracking, '/symbols/tracking')
api.add_resource(Candles, '/candles')
api.add_resource(Options, '/options')

if __name__ == '__main__':
    app.run()  # run our Flask app