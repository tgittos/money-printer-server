import pytest
import random
from datetime import datetime, timezone

from core.models import Holding, HoldingBalance

from tests.fixtures import *

@pytest.fixture
def holding_factory(db, faker, account_factory, security_factory):
    def __holding_factory(
        account_id=None,
        security_id=None,
        cost_basis=random.random() * 5,
        quantity=random.randint(1, 500),
        iso_currency_code='USD'
    ):
        if account_id is None:
            account_id = account_factory().id
        if security_id is None:
            security_id = security_factory().id

        with db.get_session() as session:
            holding = Holding()

            holding.account_id = account_id
            holding.security_id = security_id
            holding.cost_basis = cost_basis
            holding.quantity = quantity
            holding.iso_currency_code = iso_currency_code
            holding.timestamp = datetime.now(tz=timezone.utc)

            session.add(holding)
            session.commit()

            return holding
    return __holding_factory