
from core.models.account import Account
from core.models.plaid_item import PlaidItem
from core.repositories.security_repository import get_repository as get_security_repo
from core.repositories.stock_repository import get_repository as get_stock_repository
from core.repositories.scheduled_job_repository import get_repository as get_scheduled_job_repository, CreateInstantJobRequest
from core.lib.logger import get_logger

from core.stores.mysql import MySql


def get_repository(mysql_config, iex_config, plaid_config, mailgun_config):
    repo = HoldingRepository(HoldingRepositoryConfig(
        mysql_config=mysql_config,
        iex_config=iex_config,
        plaid_config=plaid_config,
        mailgun_config=mailgun_config
    ))
    return repo


class HoldingRepositoryConfig:
    def __init__(self, mysql_config, iex_config, plaid_config, mailgun_config):
        self.mysql_config = mysql_config
        self.iex_config = iex_config
        self.plaid_config = plaid_config
        self.mailgun_config = mailgun_config


class HoldingRepository:

    def __init__(self, config):
        self.logger = get_logger(__name__)
        self.mysql_config = config.mysql_config
        self.iex_config = config.iex_config
        self.plaid_config = config.plaid_config
        self.mailgun_config = config.mailgun_config

        db = MySql(self.mysql_config)
        self.db = db.get_session()
        self.security_repo = get_security_repo(mysql_config=self.mysql_config, plaid_config=self.plaid_config)
        self.stock_repo = get_stock_repository(iex_config=self.iex_config, mysql_config=self.mysql_config)

    def schedule_update_holdings(self, plaid_item_id):
        if plaid_item_id is None:
            self.logger.error("cannot schedule account holding sync without plaid item")
            return
        scheduled_job_repo = get_scheduled_job_repository(mailgun_config=self.mailgun_config, mysql_config=self.mysql_config)
        scheduled_job_repo.create_instant_job(CreateInstantJobRequest(
            job_name='sync_holdings',
            args={
                'plaid_item_id': plaid_item_id
            }
        ))

    def update_holdings(self, plaid_item_item_id):
        if plaid_item_item_id is None:
            self.logger.error("cannot update holding without a valid plaid_item_item_id")
            return
        plaid_item = self.db.query(PlaidItem).where(PlaidItem.item_id == plaid_item_item_id).first()
        if plaid_item is None:
            self.logger.warning("requested update holding with plaid item item_id {0}, no plaid item found"
                                .format(plaid_item_item_id))
        accounts = self.db.query(Account).filter(Account.plaid_item_id == plaid_item.id).all()
        if accounts is None or len(accounts) == 0:
            self.logger.error("received request to update holdings with no corresponding accounts: {0}"
                              .format(plaid_item.id))
            return
        accounts_updated = 0
        for account in accounts:
            self.logger.info("updating holdings for account: {0}".format(account.id))
            self.security_repo.sync_holdings(account_id=account.id, profile_id=account.profile_id)
            accounts_updated += 1
        self.logger.info("updated holdings for {0} accounts".format(accounts_updated))

    def schedule_update_transactions(self, plaid_item_id):
        if plaid_item_id is None:
            self.logger.error("cannot schedule investment transaction sync without plaid item")
            return
        scheduled_job_repo = get_scheduled_job_repository(mailgun_config=self.mailgun_config, mysql_config=self.mysql_config)
        scheduled_job_repo.create_instant_job(CreateInstantJobRequest(
            job_name='sync_transactions',
            args={
                'plaid_item_id': plaid_item_id
            }
        ))

    def update_transactions(self, plaid_item_id):
        if plaid_item_id is None:
            self.logger.error("cannot update investment transactions without a valid plaid_item_id")
            return
        accounts = self.db.query(Account).filter(Account.plaid_item_id == plaid_item_id).all()
        if accounts is None or len(accounts) == 0:
            self.logger.error("received request to update investment transactions with no corresponding accounts: {0}"
                              .format(plaid_item_id))
            return
        accounts_updated = 0
        for account in accounts:
            self.logger.info("updating investment transactions for account: {0}".format(account.id))
            self.security_repo.sync_transactions(account_id=account.id, profile_id=account.profile_id)
            accounts_updated += 1
        self.logger.info("updated investment transactions for {0} accounts".format(accounts_updated))

        raise Exception("not implemented yet")

    def calculate_performance(self, holding_id):
        # pull the holding
        # pull security_prices for holding
        # using cost basis of holding, at each security_price data point, calculate a rate of return
        raise Exception("Not implemented")

    def calculate_forecast(self, holding_id):
        raise Exception("Not implemented")

