import os
from core.lib.logger import init_logger, get_logger

log_path = os.path.dirname(__file__) + "/../../logs/"
init_logger(log_path)
logger = get_logger("server.services.api")
