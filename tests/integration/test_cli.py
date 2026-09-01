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
    assert "OMST-SETTLEMENT" in output
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
