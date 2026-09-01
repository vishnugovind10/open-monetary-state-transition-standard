from __future__ import annotations

import hashlib
import json
from collections.abc import Container
from dataclasses import asdict, is_dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any

from .data import synthetic_profiles
from .enums import (
    CapabilityStatus,
    CapabilityType,
    CompatibilityReasonCode,
    EvidenceSourceType,
    ReasonSeverity,
    RequirementComposition,
    RequirementOperator,
    RequirementPriority,
    TransitionEvaluationStatus,
)
from .io import decimalize, load_json
from .models import (
    CompatibilityReason,
    CompatibilitySectionEvaluation,
    CompositeMoneyState,
    EvaluationContext,
    EvidencePolicy,
    EvidenceRequirement,
    MoneyCapability,
    MoneyProfile,
    MoneyRequirement,
    MoneyRequirementSet,
    RequirementEvaluation,
    SettlementCompatibilityProfile,
    SettlementIntent,
)

OMST_VERSION = "0.6.0"
RULESET_VERSION = "omst-core-0.6"
REFERENCE_TIMESTAMP = "2026-09-01T00:00:00Z"


def default_evaluation_context() -> EvaluationContext:
    return EvaluationContext(
        omst_version=OMST_VERSION,
        ruleset_version=RULESET_VERSION,
        evaluation_timestamp=REFERENCE_TIMESTAMP,
        evidence_timestamp=REFERENCE_TIMESTAMP,
    )


def default_evidence_policy() -> EvidencePolicy:
    return EvidencePolicy(
        accepted_sources={
            "effective_liquidity": (EvidenceSourceType.observed, EvidenceSourceType.derived),
            "finality": (EvidenceSourceType.official, EvidenceSourceType.derived),
            "availability": (EvidenceSourceType.official, EvidenceSourceType.observed),
        },
        max_age_seconds={"effective_liquidity": 60, "finality": 86_400, "availability": 86_400},
    )


def tokenized_bond_dvp_requirement_set() -> MoneyRequirementSet:
    freshness = EvidenceRequirement(
        accepted_sources=(EvidenceSourceType.observed, EvidenceSourceType.derived),
        maximum_age_seconds=60,
        required=True,
    )
    return MoneyRequirementSet(
        requirement_set_id="TOKENIZED_BOND_DVP_EUR",
        description="EUR tokenized bond DvP cash-leg requirements",
        composition=RequirementComposition.AND,
        requirements=(
            MoneyRequirement("currency", RequirementOperator.EQUALS, "EUR"),
            MoneyRequirement("finality", RequirementOperator.IN, ("qualified", "deterministic", "central-bank-final")),
            MoneyRequirement("atomicity", RequirementOperator.EQUALS, True),
            MoneyRequirement("availability", RequirementOperator.EQUALS, "24_7"),
            MoneyRequirement("maximum_latency_seconds", RequirementOperator.LESS_THAN_OR_EQUAL, 60, "seconds"),
            MoneyRequirement(
                "effective_liquidity",
                RequirementOperator.GREATER_THAN_OR_EQUAL,
                Decimal(50000000),
                "EUR",
                RequirementPriority.MANDATORY,
                freshness,
            ),
            MoneyRequirement("transferability", RequirementOperator.EQUALS, True),
            MoneyRequirement("access", RequirementOperator.EQUALS, "institutional"),
        ),
    )


def synthetic_money_states() -> dict[str, CompositeMoneyState]:
    return {
    "EUR-X": CompositeMoneyState(
        "EUR-X",
        "available",
        "transferable",
        "settlement_ready",
        "redeemable",
        "none",
        "qualified",
        "operational",
        "VALID",
    ),
    "EUR-Y": CompositeMoneyState(
        "EUR-Y",
        "available",
        "transferable",
        "settlement_ready",
        "redeemable",
        "none",
        "qualified",
        "operational",
        "STALE",
    ),
    "EUR-Z": CompositeMoneyState(
        "EUR-Z",
        "available",
        "transferable",
        "settlement_ready",
        "redeemable",
        "none",
        "probabilistic",
        "operational",
        "VALID",
    ),
    "CBM": CompositeMoneyState(
        "CBM",
        "available",
        "transferable",
        "settlement_ready",
        "redeemable",
        "none",
        "deterministic",
        "operational",
        "VALID",
    ),
    }


def synthetic_evidence_snapshot() -> dict[str, dict[str, Any]]:
    return {
        "EUR-X": {
            "effective_liquidity": Decimal(120000000),
            "latency_seconds": 45,
            "atomicity": True,
            "evidence_age_seconds": 30,
            "evidence_status": "VALID",
        },
        "EUR-Y": {
            "effective_liquidity": Decimal(90000000),
            "latency_seconds": 55,
            "atomicity": True,
            "evidence_age_seconds": 3_600,
            "evidence_status": "STALE",
        },
        "EUR-Z": {
            "effective_liquidity": Decimal(25000000),
            "latency_seconds": 120,
            "atomicity": False,
            "evidence_age_seconds": 45,
            "evidence_status": "VALID",
        },
        "CBM": {
            "effective_liquidity": Decimal(500000000),
            "latency_seconds": 15,
            "atomicity": True,
            "evidence_age_seconds": 30,
            "evidence_status": "VALID",
        },
    }


def load_requirement_set(path: Path | None) -> MoneyRequirementSet:
    if path is None:
        return tokenized_bond_dvp_requirement_set()
    data = load_json(path)
    requirements = tuple(_requirement_from_json(item) for item in data["requirements"])
    return MoneyRequirementSet(
        requirement_set_id=str(data["requirement_set_id"]),
        description=str(data.get("description", "")),
        composition=RequirementComposition(str(data.get("composition", "AND"))),
        requirements=requirements,
        schema_version=str(data.get("schema_version", OMST_VERSION)),
        ruleset_version=str(data.get("ruleset_version", RULESET_VERSION)),
    )


def load_money_profile(path: Path) -> MoneyProfile:
    data = load_json(path)
    capabilities = synthetic_profiles().get(str(data["id"]), synthetic_profiles()["EUR-X"]).capabilities
    return MoneyProfile(
        id=str(data["id"]),
        name=str(data["name"]),
        currency=str(data["currency"]),
        issuer=str(data.get("issuer", "synthetic")),
        claim_type=str(data.get("claim_type", "digital_money")),
        monetary_layer_reference=str(data.get("monetary_layer_reference", "unknown")),
        functions=dict(data.get("functions", {})),
        settlement_profile=dict(data.get("settlement_profile", {})),
        redemption_profile=dict(data.get("redemption_profile", {})),
        transfer_profile=dict(data.get("transfer_profile", {})),
        access_profile=dict(data.get("access_profile", {})),
        control_profile=dict(data.get("control_profile", {})),
        network_profile=dict(data.get("network_profile", {})),
        evidence=[],
        capabilities=capabilities,
        version=str(data.get("omst_schema_version", OMST_VERSION)),
    )


def load_settlement_intent_v05(path: Path) -> SettlementIntent:
    data = load_json(path)
    cash = dict(data.get("cash", {}))
    requirements = dict(data.get("requirements", {}))
    return SettlementIntent(
        intent_id=str(data["intent_id"]),
        intent_type=str(data.get("intent_type", data.get("transaction_type", "TOKENIZED_BOND_DVP"))),
        cash_currency=str(cash.get("currency", data.get("cash_currency", "EUR"))),
        cash_amount=decimalize(cash.get("amount", data.get("cash_amount", "0"))),
        asset=str(data.get("asset")) if data.get("asset") is not None else None,
        required_finality=str(requirements.get("finality", data.get("required_finality", "qualified"))),
        maximum_latency_seconds=(
            int(requirements["maximum_latency_seconds"])
            if requirements.get("maximum_latency_seconds") is not None
            else None
        ),
        required_availability=str(requirements.get("availability", data.get("required_availability", "24_7"))),
        required_atomicity=bool(requirements.get("atomicity", data.get("required_atomicity", False))),
        venue=str(data.get("venue", "synthetic-venue")),
        participants=tuple(str(item) for item in data.get("participants", ())),
        omst_schema_version=str(data.get("omst_schema_version", OMST_VERSION)),
    )


def evaluate_settlement_compatibility(
    settlement_intent: SettlementIntent,
    money_profile: MoneyProfile,
    money_state: CompositeMoneyState | None = None,
    requirements: MoneyRequirementSet | None = None,
    evidence: dict[str, Any] | None = None,
    context: EvaluationContext | None = None,
    policy: EvidencePolicy | None = None,
) -> SettlementCompatibilityProfile:
    active_requirements = requirements or tokenized_bond_dvp_requirement_set()
    active_state = money_state or synthetic_money_states().get(
        money_profile.id,
        CompositeMoneyState(money_profile.id, "unknown", "unknown", "unknown", "unknown", "unknown", "unknown", "unknown"),
    )
    active_evidence = evidence or synthetic_evidence_snapshot().get(money_profile.id, {})
    active_context = context or default_evaluation_context()
    active_policy = policy or default_evidence_policy()

    capability_results: list[RequirementEvaluation] = []
    state_results: list[RequirementEvaluation] = []
    evidence_results: list[RequirementEvaluation] = []

    for requirement in active_requirements.requirements:
        result = _evaluate_requirement(
            requirement,
            settlement_intent,
            money_profile,
            active_state,
            active_evidence,
            active_policy,
        )
        if requirement.property in {"atomicity", "access", "transferability"}:
            capability_results.append(result)
        elif requirement.property in {"availability", "finality"}:
            state_results.append(result)
        elif requirement.property in {"effective_liquidity", "maximum_latency_seconds"}:
            evidence_results.append(result)
        else:
            capability_results.append(result)

    reasons = tuple(reason for result in capability_results + state_results + evidence_results for reason in result.reasons)
    blocking = tuple(reason for reason in reasons if reason.severity == ReasonSeverity.BLOCKING)
    warnings = tuple(reason for reason in reasons if reason.severity == ReasonSeverity.WARNING)
    overall_status = _aggregate_status(tuple(capability_results + state_results + evidence_results))
    payload = {
        "intent": settlement_intent.intent_id,
        "money": money_profile.id,
        "state": active_state,
        "requirements": active_requirements,
        "reasons": reasons,
        "context": active_context,
    }
    evaluation_hash = canonical_hash(payload)
    return SettlementCompatibilityProfile(
        evaluation_id=f"eval-{settlement_intent.intent_id}-{money_profile.id}",
        omst_version=OMST_VERSION,
        settlement_intent=settlement_intent,
        money_instrument=money_profile.id,
        money_state=active_state,
        requirements=active_requirements,
        capability_evaluation=_section(capability_results),
        state_evaluation=_section(state_results),
        evidence_evaluation=_section(evidence_results),
        overall_status=overall_status,
        reasons=reasons,
        blocking_conditions=blocking,
        warnings=warnings,
        assumptions=("synthetic reference data", "no hidden network calls", "no compatible result from unknown evidence"),
        confidence="synthetic-reference",
        generated_at=active_context.evaluation_timestamp,
        evaluation_context=active_context,
        evaluation_hash=evaluation_hash,
    )


def explain_compatibility(profile: SettlementCompatibilityProfile | dict[str, Any]) -> str:
    data = canonical_json(profile) if not isinstance(profile, dict) else profile
    lines = [
        f"Evaluation: {data['evaluation_id']}",
        f"Instrument: {data['money_instrument']}",
        f"Status: {data['overall_status']}",
        "Reasons:",
    ]
    reasons = data.get("reasons", [])
    if not reasons:
        lines.append("- no blocking or warning reasons")
    for reason in reasons:
        lines.append(f"- {reason['code']} [{reason['severity']}]: {reason['description']}")
    lines.extend(
        [
            f"Evaluation hash: {data['evaluation_hash']}",
            "Boundary: Synthetic reference evaluation, not issuer or regulatory evidence.",
        ]
    )
    return "\n".join(lines)


def canonical_json(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return canonical_json(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, datetime):
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, dict):
        return {str(key): canonical_json(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [canonical_json(item) for item in value]
    return value


def canonical_dumps(value: Any) -> str:
    return json.dumps(canonical_json(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_dumps(value).encode("utf-8")).hexdigest()


def _requirement_from_json(data: dict[str, Any]) -> MoneyRequirement:
    evidence_requirement = None
    raw_evidence_requirement = data.get("evidence_requirement")
    if isinstance(raw_evidence_requirement, dict):
        evidence_requirement = EvidenceRequirement(
            accepted_sources=tuple(
                EvidenceSourceType(str(source).lower())
                for source in raw_evidence_requirement.get("accepted_sources", ())
            ),
            maximum_age_seconds=(
                int(raw_evidence_requirement["maximum_age_seconds"])
                if raw_evidence_requirement.get("maximum_age_seconds") is not None
                else None
            ),
            required=bool(raw_evidence_requirement.get("required", False)),
        )
    value = data.get("value")
    if data.get("property") == "effective_liquidity":
        value = decimalize(value)
    if isinstance(value, list):
        value = tuple(value)
    return MoneyRequirement(
        property=str(data["property"]),
        operator=RequirementOperator(str(data["operator"])),
        value=value,
        unit=str(data["unit"]) if data.get("unit") is not None else None,
        priority=RequirementPriority(str(data.get("priority", "MANDATORY"))),
        evidence_requirement=evidence_requirement,
    )


def _evaluate_requirement(
    requirement: MoneyRequirement,
    intent: SettlementIntent,
    profile: MoneyProfile,
    state: CompositeMoneyState,
    evidence: dict[str, Any],
    policy: EvidencePolicy,
) -> RequirementEvaluation:
    observed = _observed_value(requirement.property, intent, profile, state, evidence)
    reason = _reason_for_requirement(requirement, observed, evidence, policy)
    if reason is None:
        return RequirementEvaluation(requirement, TransitionEvaluationStatus.COMPATIBLE, observed)
    status = (
        TransitionEvaluationStatus.INCOMPATIBLE
        if reason.severity == ReasonSeverity.BLOCKING
        else TransitionEvaluationStatus.CONDITIONALLY_COMPATIBLE
    )
    return RequirementEvaluation(requirement, status, observed, (reason,))


def _observed_value(
    prop: str,
    intent: SettlementIntent,
    profile: MoneyProfile,
    state: CompositeMoneyState,
    evidence: dict[str, Any],
) -> Any:
    if prop == "currency":
        return profile.currency
    if prop == "finality":
        return profile.settlement_profile.get("finality_type", state.finality)
    if prop == "atomicity":
        return bool(evidence.get("atomicity", _capability_status(profile.capabilities, CapabilityType.ATOMIC_SETTLEMENT) != CapabilityStatus.UNSUPPORTED))
    if prop == "availability":
        return profile.settlement_profile.get("availability", state.availability)
    if prop == "maximum_latency_seconds":
        return evidence.get("latency_seconds", intent.maximum_latency_seconds)
    if prop == "effective_liquidity":
        return evidence.get("effective_liquidity")
    if prop == "transferability":
        return bool(profile.transfer_profile.get("transferable", state.transferability == "transferable"))
    if prop == "access":
        return "institutional" if profile.access_profile.get("institutional") else "restricted"
    return None


def _reason_for_requirement(
    requirement: MoneyRequirement,
    observed: Any,
    evidence: dict[str, Any],
    policy: EvidencePolicy,
) -> CompatibilityReason | None:
    code_by_property = {
        "currency": CompatibilityReasonCode.CURRENCY_MISMATCH,
        "finality": CompatibilityReasonCode.FINALITY_MISMATCH,
        "atomicity": CompatibilityReasonCode.ATOMICITY_UNAVAILABLE,
        "availability": CompatibilityReasonCode.AVAILABILITY_MISMATCH,
        "maximum_latency_seconds": CompatibilityReasonCode.LATENCY_REQUIREMENT_UNMET,
        "effective_liquidity": CompatibilityReasonCode.LIQUIDITY_INSUFFICIENT,
        "transferability": CompatibilityReasonCode.TRANSFERABILITY_RESTRICTED,
        "access": CompatibilityReasonCode.ACCESS_RESTRICTED,
    }
    if observed is None:
        return _reason(CompatibilityReasonCode.EVIDENCE_INSUFFICIENT, ReasonSeverity.WARNING, "Observed value is missing.", requirement.property)
    if not _operator_passes(requirement.operator, observed, requirement.value):
        severity = ReasonSeverity.BLOCKING if requirement.priority == RequirementPriority.MANDATORY else ReasonSeverity.WARNING
        return _reason(
            code_by_property.get(requirement.property, CompatibilityReasonCode.UNKNOWN_REQUIREMENT),
            severity,
            f"{requirement.property} requirement was not satisfied.",
            requirement.property,
        )
    if requirement.evidence_requirement is not None:
        stale = _evidence_is_stale(requirement, evidence, policy)
        if stale:
            return _reason(
                CompatibilityReasonCode.LIQUIDITY_EVIDENCE_STALE
                if requirement.property == "effective_liquidity"
                else CompatibilityReasonCode.EVIDENCE_STALE,
                ReasonSeverity.WARNING,
                f"{requirement.property} evidence exceeds the permitted age.",
                requirement.property,
            )
    if evidence.get("evidence_status") == "CONFLICTING":
        return _reason(
            CompatibilityReasonCode.CONFLICTING_EVIDENCE,
            ReasonSeverity.WARNING,
            "Evidence snapshot contains conflicting claims.",
            requirement.property,
        )
    return None


def _operator_passes(operator: RequirementOperator, observed: Any, expected: Any) -> bool:
    if operator == RequirementOperator.EQUALS:
        return bool(observed == expected)
    if operator == RequirementOperator.NOT_EQUALS:
        return bool(observed != expected)
    if operator == RequirementOperator.IN:
        return _container_has(expected, observed)
    if operator == RequirementOperator.NOT_IN:
        return not _container_has(expected, observed)
    if operator == RequirementOperator.LESS_THAN_OR_EQUAL:
        return Decimal(str(observed)) <= Decimal(str(expected))
    if operator == RequirementOperator.LESS_THAN:
        return Decimal(str(observed)) < Decimal(str(expected))
    if operator == RequirementOperator.GREATER_THAN_OR_EQUAL:
        return Decimal(str(observed)) >= Decimal(str(expected))
    if operator == RequirementOperator.GREATER_THAN:
        return Decimal(str(observed)) > Decimal(str(expected))
    if operator in {RequirementOperator.REQUIRES, RequirementOperator.AVAILABLE_DURING, RequirementOperator.WITHIN}:
        return bool(observed)
    if operator == RequirementOperator.FORBIDS:
        return not bool(observed)
    return False


def _container_has(container: Any, value: Any) -> bool:
    if not isinstance(container, Container):
        return False
    result = container.__contains__(value)
    return bool(result)


def _evidence_is_stale(
    requirement: MoneyRequirement,
    evidence: dict[str, Any],
    policy: EvidencePolicy,
) -> bool:
    evidence_requirement = requirement.evidence_requirement
    if evidence_requirement is None:
        return False
    maximum_age = evidence_requirement.maximum_age_seconds
    if maximum_age is None:
        maximum_age = policy.max_age_seconds.get(requirement.property)
    if maximum_age is None:
        return False
    age = evidence.get("evidence_age_seconds")
    return age is None or int(age) > maximum_age


def _aggregate_status(results: tuple[RequirementEvaluation, ...]) -> TransitionEvaluationStatus:
    if any(result.status == TransitionEvaluationStatus.INCOMPATIBLE for result in results):
        return TransitionEvaluationStatus.INCOMPATIBLE
    if any(result.status == TransitionEvaluationStatus.UNKNOWN for result in results):
        return TransitionEvaluationStatus.UNKNOWN
    if any(result.status == TransitionEvaluationStatus.CONDITIONALLY_COMPATIBLE for result in results):
        return TransitionEvaluationStatus.CONDITIONALLY_COMPATIBLE
    return TransitionEvaluationStatus.COMPATIBLE


def _section(results: list[RequirementEvaluation]) -> CompatibilitySectionEvaluation:
    return CompatibilitySectionEvaluation(_aggregate_status(tuple(results)), tuple(results))


def _capability_status(
    capabilities: list[MoneyCapability],
    capability: CapabilityType,
) -> CapabilityStatus:
    for candidate in capabilities:
        if candidate.capability == capability:
            return candidate.status
    return CapabilityStatus.UNKNOWN


def _reason(
    code: CompatibilityReasonCode,
    severity: ReasonSeverity,
    description: str,
    source: str,
) -> CompatibilityReason:
    return CompatibilityReason(code=code, severity=severity, description=description, source=source)
