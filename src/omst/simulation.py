from decimal import Decimal

from .data import context_by_name, synthetic_graph
from .models import RouteEdge
from .routing import route_money

SCENARIOS = {
    "normal": ("ROUTE_FOUND", Decimal(50000000)),
    "liquidity-shock": ("NO_ROUTE", Decimal(125000000)),
    "redemption-shock": ("DEGRADED", Decimal(50000000)),
    "velocity-shock": ("ROUTE_FOUND", Decimal(50000000)),
    "network-fragmentation": ("NO_ROUTE", Decimal(50000000)),
    "settlement-failure": ("NO_ROUTE", Decimal(50000000)),
    "finality-degradation": ("NO_ROUTE", Decimal(50000000)),
    "conversion-failure": ("NO_ROUTE", Decimal(50000000)),
}

def simulate(name: str) -> dict[str, object]:
    if name not in SCENARIOS:
        raise ValueError(f"unknown simulation: {name}")
    expected, amount = SCENARIOS[name]
    graph = synthetic_graph()
    if name in {"network-fragmentation", "settlement-failure", "conversion-failure"}:
        graph.edges = []
    if name == "finality-degradation":
        graph.edges = [
            RouteEdge(
                edge.source,
                edge.target,
                edge.cost_bps,
                edge.latency_seconds,
                edge.liquidity,
                "probabilistic",
                edge.availability,
                edge.constraints,
                edge.evidence,
            )
            for edge in graph.edges
        ]
    result = route_money(graph, "EUR-X", "EUR-Y", amount, context_by_name("tokenized-dvp"))
    if name == "redemption-shock":
        result["status"] = expected
        result["reasons"] = ["redemption demand exceeds synthetic redemption capacity"]
    return {"scenario": name, "synthetic": True, "result": result, "expected": expected}
