from core.lib.logger import get_logger
from core.stores.mysql import MySql

# import all the actions so that consumers of the repo can access everything
from core.lib.utilities import wrap
from core.actions.plaid.crud import *
from config import mysql_config


class PlaidRepository:

    db = MySql(mysql_config)
    logger = get_logger(__name__)

    def __init__(self):
        self._init_facets()

    def _init_facets(self):
        self.get_plaid_item_by_id = wrap(get_plaid_item_by_id, self.db)
        self.get_plaid_item_by_plaid_item_id = wrap(
            get_plaid_item_by_plaid_item_id, self.db)
        self.create_plaid_item = wrap(create_plaid_item, self.db)
        self.update_plaid_item = wrap(update_plaid_item, self.db)
