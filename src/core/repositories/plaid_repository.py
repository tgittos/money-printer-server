from core.stores.mysql import MySql
from core.lib.logger import get_logger
from config import mysql_config, plaid_config

# import all the actions so that consumers of the repo can access everything
from core.lib.utilities import wrap
from core.lib.actions.plaid.crud import *
from core.lib.actions.plaid.requests import *


class PlaidRepository:

    logger = get_logger(__name__)
    db = MySql(mysql_config)

    def __init__(self):
        self._init_facets()

    def _init_facets(self):
        self.get_plaid_item_by_id = wrap(get_plaid_item_by_id, self)
        self.get_plaid_item_by_plaid_item_id = wrap(get_plaid_item_by_plaid_item_id, self)
        self.get_plaid_items_by_profile = wrap(get_plaid_items_by_profile, self)
        self.create_plaid_item = wrap(create_plaid_item, self)
        self.update_plaid_item = wrap(update_plaid_item, self)
