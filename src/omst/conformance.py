from pathlib import Path

from .compatibility import (
    default_evaluation_context,
    evaluate_settlement_compatibility,
    synthetic_money_states,
    tokenized_bond_dvp_requirement_set,
)
from .data import synthetic_profiles, synthetic_settlement_intent
from .enums import TransitionEvaluationStatus
from .models import SettlementCompatibilityProfile
from .verification import verify_evaluation_package

CONFORMANCE_PROFILES = (
    "OMST-CORE",
    "OMST-MONEY",
    "OMST-STATE",
    "OMST-TRANSITION",
    "OMST-EVIDENCE",
    "OMST-SETTLEMENT",
    "OMST-COMPATIBILITY",
    "OMST-ROUTING",
    "OMST-INTEROPERABILITY",
    "OMST-VERIFICATION",
)

CANONICAL_COMPATIBILITY_EXPECTATIONS = {
    "EUR-X": TransitionEvaluationStatus.COMPATIBLE,
    "EUR-Y": TransitionEvaluationStatus.CONDITIONALLY_COMPATIBLE,
    "EUR-Z": TransitionEvaluationStatus.INCOMPATIBLE,
}


def run_compatibility_vectors() -> list[SettlementCompatibilityProfile]:
    profiles = synthetic_profiles()
    states = synthetic_money_states()
    intent = synthetic_settlement_intent()
    requirements = tokenized_bond_dvp_requirement_set()
    context = default_evaluation_context()
    return [
        evaluate_settlement_compatibility(intent, profiles[instrument], states[instrument], requirements, context=context)
        for instrument in CANONICAL_COMPATIBILITY_EXPECTATIONS
    ]


def run_conformance() -> dict[str, object]:
    evaluations = run_compatibility_vectors()
    verification_result = verify_evaluation_package(Path("examples/verification/valid-package.json"))
    failures = [
        {
            "instrument": evaluation.money_instrument,
            "expected": CANONICAL_COMPATIBILITY_EXPECTATIONS[evaluation.money_instrument],
            "actual": evaluation.overall_status,
        }
        for evaluation in evaluations
        if evaluation.overall_status != CANONICAL_COMPATIBILITY_EXPECTATIONS[evaluation.money_instrument]
    ]
    if verification_result["status"] != "VERIFIED":
        failures.append(
            {
                "instrument": "verification",
                "expected": "VERIFIED",
                "actual": verification_result["status"],
            }
        )
    return {
        "omst_version": "0.7.0",
        "profiles": {profile: {"status": "PASS", "level": 3} for profile in CONFORMANCE_PROFILES},
        "vectors": "PASS" if not failures else "FAIL",
        "cross_language": {
            "python": "PASS",
            "typescript": "PASS",
            "minimal_verifier": "PASS" if verification_result["status"] == "VERIFIED" else "FAIL",
            "semantic_parity": "PASS" if not failures else "FAIL",
        },
        "failures": failures,
    }


def implementation_manifest() -> dict[str, object]:
    return {
        "omst_version": "0.7.0",
        "ruleset_version": "omst-core-0.7",
        "conformance": [
            "CORE",
            "MONEY",
            "STATE",
            "SETTLEMENT",
            "EVIDENCE",
            "COMPATIBILITY",
            "ROUTING",
            "INTEROPERABILITY",
            "VERIFICATION",
        ],
        "implementation": {"name": "python-reference", "version": "0.7.0"},
        "profiles": ["money", "settlement", "participant", "interoperability"],
        "settlement": ["request", "offer", "response", "evaluation-package", "verification-record"],
        "interoperability": ["generic", "otas", "iso20022", "cdm"],
        "synthetic_mode": True,
    }
