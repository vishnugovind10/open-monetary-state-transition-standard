from decimal import Decimal


def transition_cost(quantity: Decimal, liquidity: Decimal, c0: Decimal = Decimal(0), alpha: Decimal = Decimal("0.0001"), beta: Decimal = Decimal("0.01")) -> Decimal:
    if quantity < 0:
        raise ValueError("quantity must be non-negative")
    if liquidity <= 0:
        raise ValueError("liquidity must be positive")
    if quantity >= liquidity:
        raise ValueError("quantity must be lower than effective available liquidity")
    return c0 + alpha * quantity + beta * (quantity * quantity) / (liquidity - quantity)
