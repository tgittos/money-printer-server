import os
from core.lib.logger import init_logger, get_logger

if 'MP_ENVIRONMENT' in os.environ:
    os.environ['FLASK_ENV'] = os.environ['MP_ENVIRONMENT']

log_path = os.path.dirname(__file__) + "/../../logs/"
init_logger(log_path)
logger = get_logger("server.services.stonk_server")
