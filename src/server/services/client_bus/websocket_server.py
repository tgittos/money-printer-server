#import eventlet
#eventlet.monkey_patch()

import os
import sys

from flask import Flask
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


if __name__ == '__main__':
    # echo the environment we're passing in
    env_string = os.environ['MONEY_PRINTER_ENV']
    print(" * setting env to {0}".format(env_string))

    # sometimes we run with whacky paths, so lets set the python runtime
    # pwd to something sane
    pwd = os.path.abspath(os.path.dirname(__file__) + "/../../../")

    print(" * changing pwd to {0}".format(pwd))
    os.chdir(pwd)

    # also add the core dir to the path so we can include from it
    print(" * augmenting path with core")
    sys.path.append(pwd)
    print(" * path: {0}".format(sys.path))

    # todo - spin this out into a background thread
    # subscribe to redis?
    import redis

    def poc_handler(message):
        print('debug: got message: {0}'.format(message))
        emit('upstream-symbols', message)

    r = redis.Redis(host='localhost', port=6379, db=0)
    p = r.pubsub()
    p.subscribe(**{'upstream-symbols': poc_handler})
    print(" * subscribing to upstream-symbols pubsub in thread")
    thread = p.run_in_thread(sleep_time=0.1)


    # create the app
    from server.config import config as server_config
    from server.services.client_bus.handlers import augment_app

    app = create_app()
    socket_app = SocketIO(app, cors_allowed_origins='*', message_queue="redis://")

    print(" * augmenting money-printer websocket server with message handlers")
    augment_app(socket_app)

    print(" * running money-printer websocket server with config: {0}".format(server_config['server']))
    socket_app.run(app)
