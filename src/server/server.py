import sys
sys.path.append('./../src')

from flask import Flask, send_from_directory
from flask_cors import CORS

import scheduler

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.url_map.strict_slashes = False

CORS(app)

from routes import *

if __name__ == '__main__':
    # boot the scheduler
    scheduler.start()
    # run Flask app
    app.run()