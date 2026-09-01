from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

from .enums import EvidenceSourceType, MoneyState, TransitionType

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
    required_finality: str = "qualified"
    max_latency_seconds: int | None = None
    required_functions: tuple[str, ...] = ("settlement",)
    institution: str = "synthetic_institution"
    venue: str = "synthetic_venue"

@dataclass(frozen=True)
class IntegrityResult:
    status: str
    dimensions: dict[str, str]
    reasons: list[str]
    evidence: list[Evidence]

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
