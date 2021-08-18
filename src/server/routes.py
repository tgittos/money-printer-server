import sys
sys.path.append('./../../src')

from routes.oauth import *
from routes.symbols import *
from routes.oscillators import *
from routes.candles import *

# static client site routes
root_dir = path.abspath(path.join(path.dirname(__file__), '../client'))
@app.route('/v1/')
@app.route('/v1/index')
def serve_client():
    return send_from_directory(root_dir, 'index.html')

def _get_db():
    mysql = Mysql()
    return mysql