from datetime import datetime

from core.stores.mysql import MySql
from core.models.account import Account


class CreateAccountRequest:
    plaid_item_id = None
    account_id = None
    name = None
    official_name = None
    subtype = None


def get_repository():
    from server.services.api import load_config
    app_config = load_config()
    repo = AccountRepository(
        mysql_config=app_config['db']
    )
    return repo


class AccountRepository:

    def __init__(self, mysql_config):
        db = MySql(mysql_config)
        self.db = db.get_session()

    def get_all_accounts_by_profile(self, profile_id):
        r = self.db.query(Account).filter(Account.profile_id).all()
        return r

    def create_account(self, params):
        r = Account()
        r.plaid_item_id = params.plaid_item_id
        r.account_id = params.account_id
        r.name = params.name
        r.official_name = params.official_name
        r.subtype = params.subtype
        r.timestamp = datetime.now()

        self.db.add(r)
        self.db.commit()

    def get_account_by_id(self, id):
        r = self.db.query(Account).filter(Account.id == id).single()
        return r
