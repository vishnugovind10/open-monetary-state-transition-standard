from copy import deepcopy
from pathlib import Path

from omst.compatibility import canonical_hash
from omst.verification import (
    build_evaluation_package,
    canonical_evaluation_result,
    compare_semantics,
    package_fingerprint,
    tamper_package,
    verify_evaluation_package,
)


def test_package_fingerprint_is_deterministic_and_ignores_integrity_fields():
    package = build_evaluation_package()
    changed = deepcopy(package)
    changed["integrity"]["package_fingerprint"] = "different"
    changed["integrity"]["evaluation_fingerprint"] = "different"

    assert package_fingerprint(package) == package_fingerprint(changed)


def test_canonicalization_hash_ignores_json_formatting():
    first = {"b": ["50000000.00", {"a": True}], "a": "EUR"}
    second = {"a": "EUR", "b": ["50000000.00", {"a": True}]}

    assert canonical_hash(first) == canonical_hash(second)


def test_material_property_change_changes_fingerprint():
    package = build_evaluation_package()
    changed = deepcopy(package)
    changed["money_profile"]["currency"] = "USD"

    assert package_fingerprint(package) != package_fingerprint(changed)


def test_valid_package_verifies():
    result = verify_evaluation_package(Path("examples/verification/valid-package.json"))

    assert result["status"] == "VERIFIED"
    assert result["semantic_equivalence"] == "SEMANTICALLY_EQUIVALENT"


def test_result_tamper_is_semantically_different():
    result = verify_evaluation_package(Path("examples/verification/tampered-result.json"))

    assert result["status"] == "DIFFERENT"
    assert "semantic evaluation differs" in result["reasons"]


def test_evidence_tamper_is_invalid():
    result = verify_evaluation_package(Path("examples/verification/tampered-evidence.json"))

    assert result["status"] == "INVALID"
    assert any("evidence hash mismatch" in reason for reason in result["reasons"])


def test_ruleset_downgrade_is_unsupported():
    result = verify_evaluation_package(Path("examples/verification/wrong-ruleset.json"))

    assert result["status"] == "UNSUPPORTED"
    assert any("unsupported ruleset" in reason for reason in result["reasons"])


def test_semantic_equivalence_ignores_non_semantic_metadata():
    package = build_evaluation_package()
    original = package["evaluation_result"]
    reproduced = deepcopy(original)
    reproduced["generated_at"] = "2099-01-01T00:00:00Z"

    assert compare_semantics(original, reproduced)["status"] == "SEMANTICALLY_EQUIVALENT"


def test_tamper_helper_changes_evidence_hash_status():
    package = build_evaluation_package()
    tampered = tamper_package(package, "evidence")

    assert tampered["evidence_manifest"]["evidence_items"][0]["content_hash"] == "0" * 64


def test_canonical_result_contains_evaluated_properties():
    result = canonical_evaluation_result(build_evaluation_package()["evaluation_result"])

    assert result["status"] == "COMPATIBLE"
    assert {item["property"] for item in result["evaluated_requirements"]} >= {
        "currency",
        "effective_liquidity",
        "finality",
    }
