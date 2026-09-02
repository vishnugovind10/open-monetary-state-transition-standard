import type { Instrument, RouteEdge, StressScenario, TamperCase, VerificationCheck } from "./types";

export const instruments: Instrument[] = [
  {
    code: "EUR-X",
    name: "Synthetic regulated e-money",
    type: "Digital money",
    status: "active",
    jurisdiction: "EU",
    finality: "qualified",
    settlementAvailability: "24_7",
    atomicSettlement: true,
    liquidity: 95,
    latencySeconds: 45,
    evidenceAgeSeconds: 30,
    capabilities: ["transfer", "redeem", "programmable-controls", "dvp-cash-leg"]
  },
  {
    code: "EUR-Y",
    name: "Synthetic tokenized deposit",
    type: "Bank claim",
    status: "active",
    jurisdiction: "EU",
    finality: "qualified",
    settlementAvailability: "24_7",
    atomicSettlement: true,
    liquidity: 88,
    latencySeconds: 55,
    evidenceAgeSeconds: 3_600,
    capabilities: ["transfer", "redeem", "wholesale-settlement"]
  },
  {
    code: "EUR-Z",
    name: "Synthetic settlement token",
    type: "Settlement asset",
    status: "pilot",
    jurisdiction: "EU",
    finality: "probabilistic",
    settlementAvailability: "business_hours",
    atomicSettlement: false,
    liquidity: 25,
    latencySeconds: 120,
    evidenceAgeSeconds: 45,
    capabilities: ["transfer", "programmable-controls"]
  },
  {
    code: "CBM",
    name: "Synthetic central bank money",
    type: "Central bank",
    status: "active",
    jurisdiction: "EU",
    finality: "central-bank-final",
    settlementAvailability: "24_7",
    atomicSettlement: true,
    liquidity: 100,
    latencySeconds: 15,
    evidenceAgeSeconds: 30,
    capabilities: ["settlement", "reserve-transfer", "irrevocable-finality"]
  },
  {
    code: "MMF-A",
    name: "Synthetic money-market fund unit",
    type: "Fund unit",
    status: "restricted",
    jurisdiction: "EU",
    finality: "redeemable-claim",
    settlementAvailability: "business_hours",
    atomicSettlement: false,
    liquidity: 61,
    latencySeconds: 900,
    evidenceAgeSeconds: 86_500,
    capabilities: ["redeem", "collateral"]
  }
];

export const routeEdges: RouteEdge[] = [
  { from: "EUR-X", to: "EUR-Y", strength: "high" },
  { from: "EUR-Y", to: "CBM", strength: "high" },
  { from: "EUR-X", to: "EUR-Z", strength: "medium" },
  { from: "EUR-Z", to: "CBM", strength: "medium" },
  { from: "MMF-A", to: "EUR-Y", strength: "low" },
  { from: "EUR-X", to: "CBM", strength: "high" }
];

export const stressScenarios: StressScenario[] = [
  { id: "baseline", name: "Baseline", condition: "Normal conditions", impact: "Low", equivalenceRate: 100 },
  { id: "network-congestion", name: "Network Congestion", condition: "95th percentile latency", impact: "Medium", equivalenceRate: 99.62 },
  { id: "liquidity-shock", name: "Liquidity Shock", condition: "-30% available liquidity", impact: "High", equivalenceRate: 97.18 },
  { id: "jurisdiction-outage", name: "Jurisdiction Outage", condition: "One settlement domain offline", impact: "High", equivalenceRate: 92.41 }
];

export const conformanceRows = [
  ["EUR-X", "pass", "pass", "pass", "pass", "pass", "Compliant"],
  ["EUR-Y", "pass", "pass", "pass", "pass", "pass", "Compliant"],
  ["EUR-Z", "pass", "warn", "pass", "warn", "warn", "Partial"],
  ["CBM", "pass", "pass", "pass", "pass", "pass", "Compliant"],
  ["MMF-A", "pass", "warn", "warn", "pass", "warn", "Partial"]
];

export const verificationChecks: VerificationCheck[] = [
  { layer: "Schema", status: "PASS", detail: "evaluation-package v0.7" },
  { layer: "Canonicalization", status: "PASS", detail: "OMST-CANONICAL-JSON-0.7" },
  { layer: "Integrity", status: "PASS", detail: "package and evaluation fingerprints match" },
  { layer: "Evidence", status: "PASS", detail: "liquidity evidence hash and expiry valid" },
  { layer: "Ruleset", status: "PASS", detail: "omst-core-0.7 supported" },
  { layer: "Semantic parity", status: "PASS", detail: "reproduced result is equivalent" }
];

export const tamperCases: TamperCase[] = [
  {
    id: "liquidity",
    label: "Liquidity",
    status: "INVALID",
    reason: "package fingerprint mismatch"
  },
  {
    id: "evidence",
    label: "Evidence",
    status: "INVALID",
    reason: "evidence hash mismatch"
  },
  {
    id: "result",
    label: "Result",
    status: "DIFFERENT",
    reason: "semantic evaluation differs"
  },
  {
    id: "ruleset",
    label: "Ruleset",
    status: "UNSUPPORTED",
    reason: "ruleset version is not supported"
  }
];
