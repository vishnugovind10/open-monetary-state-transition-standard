from decimal import Decimal
from typing import Any

from .enums import CapabilityStatus, CapabilityType
from .graph import MoneyGraph
from .models import LiquidityProfile, MoneyCapability, MoneyProfile, RouteEdge, TransactionContext


def synthetic_profiles() -> dict[str, MoneyProfile]:
    def make_profile(
        instrument_id: str,
        name: str,
        issuer: str,
        layer: str = "m1_reference",
        settlement_profile: dict[str, Any] | None = None,
    ) -> MoneyProfile:
        return MoneyProfile(
            id=instrument_id,
            name=name,
            currency="EUR",
            issuer=issuer,
            claim_type="digital_money",
            monetary_layer_reference=layer,
            functions={
                "payment": "supported",
                "settlement": "supported",
                "redemption": "supported",
                "collateral": "conditional",
            },
            settlement_profile=settlement_profile
            or {"finality_type": "qualified", "availability": "24_7"},
            redemption_profile={"at_par": True, "latency_seconds": 30},
            transfer_profile={"transferable": True},
            access_profile={"institutional": True},
            control_profile={"freeze_possible": True},
            network_profile={"network": "synthetic-ledger"},
            evidence=[],
            capabilities=[
                MoneyCapability(CapabilityType.PAYMENT, CapabilityStatus.SUPPORTED),
                MoneyCapability(CapabilityType.SETTLEMENT, CapabilityStatus.SUPPORTED),
                MoneyCapability(CapabilityType.REDEMPTION, CapabilityStatus.SUPPORTED),
                MoneyCapability(CapabilityType.DELIVERY_VERSUS_PAYMENT, CapabilityStatus.CONDITIONAL),
                MoneyCapability(CapabilityType.ATOMIC_SETTLEMENT, CapabilityStatus.CONDITIONAL),
            ],
        )

    return {
        "EUR-X": make_profile("EUR-X", "Synthetic EUR Money X", "Synthetic Issuer X"),
        "EUR-Y": make_profile("EUR-Y", "Synthetic EUR Money Y", "Synthetic Issuer Y"),
        "EUR-Z": make_profile(
            "EUR-Z",
            "Synthetic EUR Money Z",
            "Synthetic Issuer Z",
            settlement_profile={"finality_type": "probabilistic", "availability": "business_hours"},
        ),
        "CBM": make_profile(
            "CBM",
            "Synthetic Central Bank Money Anchor",
            "Synthetic Central Bank",
            "m0_reference",
            {"finality_type": "deterministic", "availability": "TARGET_window"},
        ),
    }

def synthetic_liquidity(instrument: str) -> LiquidityProfile:
    values = {"EUR-X": "120000000", "EUR-Y": "90000000", "EUR-Z": "25000000", "CBM": "500000000"}
    ready = Decimal(values.get(instrument, "0"))
    return LiquidityProfile(instrument, ready * 2, ready, ready, ready, ready, "30d", [])

def synthetic_graph() -> MoneyGraph:
    return MoneyGraph([
        RouteEdge("EUR-X", "CBM", Decimal("1.2"), 20, Decimal(90000000), "qualified", "available", {"synthetic": True}),
        RouteEdge("CBM", "EUR-Y", Decimal("1.1"), 25, Decimal(150000000), "deterministic", "available", {"synthetic": True}),
        RouteEdge("EUR-X", "EUR-Z", Decimal("0.2"), 80, Decimal(25000000), "probabilistic", "available", {"synthetic": True}),
        RouteEdge("EUR-Z", "EUR-Y", Decimal("0.2"), 90, Decimal(25000000), "probabilistic", "available", {"synthetic": True}),
    ])

def context_by_name(name: str) -> TransactionContext:
    if name in {"tokenized-dvp", "tokenised-dvp"}:
        return TransactionContext(name="tokenized-dvp", required_finality="qualified", max_latency_seconds=60, required_functions=("settlement",))
    return TransactionContext(name=name, required_finality="qualified")
