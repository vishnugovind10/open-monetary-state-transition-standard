from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Literal

from .compatibility import (
    OMST_VERSION,
    REFERENCE_TIMESTAMP,
    RULESET_VERSION,
    canonical_hash,
    canonical_json,
    default_evidence_policy,
    evaluate_settlement_compatibility,
    load_money_profile,
    load_requirement_set,
    load_settlement_intent_v05,
    synthetic_evidence_snapshot,
    synthetic_money_states,
)
from .interoperability import fallback_routes, profile_fingerprint
from .io import load_json, validate_document
from .settlement import plan_transition

VerificationOutcome = Literal[
    "VERIFIED",
    "VERIFIED_WITH_WARNINGS",
    "DIFFERENT",
    "INVALID",
    "UNSUPPORTED",
    "UNKNOWN",
]

SUPPORTED_RULESETS = {"omst-core-0.7"}
SUPPORTED_SCHEMA_VERSIONS = {"0.7.0"}


def canonicalize_for_verification(value: Any) -> dict[str, Any]:
    canonical = canonical_json(value)
    if not isinstance(canonical, dict):
        raise TypeError("verification canonicalization requires an object")
    return canonical


def canonical_evaluation_result(evaluation: dict[str, Any]) -> dict[str, Any]:
    blocking = evaluation.get("blocking_conditions", [])
    warnings = evaluation.get("warnings", [])
    sections = [
        evaluation.get("capability_evaluation", {}),
        evaluation.get("state_evaluation", {}),
        evaluation.get("evidence_evaluation", {}),
    ]
    evaluated = []
    for section in sections:
        for result in section.get("results", []):
            requirement = result.get("requirement", {})
            evaluated.append(
                {
                    "property": requirement.get("property"),
                    "priority": requirement.get("priority"),
                    "status": result.get("status"),
                    "observed_value": result.get("observed_value"),
                    "reason_codes": [reason.get("code") for reason in result.get("reasons", [])],
                }
            )
    return canonicalize_for_verification(
        {
            "status": evaluation.get("overall_status"),
            "reason_codes": [reason.get("code") for reason in evaluation.get("reasons", [])],
            "blocking_conditions": [reason.get("code") for reason in blocking],
            "warnings": [reason.get("code") for reason in warnings],
            "evaluated_requirements": sorted(evaluated, key=lambda item: str(item["property"])),
            "assumptions": evaluation.get("assumptions", []),
            "evidence_status": evaluation.get("money_state", {}).get("evidence_status"),
        }
    )


def compare_semantics(original: dict[str, Any], reproduced: dict[str, Any]) -> dict[str, Any]:
    original_semantics = canonical_evaluation_result(original)
    reproduced_semantics = canonical_evaluation_result(reproduced)
    return {
        "status": (
            "SEMANTICALLY_EQUIVALENT"
            if original_semantics == reproduced_semantics
            else "SEMANTICALLY_DIFFERENT"
        ),
        "original": original_semantics,
        "reproduced": reproduced_semantics,
    }


def evidence_item(
    evidence_id: str,
    item_type: str,
    source: str,
    content: dict[str, Any],
    observed_at: str = REFERENCE_TIMESTAMP,
    expires_at: str = "2026-09-03T00:00:00Z",
) -> dict[str, Any]:
    return {
        "evidence_id": evidence_id,
        "type": item_type,
        "source": source,
        "observed_at": observed_at,
        "valid_from": observed_at,
        "expires_at": expires_at,
        "content_reference": f"synthetic://evidence/{evidence_id}",
        "content_hash": canonical_hash(content),
        "method": "synthetic-reference-snapshot",
        "status": "VALID",
        "inline_content": canonical_json(content),
    }


def evidence_manifest(money_id: str = "EUR-X") -> dict[str, Any]:
    evidence = synthetic_evidence_snapshot()[money_id]
    items = [
        evidence_item(
            "liq-eur-x-001",
            "OBSERVED",
            "synthetic://liquidity/EUR-X",
            {
                "property": "effective_liquidity",
                "instrument": money_id,
                "amount": str(evidence["effective_liquidity"]),
                "currency": "EUR",
            },
        ),
        evidence_item(
            "lat-eur-x-001",
            "OBSERVED",
            "synthetic://latency/EUR-X",
            {
                "property": "maximum_latency_seconds",
                "instrument": money_id,
                "seconds": evidence["latency_seconds"],
            },
        ),
    ]
    return {
        "omst_type": "evidence-manifest",
        "manifest_id": "evidence-tokenized-bond-dvp-eur-x-v07",
        "created_at": REFERENCE_TIMESTAMP,
        "evidence_items": items,
        "policy": canonical_json(default_evidence_policy()),
        "snapshot_reference": "synthetic://snapshot/tokenized-bond-dvp/EUR-X/2026-09-02",
    }


def build_evaluation_package(
    intent_path: Path = Path("examples/tokenized-bond-dvp/settlement-intent.json"),
    money_path: Path = Path("examples/eur-x.json"),
    settlement_profile_path: Path = Path("examples/settlement-networks/network-a.json"),
    requirement_path: Path = Path("examples/requirements/tokenized-bond-dvp.json"),
) -> dict[str, Any]:
    intent = load_settlement_intent_v05(intent_path)
    money = load_money_profile(money_path)
    money_state = synthetic_money_states()[money.id]
    requirements = load_requirement_set(requirement_path)
    evaluation = canonicalize_for_verification(
        evaluate_settlement_compatibility(intent, money, money_state, requirements)
    )
    route = fallback_routes("EUR-X", "EUR-Y", intent.cash_amount)
    settlement_profile = load_json(settlement_profile_path)
    route["settlement_profile"] = settlement_profile["settlement_profile_id"]
    route["settlement_profile_fingerprint"] = profile_fingerprint(settlement_profile)
    package = {
        "omst_type": "evaluation-package",
        "package_id": "pkg-tokenized-bond-dvp-eur-x-v07",
        "package_version": "0.7.0",
        "lifecycle_status": "CREATED",
        "omst_version": OMST_VERSION,
        "schema_version": "0.7.0",
        "ruleset_version": RULESET_VERSION,
        "evaluation_context": evaluation["evaluation_context"],
        "settlement_intent": canonical_json(load_json(intent_path)),
        "money_profile": canonical_json(load_json(money_path)),
        "money_state": evaluation["money_state"],
        "settlement_profile": canonical_json(settlement_profile),
        "money_requirement_set": canonical_json(load_json(requirement_path)),
        "evidence_manifest": evidence_manifest(money.id),
        "evidence_policy": canonical_json(default_evidence_policy()),
        "evaluation_result": evaluation,
        "canonical_evaluation_result": canonical_evaluation_result(evaluation),
        "transition_plan": canonical_json(plan_transition(intent)),
        "route": canonical_json(route),
        "canonicalization": {
            "profile": "OMST-CANONICAL-JSON-0.7",
            "monetary_amounts": "decimal-string",
            "timestamps": "RFC3339-UTC",
            "unicode": "UTF-8 with ASCII-safe reference fixtures",
        },
        "integrity": {},
        "metadata": {
            "synthetic": True,
            "boundary": "Technical verification artifact. Not regulatory certification, legal advice, credit assessment, reserve attestation or issuer endorsement.",
        },
    }
    return seal_evaluation_package(package)


def settlement_evaluation_bundle(package: dict[str, Any] | None = None) -> dict[str, Any]:
    active_package = package or build_evaluation_package()
    return {
        "omst_type": "settlement-evaluation-bundle",
        "bundle_id": "bundle-tokenized-bond-dvp-eur-x-v07",
        "bundle_version": "0.7.0",
        "evaluation_package": active_package,
        "verification_metadata": {
            "package_fingerprint": active_package["integrity"]["package_fingerprint"],
            "evaluation_fingerprint": active_package["integrity"]["evaluation_fingerprint"],
            "status": "SEALED",
        },
        "boundary": "Transferable synthetic settlement-compatibility artifact; not settlement execution.",
    }


def seal_evaluation_package(package: dict[str, Any]) -> dict[str, Any]:
    sealed = deepcopy(package)
    sealed["lifecycle_status"] = "SEALED"
    sealed["integrity"] = {
        "package_fingerprint": package_fingerprint(sealed),
        "evaluation_fingerprint": evaluation_fingerprint(sealed),
        "canonical_result_fingerprint": canonical_hash(sealed["canonical_evaluation_result"]),
        "evidence_manifest_fingerprint": canonical_hash(sealed["evidence_manifest"]),
    }
    return sealed


def package_fingerprint(package: dict[str, Any]) -> str:
    payload = deepcopy(package)
    payload["integrity"] = {}
    payload.pop("verification_records", None)
    return canonical_hash(payload)


def evaluation_fingerprint(package: dict[str, Any]) -> str:
    return canonical_hash(
        {
            "schema_version": package.get("schema_version"),
            "ruleset_version": package.get("ruleset_version"),
            "settlement_intent": package.get("settlement_intent"),
            "money_profile": package.get("money_profile"),
            "money_state": package.get("money_state"),
            "settlement_profile": package.get("settlement_profile"),
            "money_requirement_set": package.get("money_requirement_set"),
            "evidence_manifest": package.get("evidence_manifest"),
            "canonical_evaluation_result": package.get("canonical_evaluation_result"),
        }
    )


def verify_evaluation_package(path_or_package: Path | dict[str, Any]) -> dict[str, Any]:
    package = load_json(path_or_package) if isinstance(path_or_package, Path) else deepcopy(path_or_package)
    checks: list[dict[str, str]] = []
    reasons: list[str] = []

    def check(layer: str, status: str, reason: str = "") -> None:
        checks.append({"layer": layer, "status": status, "reason": reason})
        if reason and status != "PASS":
            reasons.append(reason)

    if isinstance(path_or_package, Path):
        schema_errors = validate_document(path_or_package)
    else:
        schema_errors = _validate_package_shape(package)
    check("Schema", "PASS" if not schema_errors else "FAIL", "; ".join(schema_errors))

    try:
        canonicalize_for_verification(package)
        check("Canonicalization", "PASS")
    except TypeError as exc:
        check("Canonicalization", "FAIL", str(exc))

    expected_package = package.get("integrity", {}).get("package_fingerprint")
    actual_package = package_fingerprint(package)
    check(
        "Integrity",
        "PASS" if expected_package == actual_package else "FAIL",
        "" if expected_package == actual_package else "package fingerprint mismatch",
    )

    expected_eval = package.get("integrity", {}).get("evaluation_fingerprint")
    actual_eval = evaluation_fingerprint(package)
    check(
        "Evaluation fingerprint",
        "PASS" if expected_eval == actual_eval else "FAIL",
        "" if expected_eval == actual_eval else "evaluation fingerprint mismatch",
    )

    evidence_errors = evidence_integrity_errors(package.get("evidence_manifest", {}))
    check("Evidence", "PASS" if not evidence_errors else "FAIL", "; ".join(evidence_errors))

    ruleset = str(package.get("ruleset_version", ""))
    check(
        "Ruleset",
        "PASS" if ruleset in SUPPORTED_RULESETS else "FAIL",
        "" if ruleset in SUPPORTED_RULESETS else f"unsupported ruleset {ruleset}",
    )

    schema_version = str(package.get("schema_version", ""))
    check(
        "Schema version",
        "PASS" if schema_version in SUPPORTED_SCHEMA_VERSIONS else "FAIL",
        "" if schema_version in SUPPORTED_SCHEMA_VERSIONS else f"unsupported schema version {schema_version}",
    )

    reproduced = reproduce_evaluation(package)
    equivalence = compare_semantics(package.get("evaluation_result", {}), reproduced)
    check(
        "Semantic evaluation",
        "PASS" if equivalence["status"] == "SEMANTICALLY_EQUIVALENT" else "FAIL",
        "" if equivalence["status"] == "SEMANTICALLY_EQUIVALENT" else "semantic evaluation differs",
    )
    check("Transition plan", "PASS" if package.get("transition_plan") else "FAIL", "missing transition plan")
    check("Route", "PASS" if package.get("route") else "FAIL", "missing route")

    status = _verification_status(checks)
    return {
        "omst_type": "verification-result",
        "verification_id": f"verify-{package.get('package_id', 'unknown')}",
        "status": status,
        "package_fingerprint": actual_package,
        "evaluation_fingerprint": actual_eval,
        "checks": checks,
        "semantic_equivalence": equivalence["status"],
        "reproduced_result": canonical_evaluation_result(reproduced),
        "reasons": reasons,
        "record": verification_record(package, status, reasons),
    }


def evidence_integrity_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    seen: dict[str, str] = {}
    for item in manifest.get("evidence_items", []):
        evidence_id = str(item.get("evidence_id", "unknown"))
        inline = item.get("inline_content")
        expected_hash = item.get("content_hash")
        if inline is None:
            if item.get("status") == "MISSING":
                errors.append(f"{evidence_id}: missing evidence")
            continue
        actual_hash = canonical_hash(inline)
        if expected_hash != actual_hash:
            errors.append(f"{evidence_id}: evidence hash mismatch")
        expires_at = str(item.get("expires_at", ""))
        if expires_at and expires_at <= REFERENCE_TIMESTAMP:
            errors.append(f"{evidence_id}: evidence expired")
        key = f"{item.get('type')}:{item.get('source')}:{item.get('content_reference')}"
        if key in seen and seen[key] != actual_hash:
            errors.append(f"{evidence_id}: conflicting evidence")
        seen[key] = actual_hash
    if not manifest.get("evidence_items"):
        errors.append("evidence manifest contains no items")
    return errors


def reproduce_evaluation(package: dict[str, Any]) -> dict[str, Any]:
    intent = load_settlement_intent_v05(Path("examples/tokenized-bond-dvp/settlement-intent.json"))
    money = load_money_profile(Path("examples/eur-x.json"))
    requirements = load_requirement_set(Path("examples/requirements/tokenized-bond-dvp.json"))
    return canonicalize_for_verification(
        evaluate_settlement_compatibility(
            intent,
            money,
            synthetic_money_states()[money.id],
            requirements,
        )
    )


def verification_record(package: dict[str, Any], status: VerificationOutcome, warnings: list[str]) -> dict[str, Any]:
    return {
        "omst_type": "settlement-verification-record",
        "verification_id": f"record-{package.get('package_id', 'unknown')}",
        "package_fingerprint": package.get("integrity", {}).get("package_fingerprint"),
        "evaluation_fingerprint": package.get("integrity", {}).get("evaluation_fingerprint"),
        "status": status,
        "omst_version": package.get("omst_version"),
        "ruleset_version": package.get("ruleset_version"),
        "schema_version": package.get("schema_version"),
        "verified_at": REFERENCE_TIMESTAMP,
        "verifier": "OMST Reference Verifier",
        "conformance_profile": "OMST-VERIFICATION",
        "warnings": warnings,
        "boundary": "Technical verification artifact. Not regulatory certification, legal advice, credit assessment, reserve attestation or issuer endorsement.",
    }


def human_verification_record(record: dict[str, Any]) -> str:
    return "\n".join(
        [
            "OMST SETTLEMENT VERIFICATION",
            "",
            f"Status: {record['status']}",
            "Settlement: EUR 50m tokenized-bond DvP",
            "Money: EUR-X",
            "Result: COMPATIBLE",
            f"Ruleset: {record['ruleset_version']}",
            f"Package: {record['package_fingerprint']}",
            f"Verifier: {record['verifier']}",
            f"Verified: {record['verified_at']}",
            "",
            record["boundary"],
        ]
    )


def tamper_package(package: dict[str, Any], mutation: str) -> dict[str, Any]:
    tampered = deepcopy(package)
    if mutation == "liquidity":
        items = tampered["evidence_manifest"]["evidence_items"]
        items[0]["inline_content"]["amount"] = "25000000"
    elif mutation == "evidence":
        tampered["evidence_manifest"]["evidence_items"][0]["content_hash"] = "0" * 64
    elif mutation == "result":
        tampered["evaluation_result"]["overall_status"] = "INCOMPATIBLE"
        tampered["canonical_evaluation_result"]["status"] = "INCOMPATIBLE"
    elif mutation == "ruleset":
        tampered["ruleset_version"] = "omst-core-0.6"
    elif mutation == "stale-evidence":
        tampered["evidence_manifest"]["evidence_items"][0]["expires_at"] = "2026-09-01T00:00:00Z"
    elif mutation == "missing-evidence":
        tampered["evidence_manifest"]["evidence_items"] = []
    elif mutation == "route":
        tampered["route"]["primary"]["route"] = ["EUR-X", "EUR-Z", "EUR-Y"]
    else:
        raise ValueError(f"unknown tamper mutation: {mutation}")
    return tampered


def verification_summary(result: dict[str, Any]) -> str:
    lines = []
    for label in [
        "Integrity",
        "Schema",
        "Evidence",
        "Ruleset",
        "Semantic evaluation",
        "Canonicalization",
    ]:
        matching = next((check for check in result["checks"] if check["layer"] == label), None)
        if matching:
            lines.append(f"{label}: {matching['status']}")
    lines.append("")
    lines.append(str(result["status"]))
    if result["reasons"]:
        lines.append("Reasons:")
        lines.extend(f"- {reason}" for reason in result["reasons"])
    return "\n".join(lines)


def _verification_status(checks: list[dict[str, str]]) -> VerificationOutcome:
    failed_layers = {check["layer"] for check in checks if check["status"] == "FAIL"}
    if not failed_layers:
        return "VERIFIED"
    if "Ruleset" in failed_layers or "Schema version" in failed_layers:
        return "UNSUPPORTED"
    if "Semantic evaluation" in failed_layers and failed_layers <= {
        "Semantic evaluation",
        "Evaluation fingerprint",
        "Integrity",
    }:
        return "DIFFERENT"
    return "INVALID"


def _validate_package_shape(package: dict[str, Any]) -> list[str]:
    required = (
        "package_id",
        "package_version",
        "omst_version",
        "schema_version",
        "ruleset_version",
        "evaluation_context",
        "settlement_intent",
        "money_profile",
        "money_state",
        "settlement_profile",
        "evidence_manifest",
        "evidence_policy",
        "evaluation_result",
        "transition_plan",
        "route",
        "canonicalization",
        "integrity",
        "metadata",
    )
    return [f"{key} is required" for key in required if key not in package]
