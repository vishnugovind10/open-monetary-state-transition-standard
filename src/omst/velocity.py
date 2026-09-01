from decimal import Decimal


def settlement_velocity(settlement_value: Decimal, time_weighted_settlement_ready_balance: Decimal) -> Decimal:
    if time_weighted_settlement_ready_balance <= 0:
        raise ValueError("time-weighted settlement-ready balance must be positive")
    if settlement_value < 0:
        raise ValueError("settlement value must be non-negative")
    return settlement_value / time_weighted_settlement_ready_balance
