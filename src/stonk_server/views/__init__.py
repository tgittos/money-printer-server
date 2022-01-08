from core.stores.database import Database
from config import config
db = Database(config.stonks)

from .prices import prices_bp