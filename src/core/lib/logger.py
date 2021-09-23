import logging
import os
from logging.handlers import RotatingFileHandler
import datetime
from os import path, utime


# 10MB log files
LOG_SIZE_BYTES = 10485760


def init_logger(base_path, level=logging.DEBUG):
    log_path = path.join(base_path, _log_file_name())
    log_path = os.path.abspath(log_path)
    if not path.exists(log_path):
        with open(log_path, 'w'):
            pass
    else:
        with open(log_path, 'a'):
            pass
    logging.basicConfig(level=level,
                        handlers=[RotatingFileHandler(log_path, maxBytes=LOG_SIZE_BYTES, backupCount=10)],
                        format='[%(levelname)s] (%(name)s) %(asctime)s %(message)s')


def get_logger(caller):
    return logging.getLogger(caller)


def _log_file_name():
    # log_file_name_template = "mp.{0}.log"
    # today = datetime.date.today().strftime("%Y-%m-%d")
    # return log_file_name_template.format(today)
    return "mp.log"
