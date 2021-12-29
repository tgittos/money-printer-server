import pytest
import random
import string
from datetime import datetime, timezone

from core.models import Security
from core.lib.utilities import id_generator


@pytest.fixture
def security_factory(db, faker):
    def __security_factory(
        name = faker.unique.company(),
        ticker_symbol = id_generator(3, chars=string.ascii_uppercase),
        iso_currency_code = 'USD',
        institution_security_id = id_generator(),
        security_id = id_generator(),
        proxy_security_id = id_generator(),
        cusip = id_generator(),
        isin = id_generator(),
        sedol = id_generator()
    ):
        with db.get_session() as session:
            security = Security()

            security.name = name
            security.ticker_symbol = ticker_symbol
            security.iso_currency_code = iso_currency_code
            security.institution_security_id = institution_security_id
            security.security_id = security_id
            security.proxy_security_id = proxy_security_id
            security.cusip = cusip
            security.isin = isin
            security.sedol = sedol
            security.timestamp = datetime.utcnow()
        
            session.add(security)
            session.commit()

            return security
    return __security_factory