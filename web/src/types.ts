export type Status = "active" | "restricted" | "pilot";

export type Instrument = {
  code: string;
  name: string;
  type: string;
  status: Status;
  jurisdiction: string;
  finality: string;
  liquidity: number;
  latencySeconds: number;
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
