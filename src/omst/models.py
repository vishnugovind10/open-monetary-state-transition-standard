from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

from .enums import (
    CapabilityStatus,
    CapabilityType,
    CompatibilityReasonCode,
    EvidenceSourceType,
    MappingClassification,
    MappingDirection,
    MoneyEventType,
    MoneyState,
    NetworkType,
    ParticipantType,
    ProfileLifecycleStatus,
    ReasonSeverity,
    RelationType,
    RequirementComposition,
    RequirementOperator,
    RequirementPriority,
    SettlementBundleMode,
    SettlementLegRelation,
    SettlementLegType,
    TransitionEvaluationStatus,
    TransitionType,
)

EvidenceConfidence = str


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    source_type: EvidenceSourceType
    source_uri: str
    publisher: str
    publication_date: str
    retrieved_at: str
    claim: str
    scope: str
    confidence: EvidenceConfidence
    method: str


@dataclass(frozen=True)
class EvidenceChainStep:
    step_id: str
    kind: str
    input_reference: str
    output_claim: str
    method: str
    timestamp: str


@dataclass(frozen=True)
class MoneyCapability:
    capability: CapabilityType
    status: CapabilityStatus
    conditions: list[str] = field(default_factory=list)
    scope: str = "instrument"
    evidence: list[Evidence] = field(default_factory=list)
    valid_from: str | None = None
    valid_until: str | None = None


@dataclass(frozen=True)
class MoneyProfile:
    id: str
    name: str
    currency: str
    issuer: str
    claim_type: str
    monetary_layer_reference: str
    functions: dict[str, str]
    settlement_profile: dict[str, Any]
    redemption_profile: dict[str, Any]
    transfer_profile: dict[str, Any]
    access_profile: dict[str, Any]
    control_profile: dict[str, Any]
    network_profile: dict[str, Any]
    evidence: list[Evidence] = field(default_factory=list)
    capabilities: list[MoneyCapability] = field(default_factory=list)
    version: str = "0.3.0"


@dataclass(frozen=True)
class MoneyProfileV06:
    profile_id: str
    profile_version: str
    omst_version: str
    identity: dict[str, Any]
    issuer_reference: str
    currency: str
    claim_type: str
    monetary_layer: str
    representation: str
    ledger: str
    settlement_model: str
    capabilities: tuple[CapabilityType, ...]
    relations: tuple[str, ...]
    availability: dict[str, Any]
    transferability: dict[str, Any]
    redemption: dict[str, Any]
    access: dict[str, Any]
    state_model: dict[str, Any]
    evidence_policy: dict[str, Any]
    jurisdiction_reference: str
    metadata: dict[str, Any]
    lifecycle_status: ProfileLifecycleStatus = ProfileLifecycleStatus.DRAFT
    effective_from: str | None = None
    effective_until: str | None = None
    supersedes: str | None = None
    profile_fingerprint: str | None = None


@dataclass(frozen=True)
class SettlementProfile:
    settlement_profile_id: str
    name: str
    version: str
    supported_assets: tuple[str, ...]
    supported_money: tuple[str, ...]
    finality: str
    atomicity: bool
    availability: str
    latency: dict[str, Any]
    transaction_limits: dict[str, Any]
    operating_windows: tuple[str, ...]
    supported_settlement_modes: tuple[str, ...]
    interoperability: dict[str, Any]
    evidence: tuple[Evidence, ...] = ()


@dataclass(frozen=True)
class ParticipantProfile:
    participant_id: str
    participant_type: ParticipantType
    access_model: str
    supported_money: tuple[str, ...]
    supported_settlement: tuple[str, ...]
    jurisdiction_reference: str
    capabilities: tuple[CapabilityType, ...]
    constraints: dict[str, Any]
    evidence: tuple[Evidence, ...] = ()


@dataclass(frozen=True)
class SettlementNetworkProfile:
    network_id: str
    network_type: NetworkType
    ledger_model: str
    finality: str
    availability: str
    atomicity: bool
    access: str
    supported_instruments: tuple[str, ...]
    supported_operations: tuple[CapabilityType, ...]
    interoperability: dict[str, Any]
    failure_model: dict[str, Any]
    evidence: tuple[Evidence, ...] = ()


@dataclass(frozen=True)
class InteroperabilityProfile:
    profile_id: str
    external_standard: str
    external_version: str
    mapping_direction: MappingDirection
    supported_objects: tuple[str, ...]
    supported_fields: dict[str, MappingClassification]
    lossiness: MappingClassification
    constraints: tuple[str, ...]


@dataclass(frozen=True)
class SettlementOffer:
    offer_id: str
    provider: str
    money_profile: str
    settlement_profile: str
    available_amount: Decimal
    availability: str
    requirements_supported: tuple[str, ...]
    evidence: tuple[Evidence, ...]
    valid_until: str


@dataclass(frozen=True)
class SettlementRequest:
    request_id: str
    settlement_intent: SettlementIntent
    required_money: str
    required_capabilities: tuple[CapabilityType, ...]
    amount: Decimal
    deadline: str
    evidence_policy: EvidencePolicy


@dataclass(frozen=True)
class SettlementResponse:
    request_id: str
    status: TransitionEvaluationStatus
    accepted_requirements: tuple[str, ...]
    rejected_requirements: tuple[str, ...]
    conditional_requirements: tuple[str, ...]
    evidence: tuple[Evidence, ...]
    transition_plan: TransitionPlan | None
    route: dict[str, Any]
    valid_until: str


@dataclass(frozen=True)
class MoneyGraphSnapshot:
    snapshot_id: str
    timestamp: str
    nodes: tuple[dict[str, Any], ...]
    edges: tuple[dict[str, Any], ...]
    evidence: tuple[Evidence, ...] = ()


@dataclass(frozen=True)
class CompositeMoneyState:
    instrument: str
    availability: str
    transferability: str
    settlement: str
    redemption: str
    encumbrance: str
    finality: str
    operational_status: str
    evidence_status: str = "UNKNOWN"


@dataclass(frozen=True)
class MoneyTransition:
    transition_id: str
    transition_type: TransitionType
    source_instrument: str
    target_instrument: str
    source_state: MoneyState
    target_state: MoneyState
    quantity: Decimal
    currency: str
    initiated_at: str | None
    completed_at: str | None
    settlement_finality: str
    liquidity_consumed: Decimal
    constraints: dict[str, Any]
    evidence: list[Evidence] = field(default_factory=list)


@dataclass(frozen=True)
class MoneyEvent:
    event_id: str
    event_type: MoneyEventType
    instrument: str
    source_state: MoneyState
    target_state: MoneyState
    quantity: Decimal
    currency: str
    timestamp: str
    actor_reference: str
    ledger_reference: str
    transaction_reference: str
    evidence: list[Evidence] = field(default_factory=list)
    omst_schema_version: str = "0.3.0"


@dataclass(frozen=True)
class MoneyRelation:
    source_instrument: str
    target_instrument: str
    relation_type: RelationType
    cost_bps: Decimal
    latency_seconds: int
    liquidity: Decimal
    finality: str
    availability: str
    access: str
    constraints: dict[str, Any]
    evidence: list[Evidence] = field(default_factory=list)


@dataclass(frozen=True)
class LiquidityProfile:
    instrument: str
    nominal_supply: Decimal
    settlement_ready_balance: Decimal
    immediately_convertible_balance: Decimal
    observed_market_depth: Decimal
    redemption_capacity: Decimal
    measurement_window: str
    evidence: list[Evidence] = field(default_factory=list)


@dataclass(frozen=True)
class TransactionContext:
    name: str
    transaction_type: str = "DvP"
    amount: Decimal | None = None
    currency: str = "EUR"
    asset: str | None = None
    required_finality: str = "qualified"
    max_latency_seconds: int | None = None
    required_functions: tuple[str, ...] = ("settlement",)
    institution: str = "synthetic_institution"
    venue: str = "synthetic_venue"
    jurisdiction_reference: str = "unknown"
    operating_window: str = "unknown"
    settlement_mode: str = "conditional"


@dataclass(frozen=True)
class IntegrityResult:
    status: str
    dimensions: dict[str, str]
    reasons: list[str]
    evidence: list[Evidence]


@dataclass(frozen=True)
class TransitionRequirement:
    required_finality_seconds: int | None
    required_availability: str
    minimum_liquidity: Decimal
    required_capabilities: tuple[CapabilityType, ...]
    evidence_required: bool = True
    required_finality: str = "qualified"
    required_atomicity: bool = False
    required_access: str = "institutional"


@dataclass(frozen=True)
class EvidenceRequirement:
    accepted_sources: tuple[EvidenceSourceType, ...] = ()
    maximum_age_seconds: int | None = None
    required: bool = False


@dataclass(frozen=True)
class EvidencePolicy:
    accepted_sources: dict[str, tuple[EvidenceSourceType, ...]]
    max_age_seconds: dict[str, int]


@dataclass(frozen=True)
class EvaluationContext:
    omst_version: str
    ruleset_version: str
    evaluation_timestamp: str
    evidence_timestamp: str
    assumption_policy: str = "no_compatible_from_unknown"


@dataclass(frozen=True)
class MoneyRequirement:
    property: str
    operator: RequirementOperator
    value: object
    unit: str | None = None
    priority: RequirementPriority = RequirementPriority.MANDATORY
    evidence_requirement: EvidenceRequirement | None = None


@dataclass(frozen=True)
class MoneyRequirementSet:
    requirement_set_id: str
    description: str
    composition: RequirementComposition
    requirements: tuple[MoneyRequirement, ...]
    schema_version: str = "0.7.0"
    ruleset_version: str = "omst-core-0.7"


@dataclass(frozen=True)
class CompatibilityReason:
    code: CompatibilityReasonCode
    severity: ReasonSeverity
    description: str
    source: str


@dataclass(frozen=True)
class RequirementEvaluation:
    requirement: MoneyRequirement
    status: TransitionEvaluationStatus
    observed_value: object
    reasons: tuple[CompatibilityReason, ...] = ()


@dataclass(frozen=True)
class CompatibilitySectionEvaluation:
    status: TransitionEvaluationStatus
    results: tuple[RequirementEvaluation, ...]


@dataclass(frozen=True)
class SettlementLeg:
    leg_id: str
    leg_type: SettlementLegType
    instrument: str | None
    quantity: Decimal
    currency: str
    source: str
    destination: str
    required_state: MoneyState
    required_finality: str


@dataclass(frozen=True)
class SettlementLegDependency:
    source_leg_id: str
    target_leg_id: str
    relation: SettlementLegRelation


@dataclass(frozen=True)
class TransitionEvaluation:
    status: TransitionEvaluationStatus
    reasons: list[str]
    integrity: IntegrityResult
    requirement: TransitionRequirement


@dataclass(frozen=True)
class RouteEdge:
    source: str
    target: str
    cost_bps: Decimal
    latency_seconds: int
    liquidity: Decimal
    finality: str
    availability: str
    constraints: dict[str, Any]
    evidence: list[Evidence] = field(default_factory=list)


@dataclass(frozen=True)
class SettlementIntent:
    intent_id: str
    intent_type: str
    cash_currency: str
    cash_amount: Decimal
    asset: str | None
    required_finality: str
    maximum_latency_seconds: int | None
    required_availability: str
    required_atomicity: bool
    venue: str
    participants: tuple[str, ...] = ()
    omst_schema_version: str = "0.3.0"


@dataclass(frozen=True)
class TransitionPlanStep:
    source: str
    target: str
    transition: TransitionType
    requirements: TransitionRequirement
    expected_state: MoneyState
    failure_path: str
    evidence: list[Evidence] = field(default_factory=list)


@dataclass(frozen=True)
class TransitionPlan:
    plan_id: str
    intent: SettlementIntent
    steps: list[TransitionPlanStep]
    status: str
    assumptions: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SettlementBundle:
    bundle_id: str
    mode: SettlementBundleMode
    cash_leg: TransitionPlan | None
    asset_leg: dict[str, Any] | None = None
    fx_leg: dict[str, Any] | None = None
    collateral_leg: dict[str, Any] | None = None
    fee_leg: dict[str, Any] | None = None


@dataclass(frozen=True)
class SettlementCompatibility:
    status: TransitionEvaluationStatus
    reasons: list[dict[str, str]]
    required_transitions: list[TransitionPlanStep]
    evidence: list[Evidence]
    assumptions: list[str]
    confidence: str


@dataclass(frozen=True)
class SettlementCompatibilityProfile:
    evaluation_id: str
    omst_version: str
    settlement_intent: SettlementIntent
    money_instrument: str
    money_state: CompositeMoneyState
    requirements: MoneyRequirementSet
    capability_evaluation: CompatibilitySectionEvaluation
    state_evaluation: CompatibilitySectionEvaluation
    evidence_evaluation: CompatibilitySectionEvaluation
    overall_status: TransitionEvaluationStatus
    reasons: tuple[CompatibilityReason, ...]
    blocking_conditions: tuple[CompatibilityReason, ...]
    warnings: tuple[CompatibilityReason, ...]
    assumptions: tuple[str, ...]
    confidence: str
    generated_at: str
    evaluation_context: EvaluationContext
    evaluation_hash: str
