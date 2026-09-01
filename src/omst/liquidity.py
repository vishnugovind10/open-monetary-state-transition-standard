from .models import LiquidityProfile


def effective_monetary_liquidity(profile: LiquidityProfile, function: str, venue: str, institution: str, timestamp: str) -> dict[str, object]:
    accessible = min(profile.settlement_ready_balance, profile.immediately_convertible_balance, profile.redemption_capacity)
    effective = min(accessible, profile.observed_market_depth) if profile.observed_market_depth > 0 else accessible
    return {
        "instrument": profile.instrument,
        "function": function,
        "venue": venue,
        "institution": institution,
        "timestamp": timestamp,
        "nominal_supply": profile.nominal_supply,
        "settlement_ready": profile.settlement_ready_balance,
        "accessible": accessible,
        "venue_compatible": True,
        "function_compatible": True,
        "effective_liquidity": effective,
        "method": "min(settlement_ready, immediately_convertible, redemption_capacity, observed_market_depth_when_available)",
    }
