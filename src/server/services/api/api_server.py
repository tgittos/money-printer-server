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

    # sometimes we run with whacky paths, so lets set the python runtime
    # pwd to something sane
    pwd = os.path.abspath(os.path.dirname(__file__) + "/../../../")

    # set the current dir to our project root
    os.chdir(pwd)

    # also add the core dir to the path so we can include from it
    sys.path.append(pwd)

    # configure the logger
    from core.lib.logger import init_logger, get_logger
    init_logger(os.path.dirname(__file__) + "/../../../logs/")

    # grab a ref to the logger
    logger = get_logger("server.services.api")

    # log all the previous stuff we set up
    logger.debug("setting env to {0}".format(env_string))
    logger.debug("changing pwd to {0}".format(pwd))
    logger.debug("augmented path with core")
    logger.debug("path: {0}".format(sys.path))

    # fetch the environment we need to be loading
    from server.services.api import load_config
    app_config = load_config()

    # now require stuff
    from server.config import config as server_config
    import routes

    logger.info("running money-printer api server")

    app = create_app()
    app.run(host=server_config['server']['host'],
            port=server_config['server']['port'])
