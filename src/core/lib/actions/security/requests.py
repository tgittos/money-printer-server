from core.models.holding import Holding


class UpdateHoldingRequest:
    def __init__(self, holding: Holding, cost_basis: float, quantity: float):
        self.holding = holding
        self.cost_basis = cost_basis
        self.quantity = quantity
