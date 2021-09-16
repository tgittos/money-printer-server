from datetime import datetime

from sqlalchemy import and_

from core.stores.mysql import MySql
from core.apis.plaid.investments import Investments, InvestmentsConfig, InvestmentsHoldingsGetRequest
from core.models.plaid_item import PlaidItem
from core.models.account import Account
from core.models.security import Security
from core.models.holding import Holding
from core.presentation.holding_presenters import HoldingWithSecurity


def get_repository(mysql_config, plaid_config):
    repo = SecurityRepository(mysql_config=mysql_config, plaid_config=plaid_config)
    return repo


class CreateSecurityRequest:
    def __init__(self, profile_id, account_id, name, ticker_symbol, iso_currency_code, institution_id,
                 institution_security_id, security_id, proxy_security_id, cusip, isin, sedol):
        self.profile_id = profile_id
        self.account_id = account_id
        self.name = name
        self.ticker_symbol = ticker_symbol
        self.iso_currency_code = iso_currency_code
        self.institution_id = institution_id
        self.institution_security_id = institution_security_id
        self.security_id = security_id
        self.proxy_security_id = proxy_security_id
        self.cusip = cusip
        self.isin = isin
        self.sedol = sedol


class CreateHoldingRequest:
    def __init__(self, account_id, security_id, cost_basis, quantity, iso_currency_code):
        self.account_id = account_id
        self.security_id = security_id
        self.cost_basis = cost_basis
        self.quantity = quantity
        self.iso_currency_code = iso_currency_code


class SecurityRepository:

    def __init__(self, mysql_config, plaid_config):
        mysql = MySql(mysql_config)
        self.db = mysql.get_session()
        self.plaid_config = plaid_config

    def get_securities(self):
        records = self.db.query(Security).distinct(Security.ticker_symbol).all()
        return records

    def get_security_by_symbol(self, symbol):
        record = self.db.query(Security).where(Security.ticker_symbol == symbol).first()
        return record

    def get_securities_by_account_id(self, account_id):
        records = self.db.query(Security).where(Security.account_id == account_id).all()
        return records

    def get_security_by_security_id(self, plaid_security_id):
        record = self.db.query(Security).where(Security.security_id == plaid_security_id).first()
        return record

    def get_holdings_by_profile_and_account(self, profile_id, account_id):
        account = self.db.query(Account).where(and_(
            Account.profile_id == profile_id,
            Account.id == account_id,
        )).first()
        holdings = self.db.query(Holding).where(Holding.account_id == account.id).all()
        security_ids = list([h.security_id for h in holdings])
        securities = self.db.query(Security).filter(Security.id.in_(security_ids)).all()
        presentations = []
        for holding in holdings:
            security = list(filter(lambda s: s.id == holding.security_id, securities))[0]
            presentations.append(HoldingWithSecurity(holding, security))
        return presentations

    def get_holding_by_account_and_security(self, plaid_account_id, plaid_security_id):
        account = self.db.query(Account).where(Account.account_id == plaid_account_id).first()
        security = self.get_security_by_security_id(plaid_security_id)
        record = self.db.query(Holding).where(and_(
            Holding.account_id == account.id,
            Holding.security_id == security.id
        )).first()
        return record

    def create_security(self, request):
        security = Security()

        security.profile_id = request.profile_id
        security.account_id = request.account_id
        security.name = request.name
        security.ticker_symbol = request.ticker_symbol
        security.iso_currency_code = request.iso_currency_code
        security.institution_security_id = request.institution_security_id
        security.security_id = request.security_id
        security.proxy_security_id = request.proxy_security_id
        security.cusip = request.cusip
        security.isin = request.isin
        security.sedol = request.sedol
        security.timestamp = datetime.utcnow()

        self.db.add(security)
        self.db.commit()

        return security

    def create_holding(self, request):
        holding = Holding()

        holding.account_id = request.account_id
        holding.security_id = request.security_id
        holding.cost_basis = request.cost_basis
        holding.quantity = request.quantity
        holding.iso_currency_code = request.iso_currency_code
        holding.timestamp = datetime.utcnow()

        self.db.add(holding)
        self.db.commit()

        return holding

    def sync_holdings(self, profile_id, account_id):
        account = self.db.query(Account).where(Account.id == account_id).first()
        if account is None:
            print(" * requested holdings sync on account that couldn't be found: {0}".format(account_id), flush=True)
            return

        plaid_item = self.db.query(PlaidItem).where(PlaidItem.id == account.plaid_item_id).first()
        if plaid_item is None:
            print(" * requested holdings sync on account but couldn't find plaid_item: {0}".format(account.to_dict()))
            return

        api = Investments(InvestmentsConfig(self.plaid_config))
        investment_dict = api.get_investments(plaid_item.access_token)

        # update securities from this account
        # these might not be account specific, but institution specific
        # so there's a chance I can detach it from the profile/account and just
        # link it in from the holdings
        for security_dict in investment_dict["securities"]:
            security = self.get_security_by_security_id(security_dict['security_id'])
            if security is None:
                security = self.create_security(CreateSecurityRequest(
                    profile_id=profile_id,
                    account_id=account.id,
                    name=security_dict['name'],
                    ticker_symbol=security_dict['ticker_symbol'],
                    iso_currency_code=security_dict['iso_currency_code'],
                    institution_id=security_dict['institution_id'],
                    institution_security_id=security_dict['institution_security_id'],
                    security_id=security_dict['security_id'],
                    proxy_security_id=security_dict['proxy_security_id'],
                    cusip=security_dict['cusip'],
                    isin=security_dict['isin'],
                    sedol=security_dict['sedol']
                ))

        # update the holdings
        for holding_dict in investment_dict["holdings"]:
            holding = self.get_holding_by_account_and_security(holding_dict["account_id"], holding_dict["security_id"])
            if holding is None:
                security = self.get_security_by_security_id(holding_dict['security_id'])
                holding = self.create_holding(CreateHoldingRequest(
                    account_id=account.id,
                    security_id=security.id,
                    cost_basis=holding_dict['cost_basis'],
                    quantity=holding_dict['quantity'],
                    iso_currency_code=holding_dict['iso_currency_code']
                ))
