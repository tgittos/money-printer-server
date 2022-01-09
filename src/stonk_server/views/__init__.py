from core.stores.database import Database
from config import config
db = Database(config.stonks)

from .health import health_bp
from .swagger import swagger_bp
from .prices import prices_bp