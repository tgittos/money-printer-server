import json
import redis

from config import config
from core.lib.logger import get_logger


class ClientBus:

    running = False
    redis = None
    pubsub = None
    subscribers = {}

    def __init__(self):
        self.logger = get_logger(__name__)
        self.thread = None

    def start(self):
        self.logger.info("subscribing to upstream-symbols pubsub in thread")
        try:
            self.redis = redis.Redis(host=config.redis.host, port=config.redis.port, db=0)
            self.pubsub = self.redis.pubsub()
            self.thread = self.pubsub.run_in_thread(sleep_time=0.1)
            self.running = True
        except Exception as err:
            print(" error starting client bus: {0}".format(err))

    def stop(self):
        if self.thread and self.running:
            for e in self.subscribers.keys():
                for sub in [] + self.subscribers[e]:
                    self.unsubscribe(e, sub)
            self.running = False
            self.thread.join()

    def subscribe(self, event, fn):
        if event not in self.subscribers:
            self.subscribers[event] = []
        self.logger.info(f"subscribing to {event} pubsub in thread")
        self.subscribers[event].push(fn)
        if self.pubsub:
            self.pubsub.subscribe(**{event: fn})

    def unsubscribe(self, event, fn):
        if event in self.subscribers:
            self.subscribers[event] = filter(lambda h: h != fn, self.subscribers[event])
        self.logger.info(f"unsubscribing to {event} pubsub in thread")
        if self.pubsub:
            self.pubsub.unsubscribe(**{event: fn})

    def publish(self, event, data):
        if self.redis is not None:
            self.logger.info(f"publishing data to {event} pubsub in thread")
            self.redis.publish(event, json.dumps(data))