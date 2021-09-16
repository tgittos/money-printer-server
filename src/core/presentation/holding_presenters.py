class HoldingWithSecurity:
    def __init__(self, holding, security):
        self.holding = holding
        self.security = security

    def to_dict(self):
        return {
            'id': self.holding.id,
            'account_id': self.holding.account_id,
            'cost_basis': self.holding.cost_basis,
            'quantity': self.holding.quantity,
            'security_symbol': self.security.ticker_symbol,
            'iso_currency_code': self.holding.iso_currency_code,
            'timestamp': self.holding.timestamp.isoformat()
        }
