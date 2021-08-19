import sys
sys.path.append('./../src')

from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.url_map.strict_slashes = False

CORS(app)

from config import DevelopmentConfig
from routes import *

if __name__ == '__main__':
    # run Flask app
    print(" * running money-printer server with config: {0}".format(DevelopmentConfig))
    app.config.from_object(DevelopmentConfig)
    app.run(host=DevelopmentConfig.HOST, port=DevelopmentConfig.PORT)