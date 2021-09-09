import os
import sys


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

    from server.config import config as server_config
    from server.services.data_server.sse_client import SSEClient
    from server.services.data_server.historical_client import HistoricalClient

    sse_client = SSEClient(env_string, server_config[env_string]['iexcloud']['secret'])
    print(" * sse upstream online")

    historical_client = HistoricalClient()
    print(" * historical upstream online")

    print(" * data-server listening for commands")
