from datetime import datetime
from sqlalchemy import desc

from core.apis.plaid.accounts import Accounts, AccountsConfig
from core.models.balance import Balance
from core.models.account import Account
from core.models.plaid_item import PlaidItem
from core.stores.mysql import MySql


def get_repository(mysql_config, plaid_config):
    repo = BalanceRepository(mysql_config=mysql_config, plaid_config=plaid_config)
    return repo


class CreateBalanceRequest:

    def __init__(self, account_id, available, current, iso_currency_code):
        self.account_id = account_id
        self.available = available
        self.current = current
        self.iso_currency_code = iso_currency_code


class BalanceRepository:

    def __init__(self, mysql_config, plaid_config):
        db = MySql(mysql_config)
        self.db = db.get_session()
        self.plaid_config = plaid_config

    def get_balances_by_account_id(self, account_id):
        r = self.db.query(Balance).filter(Balance.accountId == account_id).all()
        return r

    def get_latest_balance_by_account_id(self, account_id):
        r = self.db.query(Balance).filter(Balance.accountId == account_id).order_by(desc(Balance.timestamp)).first()
        return r

    def create_balance(self, request):
        balance = Balance()
        balance.account_id = request.account_id
        balance.available = request.available
        balance.current = request.current
        balance.iso_currency_code = request.iso_currency_code
        balance.timestamp = datetime.utcnow()

        self.db.add(balance)
        self.db.commit()

        return balance

    def sync_balance(self, account_id):
        account = self.db.query(Account).where(Account.id == account_id).first()

        if account is None:
            return

        plaid_item = self.db.query(PlaidItem).where(PlaidItem.id == account.plaid_item_id).first()

        if plaid_item is None:
            return

        api = Accounts(AccountsConfig(self.plaid_config))
        response_dict = api.get_account_balance(plaid_item.access_token, account.account_id)

        if "accounts" not in response_dict:
            print(" * unusual response from upstream: {0}".format(response_dict))
            return

        for account_dict in response_dict["accounts"]:
            balance_dict = account_dict['balances']

            new_balance = self.create_balance(CreateBalanceRequest(
                account_id=account.id,
                current=balance_dict['current'],
                available=balance_dict['available'],
                iso_currency_code=balance_dict['iso_currency_code']
            ))

