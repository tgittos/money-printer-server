from datetime import datetime
from sqlalchemy import desc

from core.models.balance import Balance
from core.stores.mysql import MySql


def get_repository(mysql_config):
    repo = BalanceRepository(mysql_config=mysql_config)
    return repo


class CreateBalanceRequest:

    def __init__(self, account_id, available, current, iso_currency_code):
        self.account_id = account_id
        self.available = available
        self.current = current
        self.iso_currency_code = iso_currency_code


class BalanceRepository:

    def __init__(self, mysql_config):
        db = MySql(mysql_config)
        self.db = db.get_session()

    def get_balances_by_account_id(self, account_id):
        r = self.db.query(Balance).filter(Balance.accountId == account_id).all()
        return r

    def get_latest_balance_by_account_id(self, account_id):
        r = self.db.query(Balance).filter(Balance.accountId == account_id).order_by(desc(Balance.timestamp)).first()
        return r

    def create_balance(self, request):
        balance = Balance()
        balance.accountId = request.account_id
        balance.available = request.available
        balance.current = request.current
        balance.iso_currency_code = request.iso_currency_code
        balance.timestamp = datetime.now()

        self.db.add(balance)
        self.db.commit()

        return balance
