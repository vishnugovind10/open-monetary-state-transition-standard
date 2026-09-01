from decimal import Decimal


def monetary_fragmentation_index(weighted_frictions: list[tuple[Decimal, Decimal]]) -> Decimal:
    if not weighted_frictions:
        return Decimal(0)
    total = Decimal(0)
    for weight, friction in weighted_frictions:
        if weight < 0 or friction < 0:
            raise ValueError("weights and frictions must be non-negative")
        total += weight * friction
    return total
