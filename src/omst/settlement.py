from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from .data import synthetic_profiles, synthetic_settlement_intent, synthetic_transition_requirement
from .enums import MoneyState, TransitionEvaluationStatus, TransitionType
from .evaluation import evaluate_requirements
from .models import (
    CompositeMoneyState,
    MoneyProfile,
    MoneyTransition,
    SettlementCompatibility,
    SettlementIntent,
    TransactionContext,
    TransitionPlan,
    TransitionPlanStep,
)


def load_settlement_intent(path: Path | None = None) -> SettlementIntent:
    # v0.3 intentionally uses a deterministic synthetic default while schemas stabilise.
    return synthetic_settlement_intent()


def plan_transition(
    intent: SettlementIntent | None = None,
    source: str = "EUR-X",
    target: str = "EUR-Y",
) -> TransitionPlan:
    active_intent = intent or synthetic_settlement_intent()
    requirement = synthetic_transition_requirement()
    steps = [
        TransitionPlanStep(
            source=source,
            target="CBM",
            transition=TransitionType.CONVERT,
            requirements=requirement,
            expected_state=MoneyState.SETTLING,
            failure_path="timeout -> reconciliation_required -> recovered_or_failed",
        ),
        TransitionPlanStep(
            source="CBM",
            target=target,
            transition=TransitionType.SETTLE,
            requirements=requirement,
            expected_state=MoneyState.FINAL,
            failure_path="settlement_failed -> manual_intervention",
        ),
    ]
    return TransitionPlan(
        plan_id="plan-tokenized-bond-dvp",
        intent=active_intent,
        steps=steps,
        status="PLANNED",
        assumptions=["synthetic data", "not an issuer assessment", "not a regulatory assessment"],
    )


def evaluate_settlement(
    settlement_intent: SettlementIntent | None = None,
    asset_requirements: dict[str, object] | None = None,
    money_profile: MoneyProfile | None = None,
    money_state: CompositeMoneyState | None = None,
    evidence: list[object] | None = None,
) -> SettlementCompatibility:
    intent = settlement_intent or synthetic_settlement_intent()
    profiles = synthetic_profiles()
    source = money_profile or profiles["EUR-X"]
    target = profiles["EUR-Y"]
    requirement = synthetic_transition_requirement()
    transition = MoneyTransition(
        transition_id="settlement-evaluation-transition",
        transition_type=TransitionType.CONVERT,
        source_instrument=source.id,
        target_instrument=target.id,
        source_state=MoneyState.AVAILABLE,
        target_state=MoneyState.FINAL,
        quantity=intent.cash_amount,
        currency=intent.cash_currency,
        initiated_at=None,
        completed_at=None,
        settlement_finality=intent.required_finality,
        liquidity_consumed=Decimal(90000000),
        constraints={"latency_seconds": 45, "atomicity": intent.required_atomicity},
        evidence=[],
    )
    evaluation = evaluate_requirements(transition, synthetic_context_from_intent(intent), requirement, source, target)
    reasons = [{"code": reason.upper().replace(" ", "_")} for reason in evaluation.reasons]
    status = evaluation.status
    if status == TransitionEvaluationStatus.CONDITIONAL:
        status = TransitionEvaluationStatus.CONDITIONALLY_COMPATIBLE
    return SettlementCompatibility(
        status=status,
        reasons=reasons,
        required_transitions=plan_transition(intent, source.id, target.id).steps,
        evidence=[],
        assumptions=[
            "synthetic example",
            "not an issuer assessment",
            "not a regulatory assessment",
            "not a representation of actual market conditions",
        ],
        confidence="synthetic-reference",
    )


def synthetic_context_from_intent(intent: SettlementIntent) -> TransactionContext:
    return TransactionContext(
        name=intent.intent_type.lower(),
        transaction_type="DVP",
        amount=intent.cash_amount,
        currency=intent.cash_currency,
        asset=intent.asset,
        required_finality=intent.required_finality,
        max_latency_seconds=intent.maximum_latency_seconds,
        required_functions=("settlement",),
        venue=intent.venue,
        operating_window=intent.required_availability,
        settlement_mode="DVP",
    )
