import os
import sys
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    # global static configs
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.url_map.strict_slashes = False
    CORS(app)

    # load routes
    print(" * loading routes")
    routes.init_app(app)

    return app


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

    # fetch the environment we need to be loading
    from server import load_config
    app_config = load_config()

    # now require stuff
    from server.config import config as server_config
    import routes

    print(" * running money-printer api server with config: {0}".format(server_config['server']))
    app = create_app()
    app.run(host=server_config['server']['host'],
            port=server_config['server']['port'])
