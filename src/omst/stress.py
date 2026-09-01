from decimal import Decimal

from .cost import transition_cost


def stress_test(scenario: str = "liquidity-shock") -> dict[str, object]:
    if scenario != "liquidity-shock":
        raise ValueError(f"unsupported stress scenario: {scenario}")
    starting_liquidity = Decimal(500000000)
    transaction_amount = Decimal(50000000)
    shocks = [Decimal("0.50"), Decimal("0.75"), Decimal("0.90")]
    results: list[dict[str, object]] = []
    for shock in shocks:
        remaining = starting_liquidity * (Decimal(1) - shock)
        utilisation = transaction_amount / remaining if remaining > 0 else Decimal("Infinity")
        compatible = transaction_amount < remaining
        cost = transition_cost(transaction_amount, remaining) if compatible else None
        results.append(
            {
                "liquidity_shock": str(shock),
                "remaining_liquidity": remaining,
                "liquidity_utilisation": utilisation,
                "compatible": compatible,
                "transition_cost": cost,
                "integrity": "PRESERVED" if compatible else "DEGRADED",
            }
        )
    return {
        "scenario": scenario,
        "synthetic": True,
        "starting_liquidity": starting_liquidity,
        "transaction_amount": transaction_amount,
        "results": results,
    }
