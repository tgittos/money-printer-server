import os
import threading

import redis

from core.lib.logger import get_logger


env_string = os.environ['MONEY_PRINTER_ENV']


class SSEControlThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(SSEControlThread, self).__init__(*args, **kwargs)
        self.logger = get_logger(__name__)
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.redis.pubsub()

    def on(self, channel, handler):
        self.logger.debug("subscribing to {0} redis pubsub".format(channel))
        self.pubsub.subscribe(**{channel: handler})

    def publish(self, channel, message):
        self.logger.debug("publishing {0} to channel {1}".format(message, channel))
        self.redis.publish(channel, message)
