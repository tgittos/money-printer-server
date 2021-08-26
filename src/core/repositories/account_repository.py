from datetime import datetime

from core.stores import mysql
from core.models import account

class CreateAccountRequest:
    plaid_item_id = None
    account_id = None
    name = None
    official_name = None
    subtype = None

class AccountRepository:

    def __init__(self):
        db = mysql()
        self.db = db.get_session()

    def create_account(self, params):
        r = account()
        r.plaid_item_id = params.plaid_item_id
        r.account_id = params.account_id
        r.name = params.name
        r.official_name = params.official_name
        r.subtype = params.subtype
        r.timestamp = datetime.now()

        self.db.add(r)
        self.db.commit()
