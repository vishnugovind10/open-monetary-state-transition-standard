from decimal import Decimal
from pathlib import Path

from omst.interoperability import (
    adapter_mapping,
    fallback_routes,
    profile_fingerprint,
    settlement_response,
    v06_manifest,
)


def test_profile_fingerprint_is_deterministic_and_ignores_existing_fingerprint():
    profile = {"profile_id": "x", "currency": "EUR", "profile_fingerprint": "old"}
    assert profile_fingerprint(profile) == profile_fingerprint({**profile, "profile_fingerprint": "new"})


def test_settlement_response_contains_portable_exchange_parts():
    response = settlement_response(
        intent_path=Path("examples/tokenized-bond-dvp/settlement-intent.json"),
        money_path=Path("examples/eur-x.json"),
        settlement_profile_path=Path("examples/settlement-networks/network-a.json"),
    )
    assert response.status == "COMPATIBLE"
    assert "effective_liquidity" in response.accepted_requirements
    assert response.route["snapshot_id"] == "graph-snapshot-v06-tokenized-bond-dvp"


def test_adapter_mapping_classifies_lossiness():
    mapping = adapter_mapping("iso20022")
    assert mapping.lossiness == "APPROXIMATED"
    assert mapping.supported_fields["amount"] == "EXACT"


def test_fallback_routes_are_reproducible_from_snapshot():
    routes = fallback_routes("EUR-X", "EUR-Y", Decimal(50000000))
    assert routes["snapshot_id"] == "graph-snapshot-v06-tokenized-bond-dvp"
    assert routes["primary"]["status"] == "ROUTE_FOUND"
    assert routes["fallback"]["type"] == "FALLBACK"


def test_manifest_declares_interoperability_layer():
    manifest = v06_manifest()
    assert manifest["omst_version"] == "0.6.0"
    assert "interoperability" in manifest["profiles"]
