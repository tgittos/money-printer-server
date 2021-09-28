from core.stores.mysql import MySql
from core.lib.logger import get_logger
from config import mysql_config, plaid_config

# import all the facets so that consumers of the repo can access everything
from .facets.plaid.crud import *
from .facets.plaid.requests import *


class PlaidRepository:

    logger = get_logger(__name__)

    def __init__(self):
        self.plaid_api_config = plaid_config
        self.mysql_config = mysql_config
        db = MySql(mysql_config)
        self.db = db.get_session()

        self._init_facets()

    def _init_facets(self):
        self.get_plaid_item_by_id = get_plaid_item_by_id
        self.get_plaid_item_by_plaid_item_id = get_plaid_item_by_plaid_item_id
        self.get_plaid_items_by_profile = get_plaid_items_by_profile
        self.create_plaid_item = create_plaid_item
        self.update_plaid_item = update_plaid_item
