from .enums import CapabilityStatus, CapabilityType, TransitionEvaluationStatus
from .integrity import evaluate_transition
from .models import (
    MoneyCapability,
    MoneyProfile,
    MoneyTransition,
    TransactionContext,
    TransitionEvaluation,
    TransitionRequirement,
)


def _capability_status(
    capabilities: list[MoneyCapability], capability: CapabilityType
) -> CapabilityStatus:
    for candidate in capabilities:
        if candidate.capability == capability:
            return candidate.status
    return CapabilityStatus.UNKNOWN


def evaluate_requirements(
    transition: MoneyTransition,
    context: TransactionContext,
    requirement: TransitionRequirement,
    source: MoneyProfile,
    target: MoneyProfile,
) -> TransitionEvaluation:
    reasons: list[str] = []
    integrity = evaluate_transition(transition, context, source, target)

    if requirement.required_finality_seconds is not None:
        latency = transition.constraints.get("latency_seconds")
        if latency is None:
            reasons.append("finality timing evidence is missing")
        elif int(latency) > requirement.required_finality_seconds:
            reasons.append("finality mismatch")

    if transition.quantity > requirement.minimum_liquidity:
        reasons.append("liquidity insufficient")

    for capability in requirement.required_capabilities:
        source_status = _capability_status(source.capabilities, capability)
        target_status = _capability_status(target.capabilities, capability)
        if CapabilityStatus.UNSUPPORTED in {source_status, target_status}:
            reasons.append(f"capability unavailable: {capability.value}")
        elif CapabilityStatus.UNKNOWN in {source_status, target_status}:
            reasons.append(f"capability evidence insufficient: {capability.value}")

    if requirement.evidence_required and not transition.evidence:
        reasons.append("evidence insufficient")

    if any(reason in reasons for reason in ["finality mismatch", "liquidity insufficient"]):
        status = TransitionEvaluationStatus.INCOMPATIBLE
    elif reasons:
        status = TransitionEvaluationStatus.CONDITIONAL
    else:
        status = TransitionEvaluationStatus.COMPATIBLE

    return TransitionEvaluation(status=status, reasons=reasons, integrity=integrity, requirement=requirement)
