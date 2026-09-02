export type Status = "active" | "restricted" | "pilot";

export type Instrument = {
  code: string;
  name: string;
  type: string;
  status: Status;
  jurisdiction: string;
  finality: string;
  settlementAvailability: "24_7" | "business_hours" | "offline";
  atomicSettlement: boolean;
  liquidity: number;
  latencySeconds: number;
  evidenceAgeSeconds: number;
  capabilities: string[];
};

export type RouteEdge = {
  from: string;
  to: string;
  strength: "high" | "medium" | "low";
};

export type StressScenario = {
  id: string;
  name: string;
  condition: string;
  impact: "Low" | "Medium" | "High";
  equivalenceRate: number;
};

export type SettlementVerdict = {
  status: "COMPATIBLE" | "CONDITIONALLY_COMPATIBLE" | "INCOMPATIBLE" | "UNKNOWN";
  reason: string;
  reasons: string[];
  confidence: "high" | "medium" | "low";
  latencySeconds: number;
  costBps: number;
  route: string[];
};

export type VerificationCheck = {
  layer: string;
  status: "PASS" | "WARN" | "FAIL";
  detail: string;
};

export type TamperCase = {
  id: string;
  label: string;
  status: "INVALID" | "DIFFERENT" | "UNSUPPORTED";
  reason: string;
};
