from decimal import Decimal

import pytest

from omst.data import context_by_name, synthetic_graph
from omst.routing import route_money
from omst.simulation import simulate


@pytest.mark.parametrize("amount,status", [
    ("50000000","ROUTE_FOUND"),
    ("125000000","NO_ROUTE"),
    ("1","ROUTE_FOUND"),
    ("99999999","NO_ROUTE"),
    ("25000000","ROUTE_FOUND"),
]*4)
def test_routing_vectors(amount, status):
    assert route_money(synthetic_graph(), "EUR-X", "EUR-Y", Decimal(amount), context_by_name("tokenized-dvp"))["status"] == status

@pytest.mark.parametrize("scenario", ["normal","liquidity-shock","redemption-shock","velocity-shock","network-fragmentation","settlement-failure","finality-degradation","conversion-failure"])
def test_simulation_vectors(scenario):
    result = simulate(scenario)
    assert result["scenario"] == scenario
    assert result["synthetic"] is True
