from datetime import datetime

from core.stores.mysql import MySql
from core.models.plaid_item import PlaidItem


def get_repository():
    from server.services.api import load_config
    app_config = load_config()
    repo = PlaidRepository(sql_config=app_config['db'])
    return repo


class CreatePlaidItem:
    profile_id = None
    item_id = None
    access_token = None
    request_id = None

    def __init__(self, profile_id, item_id, access_token, request_id):
        self.profile_id = profile_id
        self.item_id = item_id
        self.access_token = access_token
        self.request_id = request_id


class GetPlaidItem:
    item_id = None

    def __init__(self, item_id):
        self.item_id = item_id


class PlaidRepository:

    def __init__(self, sql_config):
        db = MySql(sql_config)
        self.db = db.get_session()

    def create_plaid_item(self, params):
        r = PlaidItem()
        r.profile_id = params.profile_id
        r.item_id = params.item_id
        r.access_token = params.access_token
        r.request_id = params.request_id
        r.timestamp = datetime.now()

        self.db.add(r)
        self.db.commit()

        return r

    def get_plaid_item(self, params):
        r = self.db.query(PlaidItem).filter(PlaidItem.item_id==params.item_id).single()
        return r
