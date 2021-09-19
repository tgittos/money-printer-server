import logging
import datetime
from os import path


def init_logger(base_path, level=logging.DEBUG):
    log_path = path.join(base_path, _log_file_name())
    logging.basicConfig(filename=log_path, level=level,
                        format='[%(levelname)s] (%(name)s) %(asctime)s %(message)s')


def get_logger(caller):
    return logging.getLogger(caller)


def _log_file_name():
    log_file_name_template = "mp.{0}.log"
    today = datetime.date.today().strftime("%Y-%m-%d")
    return log_file_name_template.format(today)
