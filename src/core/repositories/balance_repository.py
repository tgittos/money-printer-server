from datetime import datetime
from sqlalchemy import desc

from core.apis.plaid.accounts import Accounts, AccountsConfig
from core.models.account_balance import AccountBalance
from core.models.account import Account
from core.models.plaid_item import PlaidItem
from core.repositories.scheduled_job_repository import get_repository as get_scheduled_job_repository, CreateInstantJobRequest
from core.stores.mysql import MySql
from core.lib.logger import get_logger


def get_repository(mysql_config, plaid_config, mailgun_config):
    repo = BalanceRepository(mysql_config=mysql_config, plaid_config=plaid_config, mailgun_config=mailgun_config)
    return repo


class CreateAccountBalanceRequest:

    def __init__(self, account_id, available, current, iso_currency_code):
        self.account_id = account_id
        self.available = available
        self.current = current
        self.iso_currency_code = iso_currency_code


class BalanceRepository:

    def __init__(self, mysql_config, plaid_config, mailgun_config):
        self.logger = get_logger(__name__)
        db = MySql(mysql_config)
        self.db = db.get_session()
        self.plaid_config = plaid_config
        self.mailgun_config = mailgun_config

    def get_balances_by_account_id(self, account_id):
        r = self.db.query(AccountBalance).filter(AccountBalance.accountId == account_id).all()
        return r

    def get_latest_balance_by_account_id(self, account_id):
        r = self.db.query(AccountBalance).filter(AccountBalance.accountId == account_id).order_by(desc(AccountBalance.timestamp)).first()
        return r

    def create_balance(self, request):
        balance = AccountBalance()
        balance.account_id = request.account_id
        balance.available = request.available
        balance.current = request.current
        balance.iso_currency_code = request.iso_currency_code
        balance.timestamp = datetime.utcnow()

        self.db.add(balance)
        self.db.commit()

        return balance

    def schedule_update_all_balances(self, plaid_item_id):
        scheduled_job_repo = get_scheduled_job_repository(mailgun_config=self.mailgun_config, mysql_config=self.mysql_config)
        scheduled_job_repo.create_instant_job(CreateInstantJobRequest(
            job_name='sync_balances',
            args={
                'plaid_item_id': plaid_item_id
            }
        ))

    def sync_all_balances(self, plaid_item_id):
        self.logger.info("syncing account balance/s for plaid item: {0}".format(plaid_item_id))
        accounts = self.db.query(Account).where(Account.plaid_item_id == plaid_item_id).all()
        if accounts and len(accounts) > 0:
            self.logger.info("found {0} accounts to update".format(len(accounts)))
            for account in accounts:
                self.sync_account_balance(account.id)
            self.logger.info("done updating balances for plaid item")

    def sync_account_balance(self, account_id):
        self.logger.info("syncing account balance for account id: {0}".format(account_id))

        account = self.db.query(Account).where(Account.id == account_id).first()

        if account is None:
            return

        plaid_item = self.db.query(PlaidItem).where(PlaidItem.id == account.plaid_item_id).first()

        if plaid_item is None:
            return

        api = Accounts(AccountsConfig(self.plaid_config))
        response_dict = api.get_account_balance(plaid_item.access_token, account.account_id)

        if response_dict is None or 'accounts' not in response_dict:
            self.logger.error("unusual response from upstream: {0}".format(response_dict))
            return

        balances = []

        for account_dict in response_dict['accounts']:
            balance_dict = account_dict['balances']

            new_balance = self.create_balance(CreateAccountBalanceRequest(
                account_id=account.id,
                current=balance_dict['current'],
                available=balance_dict['available'],
                iso_currency_code=balance_dict['iso_currency_code']
            ))

            balances.append(new_balance)

        return balances
