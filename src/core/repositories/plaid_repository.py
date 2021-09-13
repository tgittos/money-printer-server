from datetime import datetime

from core.apis.plaid.accounts import Accounts, AccountsConfig
from core.stores.mysql import MySql
from core.models.plaid_item import PlaidItem


def get_repository(sql_config, plaid_api_config):
    repo = PlaidRepository(sql_config=sql_config, plaid_api_config=plaid_api_config)
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
    id = None

    def __init__(self, id):
        self.id = id


class PlaidRepository:

    def __init__(self, sql_config, plaid_api_config):
        self.plaid_api_config = plaid_api_config
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

    def sync_accounts(self, plaid_item_id):
        plaid_accounts_api = Accounts(AccountsConfig(
            plaid_config=self.plaid_api_config
        ))
        plaid_link = self.get_plaid_item(GetPlaidItem(id=plaid_item_id))
        print(" * fetching auths from Plaid using access token: {0}".format(plaid_link.access_token))
        plaid_auths = plaid_accounts_api.get_accounts(plaid_link.access_token)

    def get_plaid_item(self, params):
        r = self.db.query(PlaidItem).filter(PlaidItem.id==params.id).first()
        return r
