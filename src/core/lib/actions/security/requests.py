from datetime import datetime

from core.models.profile import Profile
from core.models.account import Account
from core.models.security import Security
from core.models.holding import Holding


class CreateSecurityRequest:
    def __init__(self, profile: Profile, account: Account, name: str, ticker_symbol: str, iso_currency_code: str,
                 institution_id: str, institution_security_id: str, security_id:str , proxy_security_id: str,
                 cusip: str, isin: str, sedol: str):
        self.profile = profile
        self.account = account
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
    def __init__(self, account: Account, security: Security, cost_basis: float, quantity: float,
                 iso_currency_code: str):
        self.account = account
        self.security = security
        self.cost_basis = cost_basis
        self.quantity = quantity
        self.iso_currency_code = iso_currency_code


class UpdateHoldingRequest:
    def __init__(self, holding: Holding, cost_basis: float, quantity: float):
        self.holding = holding
        self.cost_basis = cost_basis
        self.quantity = quantity


class CreateInvestmentTransactionRequest:
    def __init__(self, account: Account, date: datetime, name: str, amount: float, fees: float, price: float,
                 quantity: float, iso_currency_code: str, type: str, subtype: str, investment_transaction_id: str):
        self.account = account
        self.date = date
        self.name = name
        self.amount = amount
        self.fees = fees
        self.price = price
        self.quantity = quantity
        self.type = type
        self.subtype = subtype
        self.iso_currency_code = iso_currency_code
        self.investment_transaction_id = investment_transaction_id
