import { routeEdges } from "./data";
import type { Instrument, SettlementVerdict, StressScenario } from "./types";

export function evaluateSettlement(
  source: Instrument,
  target: Instrument,
  amount: number,
  scenario: StressScenario
): SettlementVerdict {
  const liquidityFloor = Math.min(source.liquidity, target.liquidity);
  const stressedLiquidity = scenario.id === "liquidity-shock" ? liquidityFloor - 30 : liquidityFloor;
  const latency = source.latencySeconds + target.latencySeconds + (scenario.impact === "High" ? 120 : 0);
  const route = routeEdges.some((edge) => edge.from === source.code && edge.to === target.code)
    ? [source.code, target.code]
    : [source.code, "EUR-Y", target.code];

  if (source.status === "restricted" || target.status === "restricted") {
    return {
      status: "BLOCKED",
      reason: "Instrument restrictions prevent unconditional settlement compatibility.",
      latencySeconds: latency,
      costBps: 0,
      route: []
    };
  }

  if (amount > stressedLiquidity * 1_000_000) {
    return {
      status: "CONSTRAINED",
      reason: "Required liquidity exceeds stressed available liquidity for this transition.",
      latencySeconds: latency,
      costBps: 18,
      route
    };
  }

  return {
    status: scenario.impact === "High" ? "CONSTRAINED" : "COMPATIBLE",
    reason:
      scenario.impact === "High"
        ? "Settlement remains routable, but stressed finality and liquidity assumptions apply."
        : "State, liquidity, route and finality constraints are compatible for this context.",
    latencySeconds: latency,
    costBps: scenario.impact === "Low" ? 6 : 12,
    route
  };
}

export function statusClass(value: string) {
  return `status status-${value.toLowerCase()}`;
}

export const formatAmount = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "EUR",
  maximumFractionDigits: 0
});
