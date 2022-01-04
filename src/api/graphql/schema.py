import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from api.views.decorators import decode_token

from core.repositories.account_repository import AccountRepository
from core.repositories.holding_repository import HoldingRepository
from core.repositories.security_repository import SecurityRepository

from core.models.profile import Profile as ProfileModel
from core.models.account import Account as AccountModel
from core.models.account_balance import AccountBalance as AccountBalanceModel
from core.models.holding import Holding as HoldingModel
from core.models.holding_balance import HoldingBalance as HoldingBalanceModel
from core.models.security import Security as SecurityModel
from core.models.security_price import SecurityPrice as SecurityPriceModel

from core.schemas.profile_schemas import ReadProfileSchema


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


# built in queries the user can call?
class Query(graphene.ObjectType):
    # accounts = SQLAlchemyConnectionField(Account.connection)
    accounts = graphene.List(Account)
    # holdings = SQLAlchemyConnectionField(Holding.connection)
    holdings = graphene.List(Holding)
    # securities = SQLAlchemyConnectionField(Security.connection)
    securities = graphene.List(Security)

    security_prices = SQLAlchemyConnectionField(SecurityPrice.connection)

    profile = graphene.Field(Profile)
    node = relay.Node.Field()

    def resolve_profile(self, info):
        return ReadProfileSchema().load(decode_token())

    def resolve_accounts(self, info):
        profile = self.resolve_profile(info)
        return AccountRepository().get_accounts_by_profile_id(profile.id).data

    def resolve_holdings(self, info):
        profile = self.resolve_profile(info)
        return HoldingRepository().get_holdings_by_profile_id(profile.id).data

    def resolve_securities(self, info):
        profile = self.resolve_profile(info)
        return SecurityRepository().get_securities_by_profile_id(profile.id).data


schema = graphene.Schema(query=Query)
