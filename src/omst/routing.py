from decimal import Decimal

from .graph import MoneyGraph
from .models import TransactionContext


def route_money(graph: MoneyGraph, source: str, target: str, amount: Decimal, context: TransactionContext) -> dict[str, object]:
    path = graph.route(source, target, amount, context.max_latency_seconds, context.required_finality)
    if not path:
        return {"status": "NO_ROUTE", "route": [], "reasons": ["no route satisfies hard transaction constraints"]}
    return {
        "status": "ROUTE_FOUND",
        "route": [path[0].source, *[edge.target for edge in path]],
        "cost_bps": sum((edge.cost_bps for edge in path), Decimal(0)),
        "latency_seconds": sum(edge.latency_seconds for edge in path),
        "liquidity_required": amount,
        "finality": min((edge.finality for edge in path), default="unknown"),
        "constraints": [edge.constraints for edge in path],
    }
