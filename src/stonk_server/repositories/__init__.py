from core.stores.database import Database
from config import config
db = Database(config.stonks)

from .stock_repository import StockRepository