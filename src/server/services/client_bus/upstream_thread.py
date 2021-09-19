import os
import threading
import requests
import sseclient

from core.lib.logger import get_logger

from server.config import config as server_config

env_string = os.environ['MONEY_PRINTER_ENV']


class UpstreamThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(UpstreamThread, self).__init__(*args, **kwargs)
        self.logger = get_logger(__name__)
        self.secret_token = server_config[env_string]['iexcloud']['secret']
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.publisher = None

    def set_publisher(self, publisher):
        self.publisher = publisher

    def start(self, tracked_symbols):
        super(UpstreamThread, self).start()
        self.logger.debug("upstream thread starting")
        self.stop_event.clear()
        self.pause_event.clear()
        while not self.stop_event.is_set():
            while not self.pause_event.is_set():
                if len(tracked_symbols) > 0:
                    url = self.__gen_api_url(self.tracked_symbols)
                    self.logger.info("starting SSE stream to url: {0}".format(url))
                    stream_response = requests.get(url, stream=True, headers=self.headers, params=self.params)
                    client = sseclient.SSEClient(stream_response)
                    for event in client.events():
                        if self.pause_event.is_set() or self.stop_event.is_set():
                            break
                        event_data = event.data
                        # self.logger.debug(" * publishing event to upstream-symbols pubsub: {0}".format(event_data))
                        if self.publisher is not None:
                            self.publisher.publish(event_data)
                else:
                    self.logger.info("not tracking any symbols, going to sleep")
                    self.pause_event.set()

    def pause(self):
        self.pause_event.set()

    def is_paused(self):
        return self.pause_event.is_set()

    def __gen_api_url(self, symbols):
        if env_string == 'sandbox':
            url = "https://sandbox-sse.iexapis.com/stable/stocksUS1Second?symbols={0}&token={1}" \
                .format(','.join(symbols), self.secret_token)
        else:
            url = "https://cloud-sse.iexapis.com/stable/stocksUS1Second?symbols={0}&token={1}" \
                .format(','.join(symbols), self.secret_token)
        return url
