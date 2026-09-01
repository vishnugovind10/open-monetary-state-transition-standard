from decimal import Decimal

import pytest

from omst.cost import transition_cost
from omst.enums import MoneyState
from omst.fragmentation import monetary_fragmentation_index
from omst.state import can_transition
from omst.velocity import settlement_velocity


@pytest.mark.parametrize("source,target,expected", [
    (MoneyState.ISSUED, MoneyState.AVAILABLE, True),
    (MoneyState.AVAILABLE, MoneyState.RESERVED, True),
    (MoneyState.AVAILABLE, MoneyState.TRANSFERRING, True),
    (MoneyState.AVAILABLE, MoneyState.REDEEMING, True),
    (MoneyState.AVAILABLE, MoneyState.CONVERTING, True),
    (MoneyState.RESERVED, MoneyState.SETTLING, True),
    (MoneyState.TRANSFERRING, MoneyState.SETTLING, True),
    (MoneyState.CONVERTING, MoneyState.SETTLING, True),
    (MoneyState.REDEEMING, MoneyState.FINAL, True),
    (MoneyState.SETTLING, MoneyState.FINAL, True),
    (MoneyState.SETTLING, MoneyState.FAILED, True),
    (MoneyState.AVAILABLE, MoneyState.ENCUMBERED, True),
    (MoneyState.ENCUMBERED, MoneyState.AVAILABLE, True),
    (MoneyState.AVAILABLE, MoneyState.FROZEN, True),
    (MoneyState.FINAL, MoneyState.AVAILABLE, False),
    (MoneyState.UNKNOWN, MoneyState.AVAILABLE, False),
    (MoneyState.AVAILABLE, MoneyState.FINAL, False),
    (MoneyState.FAILED, MoneyState.FINAL, False),
    (MoneyState.LOCKED, MoneyState.AVAILABLE, True),
    (MoneyState.FROZEN, MoneyState.AVAILABLE, True),
])
def test_state_machine(source, target, expected):
    assert can_transition(source, target) is expected

@pytest.mark.parametrize("settled,balance,expected", [(100,10,10),(0,10,0),(5,2,Decimal("2.5"))]*15)
def test_settlement_velocity(settled, balance, expected):
    assert settlement_velocity(Decimal(settled), Decimal(balance)) == Decimal(expected)

@pytest.mark.parametrize("q,l", [(1,10),(10,100),(50,100),(999,1000)]*8)
def test_transition_cost_domain(q, l):
    assert transition_cost(Decimal(q), Decimal(l)) >= 0

@pytest.mark.parametrize("q,l", [(10,10),(11,10),(-1,10),(1,0)]*5)
def test_transition_cost_rejects_invalid_domain(q, l):
    with pytest.raises(ValueError):
        transition_cost(Decimal(q), Decimal(l))

def test_fragmentation_index():
    assert monetary_fragmentation_index([(Decimal("0.5"), Decimal("0.2")), (Decimal("0.5"), Decimal("0.4"))]) == Decimal("0.30")
