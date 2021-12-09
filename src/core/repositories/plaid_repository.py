from core.lib.logger import get_logger

# import all the actions so that consumers of the repo can access everything
from core.lib.utilities import wrap
from core.lib.actions.plaid.crud import *
from core.lib.actions.plaid.requests import *


class PlaidRepository:

    logger = get_logger(__name__)

    def __init__(self, store):
        self.store = store
        self._init_facets()

    def _init_facets(self):
        self.get_plaid_item_by_id = wrap(get_plaid_item_by_id, self.store)
        self.get_plaid_item_by_plaid_item_id = wrap(get_plaid_item_by_plaid_item_id, self.store)
        self.get_plaid_items_by_profile = wrap(get_plaid_items_by_profile, self.store)
        self.create_plaid_item = wrap(create_plaid_item, self.store)
        self.update_plaid_item = wrap(update_plaid_item, self.store)
