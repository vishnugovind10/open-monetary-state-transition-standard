from decimal import Decimal

from omst.data import context_by_name, synthetic_profiles
from omst.enums import (
    CapabilityType,
    MoneyEventType,
    MoneyState,
    TransitionEvaluationStatus,
    TransitionType,
)
from omst.equivalence import monetary_equivalence
from omst.evaluation import evaluate_requirements
from omst.events import validate_event_semantics
from omst.models import MoneyEvent, MoneyTransition, TransitionRequirement


def test_monetary_equivalence_distinguishes_nominal_from_settlement_equivalence() -> None:
    profiles = synthetic_profiles()
    result = monetary_equivalence(profiles["EUR-X"], profiles["EUR-Z"], context_by_name("tokenized-dvp"))

    assert result["nominally_equivalent"] is True
    assert result["functionally_equivalent"] is True
    assert result["settlement_equivalent"] is False
    assert result["status"] == "FUNCTIONALLY_EQUIVALENT"


def test_transition_requirement_reports_evidence_insufficient_condition() -> None:
    profiles = synthetic_profiles()
    transition = MoneyTransition(
        transition_id="tx-v02",
        transition_type=TransitionType.CONVERT,
        source_instrument="EUR-X",
        target_instrument="EUR-Y",
        source_state=MoneyState.AVAILABLE,
        target_state=MoneyState.FINAL,
        quantity=Decimal(50000000),
        currency="EUR",
        initiated_at=None,
        completed_at=None,
        settlement_finality="qualified",
        liquidity_consumed=Decimal(50000000),
        constraints={"latency_seconds": 45},
        evidence=[],
    )
    requirement = TransitionRequirement(
        required_finality_seconds=60,
        required_availability="business_hours",
        minimum_liquidity=Decimal(50000000),
        required_capabilities=(CapabilityType.SETTLEMENT, CapabilityType.ATOMIC_SETTLEMENT),
        evidence_required=True,
    )

    result = evaluate_requirements(
        transition,
        context_by_name("tokenized-dvp"),
        requirement,
        profiles["EUR-X"],
        profiles["EUR-Y"],
    )

    assert result.status == TransitionEvaluationStatus.CONDITIONAL
    assert result.reasons == ["evidence insufficient"]


def test_transition_requirement_detects_incompatible_liquidity_and_finality() -> None:
    profiles = synthetic_profiles()
    transition = MoneyTransition(
        transition_id="tx-v02-fail",
        transition_type=TransitionType.CONVERT,
        source_instrument="EUR-X",
        target_instrument="EUR-Y",
        source_state=MoneyState.AVAILABLE,
        target_state=MoneyState.FINAL,
        quantity=Decimal(70000000),
        currency="EUR",
        initiated_at=None,
        completed_at=None,
        settlement_finality="probabilistic",
        liquidity_consumed=Decimal(50000000),
        constraints={"latency_seconds": 120},
        evidence=[],
    )
    requirement = TransitionRequirement(
        required_finality_seconds=60,
        required_availability="business_hours",
        minimum_liquidity=Decimal(50000000),
        required_capabilities=(CapabilityType.SETTLEMENT,),
        evidence_required=False,
    )

    result = evaluate_requirements(
        transition,
        context_by_name("tokenized-dvp"),
        requirement,
        profiles["EUR-X"],
        profiles["EUR-Y"],
    )

    assert result.status == TransitionEvaluationStatus.INCOMPATIBLE
    assert "finality mismatch" in result.reasons
    assert "liquidity insufficient" in result.reasons


def test_event_semantics_accepts_settlement_final() -> None:
    event = MoneyEvent(
        event_id="event-001",
        event_type=MoneyEventType.SETTLEMENT_FINAL,
        instrument="EUR-X",
        source_state=MoneyState.SETTLING,
        target_state=MoneyState.FINAL,
        quantity=Decimal(50000000),
        currency="EUR",
        timestamp="2026-01-01T12:00:00Z",
        actor_reference="synthetic-participant",
        ledger_reference="synthetic-ledger",
        transaction_reference="synthetic-tx",
    )

    assert validate_event_semantics(event) == []


def test_event_semantics_rejects_wrong_target_state() -> None:
    event = MoneyEvent(
        event_id="event-002",
        event_type=MoneyEventType.SETTLEMENT_FINAL,
        instrument="EUR-X",
        source_state=MoneyState.SETTLING,
        target_state=MoneyState.AVAILABLE,
        quantity=Decimal(50000000),
        currency="EUR",
        timestamp="2026-01-01T12:00:00Z",
        actor_reference="synthetic-participant",
        ledger_reference="synthetic-ledger",
        transaction_reference="synthetic-tx",
    )

    errors = validate_event_semantics(event)
    assert "event target state does not match event type" in errors
