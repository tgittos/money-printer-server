import sys
sys.path.append('./../src')

from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from routes import *

if __name__ == '__main__':
    # boot the scheduler
    # run Flask app
    app.run()