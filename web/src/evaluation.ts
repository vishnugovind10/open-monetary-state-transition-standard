import { routeEdges } from "./data";
import type { Instrument, SettlementVerdict, StressScenario } from "./types";

const settlementRequirements = {
  acceptedFinality: new Set(["qualified", "deterministic", "central-bank-final"]),
  requiredAvailability: "24_7",
  maximumLatencySeconds: 60,
  minimumLiquidity: 50_000_000,
  maximumEvidenceAgeSeconds: 60
};

export function evaluateSettlement(
  source: Instrument,
  target: Instrument,
  amount: number,
  scenario: StressScenario
): SettlementVerdict {
  const liquidityFloor = Math.min(source.liquidity, target.liquidity);
  const stressedLiquidity = scenario.id === "liquidity-shock" ? liquidityFloor - 30 : liquidityFloor;
  const latency =
    (source.code === target.code ? source.latencySeconds : source.latencySeconds + target.latencySeconds) +
    (scenario.impact === "High" ? 120 : 0);
  const route = source.code === target.code
    ? [source.code]
    : routeEdges.some((edge) => edge.from === source.code && edge.to === target.code)
    ? [source.code, target.code]
    : [source.code, "EUR-Y", target.code];

  const reasons: string[] = [];
  if (source.status === "restricted") {
    reasons.push("ACCESS_RESTRICTED");
  }
  if (!source.atomicSettlement) {
    reasons.push("ATOMICITY_UNAVAILABLE");
  }
  if (!settlementRequirements.acceptedFinality.has(source.finality)) {
    reasons.push("FINALITY_MISMATCH");
  }
  if (source.settlementAvailability !== settlementRequirements.requiredAvailability) {
    reasons.push("AVAILABILITY_MISMATCH");
  }
  if (source.latencySeconds > settlementRequirements.maximumLatencySeconds) {
    reasons.push("LATENCY_REQUIREMENT_UNMET");
  }
  if (amount > source.liquidity * 1_000_000 || amount > stressedLiquidity * 1_000_000) {
    reasons.push("LIQUIDITY_INSUFFICIENT");
  }

  if (reasons.length) {
    return {
      status: "INCOMPATIBLE",
      reason: "Mandatory atomicity, finality, availability, latency and liquidity requirements are not satisfied.",
      reasons,
      confidence: "high",
      latencySeconds: latency,
      costBps: 22,
      route
    };
  }

  if (source.evidenceAgeSeconds > settlementRequirements.maximumEvidenceAgeSeconds) {
    return {
      status: "CONDITIONALLY_COMPATIBLE",
      reason: "Mandatory settlement requirements pass, but liquidity evidence is stale under the v0.6 evidence policy.",
      reasons: ["LIQUIDITY_EVIDENCE_STALE"],
      confidence: "medium",
      latencySeconds: latency,
      costBps: 12,
      route
    };
  }

  if (amount > stressedLiquidity * 1_000_000) {
    return {
      status: "CONDITIONALLY_COMPATIBLE",
      reason: "Required liquidity exceeds stressed available liquidity for this transition.",
      reasons: ["LIQUIDITY_REQUIREMENT_CONDITIONAL"],
      confidence: "medium",
      latencySeconds: latency,
      costBps: 18,
      route
    };
  }

  return {
    status: scenario.impact === "High" ? "CONDITIONALLY_COMPATIBLE" : "COMPATIBLE",
    reason:
      scenario.impact === "High"
        ? "Settlement remains routable, but stressed finality and liquidity assumptions apply."
        : "State, liquidity, route and finality constraints are compatible for this context.",
    reasons: scenario.impact === "High" ? ["STRESS_CONTEXT_ASSUMPTION"] : [],
    confidence: scenario.impact === "High" ? "medium" : "high",
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
