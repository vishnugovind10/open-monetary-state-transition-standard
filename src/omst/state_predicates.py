from .models import CompositeMoneyState


def is_available(state: CompositeMoneyState) -> bool:
    return state.availability == "available" and state.operational_status == "operational"


def is_transferable(state: CompositeMoneyState) -> bool:
    return state.transferability == "transferable" and not is_frozen(state)


def is_settlement_ready(state: CompositeMoneyState) -> bool:
    return is_available(state) and state.settlement == "settlement_ready" and not is_locked(state)


def is_redeemable(state: CompositeMoneyState) -> bool:
    return state.redemption == "redeemable" and not is_frozen(state)


def is_final(state: CompositeMoneyState) -> bool:
    return state.finality in {"qualified", "deterministic", "central-bank-final"}


def is_locked(state: CompositeMoneyState) -> bool:
    return state.operational_status == "locked" or state.availability == "locked"


def is_frozen(state: CompositeMoneyState) -> bool:
    return state.operational_status == "frozen" or state.availability == "frozen"


def is_encumbered(state: CompositeMoneyState) -> bool:
    return state.encumbrance == "encumbered"
