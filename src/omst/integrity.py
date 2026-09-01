from decimal import Decimal

from .enums import IntegrityStatus
from .models import IntegrityResult, MoneyProfile, MoneyTransition, TransactionContext

FINALITY_ORDER = {"none": 0, "probabilistic": 1, "qualified": 2, "deterministic": 3}

def evaluate_transition(transition: MoneyTransition, context: TransactionContext, source: MoneyProfile | None = None, target: MoneyProfile | None = None) -> IntegrityResult:
    dimensions: dict[str, str] = {}
    reasons: list[str] = []
    evidence = list(transition.evidence)
    required_rank = FINALITY_ORDER.get(context.required_finality, -1)
    actual_rank = FINALITY_ORDER.get(transition.settlement_finality, -1)
    if actual_rank < 0 or required_rank < 0:
        dimensions["finality"] = IntegrityStatus.UNKNOWN.value
    elif actual_rank >= required_rank:
        dimensions["finality"] = IntegrityStatus.PRESERVED.value
    else:
        dimensions["finality"] = IntegrityStatus.DEGRADED.value
        reasons.append("settlement finality is below context requirement")
    latency = transition.constraints.get("latency_seconds")
    if context.max_latency_seconds is not None and latency is not None:
        if int(latency) <= context.max_latency_seconds:
            dimensions["latency"] = IntegrityStatus.PRESERVED.value
        else:
            dimensions["latency"] = IntegrityStatus.DEGRADED.value
            reasons.append("settlement latency exceeds context deadline")
    else:
        dimensions["latency"] = IntegrityStatus.UNKNOWN.value
    if source and target:
        for fn in context.required_functions:
            ok = source.functions.get(fn) in {"supported", "conditional"} and target.functions.get(fn) in {"supported", "conditional"}
            dimensions[f"function:{fn}"] = IntegrityStatus.PRESERVED.value if ok else IntegrityStatus.DEGRADED.value
            if not ok:
                reasons.append(f"required function {fn} is not supported by both instruments")
    if transition.liquidity_consumed > Decimal(0) and transition.quantity > transition.liquidity_consumed:
        dimensions["liquidity"] = IntegrityStatus.DEGRADED.value
        reasons.append("transition quantity exceeds represented liquidity consumed")
    else:
        dimensions["liquidity"] = IntegrityStatus.PRESERVED.value
    if any(v == IntegrityStatus.DEGRADED.value for v in dimensions.values()):
        status = IntegrityStatus.DEGRADED.value
    elif any(v == IntegrityStatus.UNKNOWN.value for v in dimensions.values()):
        status = IntegrityStatus.UNKNOWN.value
    else:
        status = IntegrityStatus.PRESERVED.value
    return IntegrityResult(status=status, dimensions=dimensions, reasons=reasons, evidence=evidence)
