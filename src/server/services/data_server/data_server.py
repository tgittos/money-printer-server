import os
import sys


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
    init_logger(os.path.dirname(__file__) + "../../../../logs/")

    # grab a ref to the logger
    logger = get_logger("server.services.data_server")

    # TODO - remove!
    if env_string != 'sandbox':
        logger.error("data server not starting - configured to not run in any env but sandbox")
        exit(0)

    # log all the previous stuff we set up
    logger.debug("setting env to {0}".format(env_string))
    logger.debug("changing pwd to {0}".format(pwd))
    logger.debug("augmented path with core")
    logger.debug("path: {0}".format(sys.path))

    # fetch the environment we need to be loading
    from server.services.api import load_config
    app_config = load_config()

    from server.config import config as server_config
    from server.services.data_server.sse_client import SSEClient
    from server.services.data_server.historical_client import HistoricalClient

    sse_client = SSEClient(env_string, server_config[env_string]['iexcloud']['secret'])
    logger.debug("sse upstream online")

    historical_client = HistoricalClient()
    logger.debug("historical upstream online")

    logger.info("running money-printer data server")
