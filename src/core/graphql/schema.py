import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from core.models.profile import Profile as ProfileModel
from core.models.account import Account as AccountModel
from core.models.account_balance import AccountBalance as AccountBalanceModel
from core.models.holding import Holding as HoldingModel
from core.models.holding_balance import HoldingBalance as HoldingBalanceModel
from core.models.security import Security as SecurityModel
from core.models.security_price import SecurityPrice as SecurityPriceModel

class Profile(SQLAlchemyObjectType):
    class Meta:
        model = ProfileModel
        exclude_fields = ("password",)
        interfaces = (relay.Node,)


class Account(SQLAlchemyObjectType):
    class Meta:
        model = AccountModel
        exclude_fields = ("plaid_item_id", "plaid_item")
        interfaces = (relay.Node,)


class AccountBalance(SQLAlchemyObjectType):
    class Meta:
        model = AccountBalanceModel
        interfaces = (relay.Node,)


class Holding(SQLAlchemyObjectType):
    class Meta:
        model = HoldingModel
        interfaces = (relay.Node,)
        

class HoldingBalance(SQLAlchemyObjectType):
    class Meta:
        model = HoldingBalanceModel
        interfaces = (relay.Node,)


class Security(SQLAlchemyObjectType):
    class Meta:
        model = SecurityModel
        interfaces = (relay.Node,)
    

class SecurityPrice(SQLAlchemyObjectType):
    class Meta:
        model = SecurityPriceModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()


schema = graphene.Schema(query=Query)