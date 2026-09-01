from .enums import MoneyState

ALLOWED_TRANSITIONS: dict[MoneyState, set[MoneyState]] = {
    MoneyState.ISSUED: {MoneyState.AVAILABLE},
    MoneyState.AVAILABLE: {MoneyState.RESERVED, MoneyState.TRANSFERRING, MoneyState.REDEEMING, MoneyState.CONVERTING, MoneyState.ENCUMBERED, MoneyState.FROZEN},
    MoneyState.RESERVED: {MoneyState.SETTLING, MoneyState.AVAILABLE},
    MoneyState.TRANSFERRING: {MoneyState.SETTLING, MoneyState.FAILED},
    MoneyState.CONVERTING: {MoneyState.SETTLING, MoneyState.FAILED},
    MoneyState.REDEEMING: {MoneyState.FINAL, MoneyState.FAILED},
    MoneyState.SETTLING: {MoneyState.FINAL, MoneyState.FAILED},
    MoneyState.ENCUMBERED: {MoneyState.AVAILABLE},
    MoneyState.FROZEN: {MoneyState.AVAILABLE},
    MoneyState.LOCKED: {MoneyState.AVAILABLE},
    MoneyState.FINAL: set(),
    MoneyState.FAILED: set(),
    MoneyState.UNKNOWN: set(),
}

STATE_DEFINITIONS = {state.value: f"OMST machine-readable state `{state.value}`." for state in MoneyState}

def can_transition(source: MoneyState, target: MoneyState) -> bool:
    if source is MoneyState.UNKNOWN or target is MoneyState.UNKNOWN:
        return False
    return target in ALLOWED_TRANSITIONS[source]
