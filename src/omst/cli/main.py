import argparse
import json
from dataclasses import asdict, is_dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from omst.cost import transition_cost
from omst.data import context_by_name, synthetic_graph, synthetic_liquidity, synthetic_profiles
from omst.enums import MoneyState, TransitionType
from omst.equivalence import monetary_equivalence
from omst.integrity import evaluate_transition
from omst.io import validate_document
from omst.models import MoneyTransition
from omst.routing import route_money
from omst.simulation import simulate
from omst.state import STATE_DEFINITIONS
from omst.velocity import settlement_velocity


def out(value: Any) -> None:
    if is_dataclass(value) and not isinstance(value, type):
        value = asdict(value)
    print(json.dumps(value, indent=2, default=str))

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="omst")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("validate"); p.add_argument("path")
    p = sub.add_parser("inspect"); p.add_argument("path")
    p = sub.add_parser("state"); p.add_argument("instrument")
    p = sub.add_parser("transition"); p.add_argument("--from", dest="from_", required=True); p.add_argument("--to", required=True); p.add_argument("--amount", required=True)
    p = sub.add_parser("compare"); p.add_argument("source"); p.add_argument("target")
    p = sub.add_parser("equivalence"); p.add_argument("source"); p.add_argument("target"); p.add_argument("--context", default="tokenized-dvp")
    p = sub.add_parser("velocity"); p.add_argument("instrument"); p.add_argument("--window", default="30d")
    p = sub.add_parser("liquidity"); p.add_argument("instrument")
    p = sub.add_parser("mobility"); p.add_argument("--from", dest="from_", required=True); p.add_argument("--to", required=True); p.add_argument("--amount", required=True)
    p = sub.add_parser("route"); p.add_argument("--from", dest="from_", required=True); p.add_argument("--to", required=True); p.add_argument("--amount", required=True); p.add_argument("--context", default="tokenized-dvp")
    sub.add_parser("graph")
    p = sub.add_parser("simulate"); p.add_argument("scenario")
    args = parser.parse_args(argv)
    profiles = synthetic_profiles()
    if args.cmd == "validate":
        path = Path(args.path)
        files = list(path.rglob("*.json")) if path.is_dir() else [path]
        errors = {str(f): validate_document(f) for f in files}
        failed = {k: v for k, v in errors.items() if v}
        out({"status": "VALID" if not failed else "INVALID", "checked": len(files), "errors": failed})
        return 1 if failed else 0
    if args.cmd == "inspect":
        out(json.loads(Path(args.path).read_text(encoding="utf-8")))
    elif args.cmd == "state":
        out({"instrument": args.instrument, "state": "AVAILABLE", "definition": STATE_DEFINITIONS["AVAILABLE"]})
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
    elif args.cmd == "graph":
        out({"nodes": list(profiles), "edges": synthetic_graph().edges})
    elif args.cmd == "simulate":
        out(simulate(args.scenario))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
