from typing import List, Optional

from core.models.holding import Holding
from core.models.security import Security
from core.repositories.stock_repository import StockRepository
from core.lib.types import HoldingList
from core.lib.logger import get_logger


class HoldingWithSecurity:
    def __init__(self, holding: Holding, ticker: str, price: float):
        self.holding = holding
        self.ticker = ticker
        self.price = price

    def to_dict(self):
        return {
            'id': self.holding.id,
            'account_id': self.holding.account_id,
            'cost_basis': self.holding.cost_basis,
            'quantity': self.holding.quantity,
            'security_symbol': self.ticker,
            'latest_price': self.price,
            'iso_currency_code': self.holding.iso_currency_code,
            'timestamp': self.holding.timestamp.isoformat(),
        }


HoldingWithSecurityList = List[HoldingWithSecurity]


class HoldingPresenter:

    logger = get_logger(__name__)

    def __init__(self, db):
        self.db = db
        self.repo = StockRepository()

    def with_balances(self, security: Security, holdings: HoldingList) -> Optional[HoldingWithSecurityList]:
        if not holdings:
            return None
        augmented_records = []
        for holding_record in holdings:
            if not holding_record:
                continue

            last_price = None
            if security:
                last_price = self.repo.previous(security.ticker_symbol)
                if last_price is not None:
                    last_price = last_price.iloc[0]
            if last_price is not None:
                holding_record.timestamp = last_price.date
                augmented_record = HoldingWithSecurity(
                    holding=holding_record,
                    ticker=security.ticker_symbol,
                    price=last_price.close
                )
                self.logger.debug("augmented holding {0} with balance {1}".format(augmented_record, last_price.close))
            else:
                augmented_record = HoldingWithSecurity(holding=holding_record, ticker=security.ticker_symbol, price=0)

            augmented_records.append(augmented_record)

        return augmented_records
