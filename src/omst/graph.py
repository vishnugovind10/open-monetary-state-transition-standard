from decimal import Decimal

from .models import RouteEdge


class MoneyGraph:
    def __init__(self, edges: list[RouteEdge] | None = None) -> None:
        self.edges = edges or []
    def add_edge(self, edge: RouteEdge) -> None:
        self.edges.append(edge)
    def neighbours(self, node: str) -> list[RouteEdge]:
        return [edge for edge in self.edges if edge.source == node]
    def route(self, source: str, target: str, amount: Decimal, max_latency_seconds: int | None = None, required_finality: str = "qualified") -> list[RouteEdge] | None:
        queue: list[tuple[str, list[RouteEdge]]] = [(source, [])]
        seen = {source}
        while queue:
            node, path = queue.pop(0)
            if node == target:
                return path
            for edge in sorted(self.neighbours(node), key=lambda e: (e.cost_bps, e.latency_seconds)):
                if edge.target in seen or edge.liquidity < amount or edge.availability != "available":
                    continue
                if max_latency_seconds is not None and sum(e.latency_seconds for e in path + [edge]) > max_latency_seconds:
                    continue
                if required_finality == "qualified" and edge.finality not in {"qualified", "deterministic"}:
                    continue
                seen.add(edge.target)
                queue.append((edge.target, path + [edge]))
        return None
