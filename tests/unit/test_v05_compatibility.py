from decimal import Decimal

from omst.compatibility import (
    canonical_hash,
    evaluate_settlement_compatibility,
    synthetic_money_states,
    tokenized_bond_dvp_requirement_set,
)
from omst.conformance import run_conformance
from omst.data import synthetic_profiles, synthetic_settlement_intent
from omst.enums import CompatibilityReasonCode, TransitionEvaluationStatus


def test_tokenized_bond_dvp_candidates_have_distinct_results() -> None:
    profiles = synthetic_profiles()
    states = synthetic_money_states()
    intent = synthetic_settlement_intent()
    requirements = tokenized_bond_dvp_requirement_set()

    eur_x = evaluate_settlement_compatibility(intent, profiles["EUR-X"], states["EUR-X"], requirements)
    eur_y = evaluate_settlement_compatibility(intent, profiles["EUR-Y"], states["EUR-Y"], requirements)
    eur_z = evaluate_settlement_compatibility(intent, profiles["EUR-Z"], states["EUR-Z"], requirements)

    assert eur_x.overall_status == TransitionEvaluationStatus.COMPATIBLE
    assert eur_y.overall_status == TransitionEvaluationStatus.CONDITIONALLY_COMPATIBLE
    assert eur_z.overall_status == TransitionEvaluationStatus.INCOMPATIBLE
    assert [reason.code for reason in eur_y.warnings] == [
        CompatibilityReasonCode.LIQUIDITY_EVIDENCE_STALE
    ]
    assert CompatibilityReasonCode.FINALITY_MISMATCH in {reason.code for reason in eur_z.reasons}
    assert CompatibilityReasonCode.LIQUIDITY_INSUFFICIENT in {reason.code for reason in eur_z.reasons}


def test_evaluation_hash_is_deterministic_and_input_sensitive() -> None:
    base = {"amount": Decimal(50000000), "instrument": "EUR-X"}
    changed = {"amount": Decimal(50000001), "instrument": "EUR-X"}

    assert canonical_hash(base) == canonical_hash(base)
    assert canonical_hash(base) != canonical_hash(changed)


def test_conformance_runner_reports_pass() -> None:
    result = run_conformance()

    assert result["vectors"] == "PASS"
    assert result["failures"] == []
    assert result["profiles"]["OMST-SETTLEMENT"]["status"] == "PASS"
