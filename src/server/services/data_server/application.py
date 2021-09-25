import time
import os
import signal
import sys

from core.lib.logger import init_logger, get_logger
from config import config, env

from .lib.sse_client import SSEClient
from .lib.historical_client import HistoricalClient


class DataServerApplication:

    log_path = os.path.dirname(__file__) + "/../../../logs/"

    def __init__(self):
        init_logger(self.log_path)
        self.logger = get_logger("server.services.data_server")
        self.sse_client = SSEClient(env, config.iex.secret)
        self.historical_client = HistoricalClient()
        # self._configure_signals()

    def run(self):
        print(" * Starting money-printer data server", flush=True)
        self.logger.info("starting sse client")
        self.sse_client.start()
        self.logger.info("starting historical client")
        self.historical_client.start()
        # block until a stop is requested, sigint handler should handle the
        # all thread shutdowns
        while True:
            time.sleep(1)

    def _configure_signals(self):
        self.logger.debug("intercepting sigints for graceful shutdown")
        signal.signal(signal.SIGINT, self._curry_sigint_handler({
            "sse_client": self.sse_client,
            "historical_client": self.historical_client
        }))

    def _curry_sigint_handler(self, context):
        sse_client = context["sse_client"]
        historical_client = context["historical_client"]

        def sigint_handler(signal, frame):
            print("requested data-server shutdown", flush=True)
            if sse_client:
                print("shutting down sse client", flush=True)
                sse_client.stop()
            if historical_client:
                print("shutting down historical client", flush=True)
                historical_client.stop()
            sys.exit(0)

        return sigint_handler
