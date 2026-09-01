from .enums import EquivalenceStatus
from .models import MoneyProfile, TransactionContext


def monetary_equivalence(
    source: MoneyProfile, target: MoneyProfile, context: TransactionContext
) -> dict[str, object]:
    nominal = source.currency == target.currency
    functional = all(
        source.functions.get(function) in {"supported", "conditional"}
        and target.functions.get(function) in {"supported", "conditional"}
        for function in context.required_functions
    )
    settlement = (
        source.settlement_profile.get("finality_type") == target.settlement_profile.get("finality_type")
    )

    if nominal and functional and settlement:
        status = EquivalenceStatus.SETTLEMENT_EQUIVALENT
    elif nominal and functional:
        status = EquivalenceStatus.FUNCTIONALLY_EQUIVALENT
    elif nominal:
        status = EquivalenceStatus.NOMINALLY_EQUIVALENT
    else:
        status = EquivalenceStatus.NOT_EQUIVALENT

    return {
        "source": source.id,
        "target": target.id,
        "context": context.name,
        "nominally_equivalent": nominal,
        "functionally_equivalent": functional,
        "settlement_equivalent": settlement,
        "status": status.value,
    }
