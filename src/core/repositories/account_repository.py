from datetime import datetime
import redis
import json

from sqlalchemy import desc, and_

from core.stores.mysql import MySql
from core.models.account import Account
from core.models.balance import Balance
from core.presentation.account_presenters import AccountWithBalance


class CreateAccountRequest:

    def __init__(self, plaid_item_id, profile_id, account_id, name, official_name, type, subtype):
        self.profile_id = profile_id
        self.plaid_item_id = plaid_item_id
        self.account_id = account_id
        self.name = name
        self.official_name = official_name
        self.type = type
        self.subtype = subtype


class GetAccountBalanceRequest:

    def __init__(self, profile_id, account_id, start=None, end=None):
        self.profile_id = profile_id
        self.account_id = account_id
        self.start = start
        self.end = end


def get_repository():
    from server.services.api import load_config
    app_config = load_config()
    repo = AccountRepository(
        mysql_config=app_config['db']
    )
    return repo


WORKER_QUEUE = "mp:worker"


class AccountRepository:

    def __init__(self, mysql_config):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        db = MySql(mysql_config)
        self.db = db.get_session()

    def get_all_accounts_by_profile(self, profile_id):
        account_records = self.db.query(Account).filter(Account.profile_id == profile_id).all()
        return self.__augment_with_balances(account_records)

    def get_account_by_id(self, profile_id, account_id):
        r = self.db.query(Account).where(and_(Account.profile_id == profile_id, Account.id == account_id)).first()
        return r

    def get_account_by_account_id(self, profile_id, account_id):
        r = self.db.query(Account).where(and_(Account.profile_id == profile_id, Account.account_id == account_id)).first()
        return r

    def create_account(self, params):
        r = Account()
        r.profile_id = params.profile_id
        r.plaid_item_id = params.plaid_item_id
        r.account_id = params.account_id
        r.name = params.name
        r.official_name = params.official_name
        r.type = params.type
        r.subtype = params.subtype
        r.timestamp = datetime.now()

        self.db.add(r)
        self.db.commit()

        return r

    def update_account(self, account):
        self.db.commit()

        return account

    def schedule_account_sync(self, profile_id, plaid_item_id):
        self.redis.publish(WORKER_QUEUE, json.dumps({
            'job': 'sync_accounts',
            'profile_id': profile_id,
            'plaid_item_id': plaid_item_id
        }))

    def get_account_balances(self, request):
        account = self.get_account_by_id(request.profile_id, request.account_id)
        records = []
        if account is not None:
            if request.start is not None:
                if request.end is not None:
                    records = self.db.query.filter(Balance.accountId == account.id and
                                                   request.start <= Balance.timestamp <= request.end).all()
                else:
                    records = self.db.query.filter(Balance.accountId == account.id and
                                                   request.start <= Balance.timestamp).all()
            else:
                records = self.db.query(Balance).filter(Balance.accountId == account.id).all()
        return records

    def __augment_with_balances(self, account_records):
        augmented_records = []
        for account_record in account_records:
            balance = self.db.query(Balance).filter(Balance.accountId == account_record.id)\
                .order_by(desc(Balance.timestamp)).first()
            account_record.timestamp = balance.timestamp
            augmented_record = AccountWithBalance(
                account=account_record,
                balance=balance.current
            )
            augmented_records.append(augmented_record)
            # undo the update to the account_record timestamp
            self.db.rollback()

        return augmented_records

