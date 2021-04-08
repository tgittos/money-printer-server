import sys
sys.path.append('./../../src')

import schedule
import time
import threading

from lib.stores.mysql import Mysql

def init():
    schedule.every().day.do(update_data, "HD")

def run():
    while True:
        schedule.run_pending()
        time.sleep(1000)

def update_data():
    print("[scheduler] updating tracked symbols")
    db = Mysql()
    data = db.get_sync()
    for sync in data:
        print("[scheduler] fetching data for {0}".format(sync.symbol))
        db.update_candles(sync.symbol, 60)

def update_data_async():
    thread = threading.Thread(target=update_data)
    thread.start()

def start():
    print("[scheduler] initializing")
    init
    print("[scheduler] spinning off thread")
    thread = threading.Thread(target=run)
    thread.start()
