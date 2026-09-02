from __future__ import annotations

from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from typing import Any, cast

from .compatibility import (
    OMST_VERSION,
    RULESET_VERSION,
    canonical_hash,
    canonical_json,
    default_evidence_policy,
    evaluate_settlement_compatibility,
    load_money_profile,
    load_requirement_set,
    load_settlement_intent_v05,
    synthetic_money_states,
)
from .data import context_by_name, synthetic_graph
from .enums import (
    CapabilityType,
    MappingClassification,
    MappingDirection,
    NetworkType,
    ParticipantType,
    ProfileLifecycleStatus,
    SettlementRouteType,
    TransitionEvaluationStatus,
)
from .io import load_json
from .models import (
    InteroperabilityProfile,
    MoneyGraphSnapshot,
    MoneyProfileV06,
    ParticipantProfile,
    SettlementNetworkProfile,
    SettlementOffer,
    SettlementProfile,
    SettlementRequest,
    SettlementResponse,
)
from .routing import route_money
from .settlement import plan_transition

REFERENCE_VALID_UNTIL = "2026-09-03T00:00:00Z"


def profile_fingerprint(profile: dict[str, Any]) -> str:
    payload = {key: value for key, value in profile.items() if key != "profile_fingerprint"}
    return canonical_hash(payload)


def enrich_profile_fingerprint(profile: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(profile)
    enriched["profile_fingerprint"] = profile_fingerprint(enriched)
    return enriched


def example_money_profile_v06() -> MoneyProfileV06:
    profile = MoneyProfileV06(
        profile_id="money-eur-x-v06",
        profile_version="2026-09-01",
        omst_version=OMST_VERSION,
        identity={"instrument": "EUR-X", "name": "Synthetic regulated e-money"},
        issuer_reference="synthetic-issuer",
        currency="EUR",
        claim_type="regulated_e_money",
        monetary_layer="commercial_money",
        representation="tokenized_claim",
        ledger="synthetic-ledger-a",
        settlement_model="delivery-versus-payment",
        capabilities=(
            CapabilityType.TRANSFER,
            CapabilityType.DVP,
            CapabilityType.ATOMIC_SETTLEMENT,
            CapabilityType.SETTLEMENT,
        ),
        relations=("settled_in:CBM",),
        availability={"window": "24_7"},
        transferability={"institutional": True},
        redemption={"redeemable": True},
        access={"model": "institutional"},
        state_model={"available": "settlement_ready"},
        evidence_policy={"effective_liquidity_max_age_seconds": 60},
        jurisdiction_reference="EU-synthetic",
        metadata={"synthetic": True},
        lifecycle_status=ProfileLifecycleStatus.PUBLISHED,
        effective_from="2026-09-01T00:00:00Z",
    )
    return replace(profile, profile_fingerprint=canonical_hash(profile))


def example_settlement_profile() -> SettlementProfile:
    return SettlementProfile(
        settlement_profile_id="settlement-network-a",
        name="Synthetic Settlement Network A",
        version="2026-09-01",
        supported_assets=("synthetic-tokenised-bond",),
        supported_money=("EUR-X", "EUR-Y"),
        finality="qualified",
        atomicity=True,
        availability="24_7",
        latency={"maximum_seconds": 60, "observed_seconds": 45},
        transaction_limits={"maximum_amount": "150000000", "currency": "EUR"},
        operating_windows=("24_7",),
        supported_settlement_modes=("DVP", "ATOMIC"),
        interoperability={"profile": "OMST-INTEROPERABILITY"},
    )


def example_participant_profile() -> ParticipantProfile:
    return ParticipantProfile(
        participant_id="party-a",
        participant_type=ParticipantType.SETTLEMENT_AGENT,
        access_model="institutional",
        supported_money=("EUR-X",),
        supported_settlement=("settlement-network-a",),
        jurisdiction_reference="EU-synthetic",
        capabilities=(CapabilityType.DVP, CapabilityType.ATOMIC_SETTLEMENT),
        constraints={"pii": "not embedded in OMST core"},
    )


def example_network_profile() -> SettlementNetworkProfile:
    return SettlementNetworkProfile(
        network_id="network-a",
        network_type=NetworkType.PERMISSIONED_DLT,
        ledger_model="account-based",
        finality="qualified",
        availability="24_7",
        atomicity=True,
        access="permissioned",
        supported_instruments=("EUR-X", "EUR-Y"),
        supported_operations=(CapabilityType.TRANSFER, CapabilityType.DVP),
        interoperability={"neutral": True},
        failure_model={"liquidity_exhausted": "fallback_route"},
    )


def adapter_mapping(name: str) -> InteroperabilityProfile:
    normalized = name.lower()
    if normalized in {"otas", "asset"}:
        return InteroperabilityProfile(
            "adapter-otas-v06",
            "OTAS",
            "conceptual",
            MappingDirection.BIDIRECTIONAL,
            ("asset", "settlement_intent"),
            {
                "asset_id": MappingClassification.LOSSLESS,
                "cash_leg": MappingClassification.DERIVED,
                "money_state": MappingClassification.UNSUPPORTED,
            },
            MappingClassification.DERIVED,
            ("OTAS is asset-side; OMST remains money-side.",),
        )
    if normalized in {"iso20022", "iso-20022", "iso"}:
        return InteroperabilityProfile(
            "adapter-iso20022-v06",
            "ISO 20022",
            "conceptual",
            MappingDirection.EXTERNAL_TO_OMST,
            ("message", "payment_instruction"),
            {
                "amount": MappingClassification.EXACT,
                "currency": MappingClassification.EXACT,
                "settlement_state": MappingClassification.APPROXIMATED,
            },
            MappingClassification.APPROXIMATED,
            ("ISO 20022 is message semantics; OMST is monetary state-transition semantics.",),
        )
    return InteroperabilityProfile(
        "adapter-cdm-v06",
        "CDM",
        "conceptual",
        MappingDirection.BIDIRECTIONAL,
        ("financial_contract", "event"),
        {
            "contract_event": MappingClassification.LOSSY,
            "money_transition": MappingClassification.DERIVED,
            "legal_terms": MappingClassification.UNSUPPORTED,
        },
        MappingClassification.LOSSY,
        ("CDM covers contract semantics; OMST covers digital-money semantics.",),
    )


def graph_snapshot() -> MoneyGraphSnapshot:
    graph = synthetic_graph()
    return MoneyGraphSnapshot(
        snapshot_id="graph-snapshot-v06-tokenized-bond-dvp",
        timestamp="2026-09-01T00:00:00Z",
        nodes=tuple({"node_id": node, "node_type": "Money"} for node in sorted({"EUR-X", "EUR-Y", "EUR-Z", "CBM"})),
        edges=tuple(
            {
                "source": edge.source,
                "target": edge.target,
                "capability": "SETTLEMENT",
                "cost_bps": str(edge.cost_bps),
                "latency_seconds": edge.latency_seconds,
                "liquidity": str(edge.liquidity),
                "finality": edge.finality,
                "availability": edge.availability,
                "evidence": edge.evidence,
                "conditions": edge.constraints,
            }
            for edge in graph.edges
        ),
    )


def fallback_routes(source: str, target: str, amount: Decimal) -> dict[str, Any]:
    context = context_by_name("tokenized-dvp")
    graph = synthetic_graph()
    primary = route_money(graph, source, target, amount, context)
    fallback = {
        "type": SettlementRouteType.FALLBACK,
        "route": [source, "REDEMPTION", "BANK_MONEY", target],
        "conditions": ["issuer_available", "redemption_capacity_available", "deadline_not_exceeded"],
    }
    recovery = {
        "type": SettlementRouteType.RECOVERY,
        "route": ["reconcile", "restore_settlement_state"],
        "conditions": ["settlement_failed", "manual_or_automated_reconciliation_required"],
    }
    return {
        "snapshot_id": graph_snapshot().snapshot_id,
        "primary": primary,
        "fallback": canonical_json(fallback),
        "recovery": canonical_json(recovery),
    }


def settlement_offer() -> SettlementOffer:
    return SettlementOffer(
        offer_id="offer-party-a-eur-x",
        provider="party-a",
        money_profile="money-eur-x-v06",
        settlement_profile="settlement-network-a",
        available_amount=Decimal(120000000),
        availability="24_7",
        requirements_supported=("atomicity", "finality", "availability", "effective_liquidity"),
        evidence=(),
        valid_until=REFERENCE_VALID_UNTIL,
    )


def settlement_request(intent_path: Path | None = None) -> SettlementRequest:
    intent = load_settlement_intent_v05(intent_path or Path("examples/tokenized-bond-dvp/settlement-intent.json"))
    return SettlementRequest(
        request_id="request-tokenized-bond-dvp-eur-50m",
        settlement_intent=intent,
        required_money="EUR",
        required_capabilities=(CapabilityType.DVP, CapabilityType.ATOMIC_SETTLEMENT),
        amount=intent.cash_amount,
        deadline=REFERENCE_VALID_UNTIL,
        evidence_policy=default_evidence_policy(),
    )


def settlement_response(
    intent_path: Path,
    money_path: Path,
    settlement_profile_path: Path | None = None,
) -> SettlementResponse:
    request = settlement_request(intent_path)
    money = load_money_profile(money_path)
    settlement_profile = load_json(settlement_profile_path) if settlement_profile_path else {}
    evaluation = evaluate_settlement_compatibility(
        request.settlement_intent,
        money,
        synthetic_money_states().get(money.id),
        load_requirement_set(Path("examples/requirements/tokenized-bond-dvp.json")),
    )
    accepted = tuple(
        result.requirement.property
        for section in (
            evaluation.capability_evaluation,
            evaluation.state_evaluation,
            evaluation.evidence_evaluation,
        )
        for result in section.results
        if result.status == TransitionEvaluationStatus.COMPATIBLE
    )
    rejected = tuple(reason.source for reason in evaluation.blocking_conditions)
    conditional = tuple(reason.source for reason in evaluation.warnings)
    return SettlementResponse(
        request_id=request.request_id,
        status=evaluation.overall_status,
        accepted_requirements=accepted,
        rejected_requirements=rejected,
        conditional_requirements=conditional,
        evidence=(),
        transition_plan=plan_transition(request.settlement_intent),
        route={
            **fallback_routes("EUR-X", "EUR-Y", request.amount),
            "settlement_profile": settlement_profile.get("settlement_profile_id"),
            "settlement_profile_fingerprint": profile_fingerprint(settlement_profile) if settlement_profile else None,
        },
        valid_until=REFERENCE_VALID_UNTIL,
    )


def v06_manifest() -> dict[str, Any]:
    return {
        "omst_type": "omst-manifest",
        "omst_version": "0.7.0",
        "implementation": {"name": "python-reference", "version": "0.7.0"},
        "ruleset_version": RULESET_VERSION,
        "conformance": [
            {"profile": "OMST-CORE", "level": 3, "version": "0.7.0"},
            {"profile": "OMST-COMPATIBILITY", "level": 3, "version": "0.7.0"},
            {"profile": "OMST-INTEROPERABILITY", "level": 4, "version": "0.7.0"},
            {"profile": "OMST-VERIFICATION", "level": 4, "version": "0.7.0"},
        ],
        "profiles": ["money", "settlement", "participant", "interoperability"],
        "settlement": ["request", "offer", "response", "graph-snapshot", "evaluation-package"],
        "interoperability": ["generic", "otas", "iso20022", "cdm"],
        "verification": ["package", "verify", "record", "tamper-demo"],
        "experimental": True,
        "boundary": "Synthetic reference implementation; not issuer, regulatory or market-condition evidence.",
    }


def well_known_discovery() -> dict[str, Any]:
    return {
        "omst": "0.7.0",
        "implementation": "python-reference",
        "profiles": ["money", "settlement", "participant", "interoperability"],
        "conformance": ["CORE", "SETTLEMENT", "COMPATIBILITY", "INTEROPERABILITY", "VERIFICATION"],
        "manifest": "omst-manifest.json",
        "experimental": True,
    }


def api_response(endpoint: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    if endpoint == "profile/validate":
        return {"status": "VALID", "fingerprint": profile_fingerprint(payload) if payload else None}
    if endpoint == "settlement/request":
        return cast(dict[str, Any], canonical_json(settlement_request()))
    if endpoint == "settlement/evaluate":
        return cast(dict[str, Any], canonical_json(
            evaluate_settlement_compatibility(
                load_settlement_intent_v05(Path("examples/tokenized-bond-dvp/settlement-intent.json")),
                load_money_profile(Path("examples/eur-x.json")),
                synthetic_money_states()["EUR-X"],
                load_requirement_set(Path("examples/requirements/tokenized-bond-dvp.json")),
            )
        ))
    if endpoint == "settlement/response":
        return cast(dict[str, Any], canonical_json(
            settlement_response(
                Path("examples/tokenized-bond-dvp/settlement-intent.json"),
                Path("examples/eur-x.json"),
                Path("examples/settlement-networks/network-a.json"),
            )
        ))
    if endpoint == "route":
        return fallback_routes("EUR-X", "EUR-Y", Decimal(50000000))
    if endpoint == "conformance":
        from .conformance import run_conformance

        return cast(dict[str, Any], run_conformance())
    if endpoint == "adapter/map":
        return cast(dict[str, Any], canonical_json(adapter_mapping(str(payload.get("adapter", "iso20022")))))
    return {"status": "UNKNOWN_ENDPOINT", "endpoint": endpoint}
