from omst.cli.main import main


def test_validate_examples():
    assert main(["validate", "examples"]) == 0

def test_route_cli(capsys):
    assert main(["route", "--from", "EUR-X", "--to", "EUR-Y", "--amount", "50000000", "--context", "tokenized-dvp"]) == 0
    assert "ROUTE_FOUND" in capsys.readouterr().out

def test_transition_cli(capsys):
    assert main(["transition", "--from", "EUR-X:AVAILABLE", "--to", "EUR-Y:FINAL", "--amount", "50000000"]) == 0
    assert "PRESERVED" in capsys.readouterr().out

def test_simulate_cli(capsys):
    assert main(["simulate", "redemption-shock"]) == 0
    assert "redemption demand" in capsys.readouterr().out


def test_equivalence_cli(capsys):
    assert main(["equivalence", "EUR-X", "EUR-Z", "--context", "tokenized-dvp"]) == 0
    assert "FUNCTIONALLY_EQUIVALENT" in capsys.readouterr().out


def test_profile_cli(capsys):
    assert main(["profile", "examples/eur-x.json"]) == 0
    assert "EUR-X" in capsys.readouterr().out


def test_capability_cli(capsys):
    assert main(["capability", "EUR-X"]) == 0
    assert "ATOMIC_SETTLEMENT" in capsys.readouterr().out


def test_evaluate_settlement_cli(capsys):
    assert main(["evaluate-settlement", "examples/tokenized-bond-dvp/"]) == 0
    assert "COMPATIBLE" in capsys.readouterr().out


def test_v05_evaluate_settlement_cli_with_money(capsys):
    assert (
        main(
            [
                "evaluate-settlement",
                "examples/tokenized-bond-dvp/settlement-intent.json",
                "--money",
                "examples/eur-z.json",
            ]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "INCOMPATIBLE" in output
    assert "FINALITY_MISMATCH" in output


def test_requirement_cli(capsys):
    assert main(["requirement", "examples/requirements/tokenized-bond-dvp.json"]) == 0
    assert "TOKENIZED_BOND_DVP_EUR" in capsys.readouterr().out


def test_conformance_cli(capsys):
    assert main(["conformance"]) == 0
    output = capsys.readouterr().out
    assert "OMST-INTEROPERABILITY" in output
    assert "PASS" in output


def test_conformance_profile_cli(capsys):
    assert main(["conformance", "--profile", "OMST-INTEROPERABILITY"]) == 0
    output = capsys.readouterr().out
    assert "OMST-INTEROPERABILITY" in output
    assert "PASS" in output


def test_explain_cli(capsys):
    assert main(["explain", "evaluation.json"]) == 0
    output = capsys.readouterr().out
    assert "Evaluation:" in output
    assert "Synthetic" in output


def test_plan_cli(capsys):
    assert main(["plan", "examples/tokenized-bond-dvp/"]) == 0
    assert "plan-tokenized-bond-dvp" in capsys.readouterr().out


def test_graph_mermaid_cli(capsys):
    assert main(["graph", "--format", "mermaid"]) == 0
    assert "flowchart LR" in capsys.readouterr().out


def test_stress_cli(capsys):
    assert main(["stress", "--scenario", "liquidity-shock"]) == 0
    assert "liquidity-shock" in capsys.readouterr().out


def test_v06_profile_validate_cli(capsys):
    assert main(["profile", "validate", "examples/profiles/money/eur-x.v06.json"]) == 0
    output = capsys.readouterr().out
    assert "profile_fingerprint" in output
    assert "VALID" in output


def test_v06_settlement_profile_cli(capsys):
    assert main(["settlement-profile", "examples/settlement-networks/network-a.json"]) == 0
    assert "settlement-network-a" in capsys.readouterr().out


def test_v06_adapter_cli(capsys):
    assert main(["adapter", "iso20022"]) == 0
    output = capsys.readouterr().out
    assert "ISO 20022" in output
    assert "APPROXIMATED" in output


def test_v06_exchange_cli(capsys):
    assert (
        main(
            [
                "exchange",
                "--intent",
                "examples/tokenized-bond-dvp/settlement-intent.json",
                "--money",
                "examples/eur-x.json",
                "--settlement",
                "examples/settlement-networks/network-a.json",
            ]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "request-tokenized-bond-dvp-eur-50m" in output
    assert "COMPATIBLE" in output


def test_v06_manifest_and_discovery_cli(capsys):
    assert main(["manifest"]) == 0
    assert "0.7.0" in capsys.readouterr().out
    assert main(["discovery"]) == 0
    assert "experimental" in capsys.readouterr().out


def test_v06_api_cli(capsys):
    assert main(["api", "settlement/response"]) == 0
    output = capsys.readouterr().out
    assert "portable" not in output
    assert "COMPATIBLE" in output


def test_v07_package_create_cli(capsys):
    assert main(["package", "create"]) == 0
    output = capsys.readouterr().out
    assert "evaluation-package" in output
    assert "package_fingerprint" in output


def test_v07_verify_cli(capsys):
    assert main(["verify", "examples/verification/valid-package.json"]) == 0
    output = capsys.readouterr().out
    assert "VERIFIED" in output
    assert "Semantic evaluation: PASS" in output


def test_v07_verify_human_cli(capsys):
    assert main(["verify", "examples/verification/valid-package.json", "--human"]) == 0
    output = capsys.readouterr().out
    assert "OMST SETTLEMENT VERIFICATION" in output
    assert "Not regulatory certification" in output


def test_v07_tamper_cli(capsys):
    assert main(["tamper", "evidence", "examples/verification/valid-package.json"]) == 0
    output = capsys.readouterr().out
    assert '"content_hash": "0000000000000000000000000000000000000000000000000000000000000000"' in output


def test_v07_bundle_cli(capsys):
    assert main(["bundle", "create"]) == 0
    assert "settlement-evaluation-bundle" in capsys.readouterr().out
    assert main(["bundle", "verify", "examples/verification/settlement-evaluation-bundle.json"]) == 0
    assert "VERIFIED" in capsys.readouterr().out


def test_v07_api_verification_cli(capsys):
    assert main(["api", "verification/verify"]) == 0
    output = capsys.readouterr().out
    assert "verification-result" in output
    assert "VERIFIED" in output
