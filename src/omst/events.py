from .enums import MoneyEventType, MoneyState
from .models import MoneyEvent
from .state import can_transition

EVENT_TARGETS: dict[MoneyEventType, MoneyState] = {
    MoneyEventType.CONVERSION_EXECUTED: MoneyState.SETTLING,
    MoneyEventType.CONVERSION_REQUESTED: MoneyState.CONVERTING,
    MoneyEventType.ENCUMBERED: MoneyState.ENCUMBERED,
    MoneyEventType.FROZEN: MoneyState.FROZEN,
    MoneyEventType.ISSUED: MoneyState.ISSUED,
    MoneyEventType.LOCKED: MoneyState.LOCKED,
    MoneyEventType.MINTED: MoneyState.AVAILABLE,
    MoneyEventType.REDEEMED: MoneyState.FINAL,
    MoneyEventType.REDEMPTION_REQUESTED: MoneyState.REDEEMING,
    MoneyEventType.RELEASED: MoneyState.AVAILABLE,
    MoneyEventType.RESERVED: MoneyState.RESERVED,
    MoneyEventType.SETTLEMENT_FAILED: MoneyState.FAILED,
    MoneyEventType.SETTLEMENT_FINAL: MoneyState.FINAL,
    MoneyEventType.SETTLEMENT_STARTED: MoneyState.SETTLING,
    MoneyEventType.TRANSFER_REQUESTED: MoneyState.TRANSFERRING,
    MoneyEventType.TRANSFERRED: MoneyState.SETTLING,
    MoneyEventType.UNFROZEN: MoneyState.AVAILABLE,
    MoneyEventType.UNLOCKED: MoneyState.AVAILABLE,
}


def validate_event_semantics(event: MoneyEvent) -> list[str]:
    errors: list[str] = []
    expected_target = EVENT_TARGETS.get(event.event_type)
    if expected_target and event.target_state != expected_target:
        errors.append("event target state does not match event type")
    if event.source_state != MoneyState.UNKNOWN and not can_transition(
        event.source_state, event.target_state
    ):
        errors.append("event state transition is not allowed by the OMST state machine")
    if event.quantity < 0:
        errors.append("event quantity cannot be negative")
    return errors
