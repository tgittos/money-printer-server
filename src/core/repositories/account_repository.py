from datetime import datetime
import redis
import json

from sqlalchemy import desc, and_

from core.apis.plaid.accounts import Accounts, AccountsConfig
from core.models.account import Account
from core.models.balance import Balance
from core.models.profile import Profile
from core.models.plaid_item import PlaidItem
from core.presentation.account_presenters import AccountWithBalance
from core.stores.mysql import MySql
from core.repositories.balance_repository import get_repository as get_balance_repository
from core.repositories.security_repository import get_repository as get_security_repository
from core.lib.logger import get_logger


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


def get_repository(mysql_config, plaid_config):
    repo = AccountRepository(
        mysql_config=mysql_config,
        plaid_config=plaid_config
    )
    return repo


WORKER_QUEUE = "mp:worker"


class AccountRepository:

    def __init__(self, mysql_config, plaid_config):
        self.logger = get_logger(__name__)
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        db = MySql(mysql_config)
        self.db = db.get_session()
        self.mysql_config = mysql_config
        self.plaid_config = plaid_config

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
        r.timestamp = datetime.utcnow()

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
                    records = self.db.query.filter(Balance.account_id == account.id and
                                                   request.start <= Balance.timestamp <= request.end).all()
                else:
                    records = self.db.query.filter(Balance.account_id == account.id and
                                                   request.start <= Balance.timestamp).all()
            else:
                records = self.db.query(Balance).filter(Balance.account_id == account.id).all()
        return records

    def sync_all_accounts(self, profile_id):
        profile = self.__fetch_profile(profile_id)
        if profile is None:
            return

        self.logger.info("updating account state for profile {0}".format(profile.id))

        balance_repo = get_balance_repository(mysql_config=self.mysql_config, plaid_config=self.plaid_config)
        security_repo = get_security_repository(mysql_config=self.mysql_config, plaid_config=self.plaid_config)
        plaid_accounts_api = Accounts(AccountsConfig(
            plaid_config=self.plaid_config
        ))

        plaid_links = self.__fetch_plaid_links(profile_id)
        for plaid_link in plaid_links:
            plaid_accounts_dict = plaid_accounts_api.get_accounts(plaid_link.access_token)

            self.logger.info("updating {0} accounts".format(len(plaid_accounts_dict['accounts'])))

            accounts = []
            for account_dict in plaid_accounts_dict['accounts']:
                if 'id' in account_dict:
                    self.logger.info("updating account details for account {0}".format(account_dict['id']))
                    account = self.__sync_update_account(profile, plaid_link, account_dict)
                    accounts.append(account)
                    self.logger.info("updating account balance for account {0}".format(account.id))
                    balance_repo.sync_balance(account.id)
                else:
                    self.logger.warning("upstream returned account response missing an id: {0}".format(account_dict))

            for account in accounts:
                # TODO - figure out enums or something
                if account.type == "investment":
                    self.logger.info("updating investment holdings for account {0}".format(account.id))
                    security_repo.sync_holdings(profile_id=profile_id, account_id=account.id)

        self.logger.info("done updating accounts for profile {0}".format(profile.id))

    def __augment_with_balances(self, account_records):
        augmented_records = []
        for account_record in account_records:
            balance = self.db.query(Balance).filter(Balance.account_id == account_record.id)\
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

    def __fetch_profile(self, profile_id):
        record = self.db.query(Profile).where(Profile.id == profile_id).first()
        return record

    def __fetch_plaid_links(self, profile_id):
        records = self.db.query(PlaidItem).where(PlaidItem.profile_id == profile_id).all()
        return records

    def __sync_update_account(self, profile, plaid_link, account_dict):
        # update the account
        account = self.get_account_by_account_id(profile_id=profile.id, account_id=account_dict['account_id'])
        if account is None:
            account = self.create_account(CreateAccountRequest(
                account_id=account_dict['account_id'],
                name=account_dict['name'],
                official_name=account_dict['official_name'],
                type=account_dict['type'],
                subtype=account_dict['subtype'],
                plaid_item_id=plaid_link.id,
                profile_id=profile.id
            ))
        else:
            account.name = account_dict['name']
            account.official_name = account_dict['official_name']
            account.type = account_dict['type'],
            account.subtype = account_dict['subtype']
            self.update_account(account)

        return account
