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
