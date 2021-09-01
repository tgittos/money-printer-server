import os, sys
from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit


app = None
socket_app = None

def create_app():
    from server.config import config as server_config

    temp_app = Flask(__name__)

    # configure cores
    temp_app.config['CORS_HEADERS'] = 'Content-Type'
    temp_app.config['DEBUG'] = False
    CORS(temp_app)

    # global static configs
    temp_app.config['SECRET_KEY'] = server_config['server']['secret']

    return temp_app


def augment_app():

    @app.route('/')
    def index():
        return 'please upgrade to ws connection'

    @socket_app.on('connect')
    def connect():
        print("ws client connected")

    # default handler
    @socket_app.on('json')
    def handle_json_message(data):
        print("received message: {0}".format(data))

    @socket_app.on('subscribe_symbols')
    def subscribe_symbols(data):
        print("received subscribe_symbols message: {0}".format(data))


if __name__ == '__main__':
    # echo the environment we're passing in
    env_string = os.environ['MONEY_PRINTER_ENV']
    print(" * setting env to {0}".format(env_string))

    # sometimes we run with whacky paths, so lets set the python runtime
    # pwd to something sane
    pwd = os.path.abspath(os.path.dirname(__file__) + "/../")

    print(" * changing pwd to {0}".format(pwd))
    os.chdir(pwd)

    # also add the core dir to the path so we can include from it
    print(" * augmenting path with core")
    sys.path.append(pwd)
    print(" * path: {0}".format(sys.path))

    # create the app
    from server.config import config as server_config
    app = create_app()

    socket_app = SocketIO(app, cors_allowed_origins='*')

    print(" * augmenting money-printer websocket server with message handlers")
    augment_app()

    print(" * running money-printer websocket server with config: {0}".format(server_config['server']))
    socket_app.run(app)
