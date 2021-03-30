import schedule
import time
import threading

import jobs.quandl_eod as q_eod

def init:
    schedule.every().day.do(q_eod.run, "HD")

def run:
    while True:
        schedule.run_pending()
        time.sleep(1000)

def start:
    init
    thread = threading.Thread(target=run, args=(1,))
    thread.start()
