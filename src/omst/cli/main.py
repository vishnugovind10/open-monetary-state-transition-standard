import argparse
import json
from dataclasses import asdict, is_dataclass
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any

from omst.compatibility import (
    canonical_json,
    evaluate_settlement_compatibility,
    explain_compatibility,
    load_money_profile,
    load_requirement_set,
    load_settlement_intent_v05,
    synthetic_money_states,
)
from omst.conformance import run_conformance
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
from omst.interoperability import (
    adapter_mapping,
    api_response,
    example_participant_profile,
    example_settlement_profile,
    profile_fingerprint,
    settlement_response,
    v06_manifest,
    well_known_discovery,
)
from omst.io import validate_document
from omst.models import MoneyTransition
from omst.routing import route_money
from omst.settlement import evaluate_settlement, load_settlement_intent, plan_transition
from omst.simulation import simulate
from omst.state import STATE_DEFINITIONS
from omst.stress import stress_test
from omst.velocity import settlement_velocity
from omst.verification import (
    build_evaluation_package,
    human_verification_record,
    seal_evaluation_package,
    settlement_evaluation_bundle,
    tamper_package,
    verification_summary,
    verify_evaluation_package,
)


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
    p = sub.add_parser("profile"); p.add_argument("path", nargs="?"); p.add_argument("extra", nargs="?")
    p = sub.add_parser("state"); p.add_argument("instrument")
    p = sub.add_parser("capability"); p.add_argument("instrument")
    p = sub.add_parser("requirement"); p.add_argument("path", nargs="?")
    p = sub.add_parser("transition"); p.add_argument("--from", dest="from_", required=True); p.add_argument("--to", required=True); p.add_argument("--amount", required=True)
    p = sub.add_parser("compare"); p.add_argument("source"); p.add_argument("target")
    p = sub.add_parser("equivalence"); p.add_argument("source"); p.add_argument("target"); p.add_argument("--context", default="tokenized-dvp")
    p = sub.add_parser("velocity"); p.add_argument("instrument"); p.add_argument("--window", default="30d")
    p = sub.add_parser("liquidity"); p.add_argument("instrument")
    p = sub.add_parser("mobility"); p.add_argument("--from", dest="from_", required=True); p.add_argument("--to", required=True); p.add_argument("--amount", required=True)
    p = sub.add_parser("route"); p.add_argument("--from", dest="from_", required=True); p.add_argument("--to", required=True); p.add_argument("--amount", required=True); p.add_argument("--context", default="tokenized-dvp")
    p = sub.add_parser("evaluate-settlement"); p.add_argument("path", nargs="?"); p.add_argument("--intent"); p.add_argument("--money"); p.add_argument("--settlement")
    p = sub.add_parser("plan"); p.add_argument("path")
    p = sub.add_parser("explain"); p.add_argument("path")
    p = sub.add_parser("conformance"); p.add_argument("--profile")
    sub.add_parser("manifest")
    sub.add_parser("discovery")
    p = sub.add_parser("settlement-profile"); p.add_argument("path", nargs="?")
    p = sub.add_parser("participant"); p.add_argument("path", nargs="?")
    p = sub.add_parser("interoperability"); p.add_argument("path", nargs="?")
    p = sub.add_parser("adapter"); p.add_argument("name", nargs="?", default="iso20022")
    p = sub.add_parser("fingerprint"); p.add_argument("path")
    p = sub.add_parser("exchange"); p.add_argument("--intent", default="examples/tokenized-bond-dvp/settlement-intent.json"); p.add_argument("--money", default="examples/eur-x.json"); p.add_argument("--settlement", default="examples/settlement-networks/network-a.json")
    p = sub.add_parser("api"); p.add_argument("endpoint")
    p = sub.add_parser("package"); p.add_argument("action", choices=["create", "seal"]); p.add_argument("path", nargs="?"); p.add_argument("--intent", default="examples/tokenized-bond-dvp/settlement-intent.json"); p.add_argument("--money", default="examples/eur-x.json"); p.add_argument("--settlement", default="examples/settlement-networks/network-a.json")
    p = sub.add_parser("bundle"); p.add_argument("action", choices=["create", "verify"]); p.add_argument("path", nargs="?")
    p = sub.add_parser("verify"); p.add_argument("path"); p.add_argument("--human", action="store_true")
    p = sub.add_parser("tamper"); p.add_argument("mutation"); p.add_argument("path", nargs="?")
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
    if args.cmd == "inspect":
        out(json.loads(Path(args.path).read_text(encoding="utf-8")))
    elif args.cmd == "profile":
        if args.path == "validate":
            profile_path = Path(args.extra or "examples/profiles/money/eur-x.v06.json")
            profile_errors = validate_document(profile_path)
            payload = json.loads(profile_path.read_text(encoding="utf-8"))
            out(
                {
                    "status": "VALID" if not profile_errors else "INVALID",
                    "errors": profile_errors,
                    "profile_fingerprint": profile_fingerprint(payload),
                }
            )
            return 1 if profile_errors else 0
        out(json.loads(Path(args.path or "examples/profiles/money/eur-x.v06.json").read_text(encoding="utf-8")))
    elif args.cmd == "state":
        out({"instrument": args.instrument, "state": "AVAILABLE", "definition": STATE_DEFINITIONS["AVAILABLE"]})
    elif args.cmd == "capability":
        out({"instrument": args.instrument, "capabilities": profiles[args.instrument].capabilities})
    elif args.cmd == "requirement":
        requirement_path = Path(args.path) if args.path else None
        out(load_requirement_set(requirement_path))
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
        intent_arg = args.intent or args.path
        if args.money and intent_arg:
            intent_path = Path(intent_arg)
            requirement_path = Path("examples/requirements/tokenized-bond-dvp.json")
            money = load_money_profile(Path(args.money))
            states = synthetic_money_states()
            out(
                canonical_json(
                    evaluate_settlement_compatibility(
                        load_settlement_intent_v05(intent_path),
                        money,
                        states.get(money.id),
                        load_requirement_set(requirement_path if requirement_path.exists() else None),
                    )
                )
            )
        else:
            out(evaluate_settlement(load_settlement_intent(Path(args.path))))
    elif args.cmd == "plan":
        out(plan_transition(load_settlement_intent(Path(args.path))))
    elif args.cmd == "explain":
        print(explain_compatibility(json.loads(Path(args.path).read_text(encoding="utf-8"))))
    elif args.cmd == "conformance":
        result = canonical_json(run_conformance())
        if args.profile:
            profiles_result = result["profiles"]
            out({args.profile: profiles_result.get(args.profile, "UNKNOWN")})
        else:
            out(result)
    elif args.cmd == "manifest":
        out(v06_manifest())
    elif args.cmd == "discovery":
        out(well_known_discovery())
    elif args.cmd == "settlement-profile":
        if args.path:
            out(json.loads(Path(args.path).read_text(encoding="utf-8")))
        else:
            out(canonical_json(example_settlement_profile()))
    elif args.cmd == "participant":
        if args.path:
            out(json.loads(Path(args.path).read_text(encoding="utf-8")))
        else:
            out(canonical_json(example_participant_profile()))
    elif args.cmd == "interoperability":
        if args.path:
            out(json.loads(Path(args.path).read_text(encoding="utf-8")))
        else:
            out(canonical_json(adapter_mapping("iso20022")))
    elif args.cmd == "adapter":
        out(canonical_json(adapter_mapping(args.name)))
    elif args.cmd == "fingerprint":
        out({"profile_fingerprint": profile_fingerprint(json.loads(Path(args.path).read_text(encoding="utf-8")))})
    elif args.cmd == "exchange":
        out(canonical_json(settlement_response(Path(args.intent), Path(args.money), Path(args.settlement))))
    elif args.cmd == "api":
        if args.endpoint == "verification/package":
            out(build_evaluation_package())
        elif args.endpoint == "verification/verify":
            out(verify_evaluation_package(Path("examples/verification/valid-package.json")))
        elif args.endpoint == "verification/record":
            out(verify_evaluation_package(Path("examples/verification/valid-package.json"))["record"])
        elif args.endpoint == "verification/tamper":
            out(verify_evaluation_package(Path("examples/verification/tampered-evidence.json")))
        else:
            out(api_response(args.endpoint))
    elif args.cmd == "package":
        if args.action == "create":
            out(
                build_evaluation_package(
                    Path(args.intent),
                    Path(args.money),
                    Path(args.settlement),
                )
            )
        else:
            out(seal_evaluation_package(json.loads(Path(args.path).read_text(encoding="utf-8"))))
    elif args.cmd == "bundle":
        if args.action == "create":
            out(settlement_evaluation_bundle())
        else:
            bundle_verification = verify_evaluation_package(
                json.loads(Path(args.path).read_text(encoding="utf-8"))["evaluation_package"]
            )
            print(verification_summary(bundle_verification))
    elif args.cmd == "verify":
        verification = verify_evaluation_package(Path(args.path))
        if args.human:
            print(human_verification_record(verification["record"]))
        else:
            print(verification_summary(verification))
    elif args.cmd == "tamper":
        package_path = Path(args.path or "examples/verification/valid-package.json")
        out(tamper_package(json.loads(package_path.read_text(encoding="utf-8")), args.mutation))
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
