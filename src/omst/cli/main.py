import argparse
import json
from dataclasses import asdict, is_dataclass
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any

from omst.cost import transition_cost
from omst.data import (
    context_by_name,
    synthetic_graph,
    synthetic_liquidity,
    synthetic_profiles,
)
from omst.enums import MoneyState, TransitionType
from omst.equivalence import monetary_equivalence
from omst.integrity import evaluate_transition
from omst.io import validate_document
from omst.models import MoneyTransition
from omst.routing import route_money
from omst.settlement import evaluate_settlement, load_settlement_intent, plan_transition
from omst.simulation import simulate
from omst.state import STATE_DEFINITIONS
from omst.stress import stress_test
from omst.velocity import settlement_velocity


def out(value: Any) -> None:
    if is_dataclass(value) and not isinstance(value, type):
        value = asdict(value)
    print(json.dumps(to_plain(value), indent=2, default=str))


def to_plain(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return to_plain(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): to_plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_plain(item) for item in value]
    return value

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="omst")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("validate"); p.add_argument("path")
    p = sub.add_parser("inspect"); p.add_argument("path")
    p = sub.add_parser("profile"); p.add_argument("path")
    p = sub.add_parser("state"); p.add_argument("instrument")
    p = sub.add_parser("capability"); p.add_argument("instrument")
    p = sub.add_parser("transition"); p.add_argument("--from", dest="from_", required=True); p.add_argument("--to", required=True); p.add_argument("--amount", required=True)
    p = sub.add_parser("compare"); p.add_argument("source"); p.add_argument("target")
    p = sub.add_parser("equivalence"); p.add_argument("source"); p.add_argument("target"); p.add_argument("--context", default="tokenized-dvp")
    p = sub.add_parser("velocity"); p.add_argument("instrument"); p.add_argument("--window", default="30d")
    p = sub.add_parser("liquidity"); p.add_argument("instrument")
    p = sub.add_parser("mobility"); p.add_argument("--from", dest="from_", required=True); p.add_argument("--to", required=True); p.add_argument("--amount", required=True)
    p = sub.add_parser("route"); p.add_argument("--from", dest="from_", required=True); p.add_argument("--to", required=True); p.add_argument("--amount", required=True); p.add_argument("--context", default="tokenized-dvp")
    p = sub.add_parser("evaluate-settlement"); p.add_argument("path")
    p = sub.add_parser("plan"); p.add_argument("path")
    p = sub.add_parser("graph"); p.add_argument("--format", choices=["json", "mermaid"], default="json")
    p = sub.add_parser("simulate"); p.add_argument("scenario")
    p = sub.add_parser("stress"); p.add_argument("--scenario", default="liquidity-shock")
    args = parser.parse_args(argv)
    profiles = synthetic_profiles()
    if args.cmd == "validate":
        path = Path(args.path)
        files = list(path.rglob("*.json")) if path.is_dir() else [path]
        errors = {str(f): validate_document(f) for f in files}
        failed = {k: v for k, v in errors.items() if v}
        out({"status": "VALID" if not failed else "INVALID", "checked": len(files), "errors": failed})
        return 1 if failed else 0
    if args.cmd == "inspect" or args.cmd == "profile":
        out(json.loads(Path(args.path).read_text(encoding="utf-8")))
    elif args.cmd == "state":
        out({"instrument": args.instrument, "state": "AVAILABLE", "definition": STATE_DEFINITIONS["AVAILABLE"]})
    elif args.cmd == "capability":
        out({"instrument": args.instrument, "capabilities": profiles[args.instrument].capabilities})
    elif args.cmd == "transition":
        src_id, src_state = args.from_.split(":")
        tgt_id, tgt_state = args.to.split(":")
        transition = MoneyTransition("cli-transition", TransitionType.CONVERT, src_id, tgt_id, MoneyState(src_state), MoneyState(tgt_state), Decimal(args.amount), "EUR", None, None, "qualified", Decimal(args.amount), {"latency_seconds": 45}, [])
        result = evaluate_transition(transition, context_by_name("tokenized-dvp"), profiles.get(src_id), profiles.get(tgt_id))
        out(result)
    elif args.cmd == "compare":
        out({"source": profiles[args.source], "target": profiles[args.target]})
    elif args.cmd == "equivalence":
        out(monetary_equivalence(profiles[args.source], profiles[args.target], context_by_name(args.context)))
    elif args.cmd == "velocity":
        out({"instrument": args.instrument, "window": args.window, "settlement_velocity": settlement_velocity(Decimal(5000000000), Decimal(500000000))})
    elif args.cmd == "liquidity":
        out(synthetic_liquidity(args.instrument))
    elif args.cmd == "mobility":
        amount = Decimal(args.amount)
        out({"route": route_money(synthetic_graph(), args.from_, args.to, amount, context_by_name("tokenized-dvp")), "transition_cost": transition_cost(amount, Decimal(100000000))})
    elif args.cmd == "route":
        out(route_money(synthetic_graph(), args.from_, args.to, Decimal(args.amount), context_by_name(args.context)))
    elif args.cmd == "evaluate-settlement":
        out(evaluate_settlement(load_settlement_intent(Path(args.path))))
    elif args.cmd == "plan":
        out(plan_transition(load_settlement_intent(Path(args.path))))
    elif args.cmd == "graph":
        graph = synthetic_graph()
        if args.format == "mermaid":
            print(graph.to_mermaid())
        else:
            out({"nodes": list(profiles), "edges": graph.edges})
    elif args.cmd == "simulate":
        out(simulate(args.scenario))
    elif args.cmd == "stress":
        out(stress_test(args.scenario))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
