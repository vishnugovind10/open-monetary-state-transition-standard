export type CompatibilityStatus =
  | "COMPATIBLE"
  | "CONDITIONALLY_COMPATIBLE"
  | "INCOMPATIBLE"
  | "UNKNOWN";

export type ReasonCode =
  | "ATOMICITY_UNAVAILABLE"
  | "FINALITY_MISMATCH"
  | "AVAILABILITY_MISMATCH"
  | "LATENCY_REQUIREMENT_UNMET"
  | "LIQUIDITY_INSUFFICIENT"
  | "LIQUIDITY_EVIDENCE_STALE"
  | "UNKNOWN_STATE";

export type MoneyProfile = {
  id: string;
  finality: "qualified" | "contractual" | "probabilistic" | "central-bank-final";
  settlementAvailability: "24_7" | "business_hours" | "offline";
  atomicSettlement: boolean;
  effectiveLiquidity: number;
  settlementLatencySeconds: number;
  evidenceAgeSeconds: number;
};

export type SettlementProfile = {
  settlementProfileId: string;
  finality: MoneyProfile["finality"][];
  availability: "24_7" | "business_hours";
  atomicity: boolean;
  maximumLatencySeconds: number;
  minimumLiquidity: number;
  maximumEvidenceAgeSeconds: number;
};

export type RequirementSet = {
  minimumLiquidity: number;
  maximumLatencySeconds: number;
  requiredAvailability: "24_7" | "business_hours";
  acceptedFinality: MoneyProfile["finality"][];
  requireAtomicSettlement: boolean;
  maximumEvidenceAgeSeconds: number;
};

export type CompatibilityProfile = {
  moneyInstrument: string;
  overallStatus: CompatibilityStatus;
  reasonCodes: ReasonCode[];
};

const defaultRequirementSet: RequirementSet = {
  minimumLiquidity: 50_000_000,
  maximumLatencySeconds: 90,
  requiredAvailability: "24_7",
  acceptedFinality: ["qualified", "contractual", "central-bank-final"],
  requireAtomicSettlement: true,
  maximumEvidenceAgeSeconds: 86_400
};

const defaultSettlementProfile: SettlementProfile = {
  settlementProfileId: "settlement-network-a",
  finality: ["qualified", "contractual", "central-bank-final"],
  availability: "24_7",
  atomicity: true,
  maximumLatencySeconds: 90,
  minimumLiquidity: 50_000_000,
  maximumEvidenceAgeSeconds: 86_400
};

export function evaluateCompatibility(
  money: MoneyProfile,
  requirementSet: RequirementSet = defaultRequirementSet,
  settlementProfile: SettlementProfile = defaultSettlementProfile
): CompatibilityProfile {
  const reasonCodes: ReasonCode[] = [];

  if ((requirementSet.requireAtomicSettlement || settlementProfile.atomicity) && !money.atomicSettlement) {
    reasonCodes.push("ATOMICITY_UNAVAILABLE");
  }
  if (
    !requirementSet.acceptedFinality.includes(money.finality) ||
    !settlementProfile.finality.includes(money.finality)
  ) {
    reasonCodes.push("FINALITY_MISMATCH");
  }
  if (
    money.settlementAvailability !== requirementSet.requiredAvailability ||
    money.settlementAvailability !== settlementProfile.availability
  ) {
    reasonCodes.push("AVAILABILITY_MISMATCH");
  }
  if (
    money.settlementLatencySeconds > requirementSet.maximumLatencySeconds ||
    money.settlementLatencySeconds > settlementProfile.maximumLatencySeconds
  ) {
    reasonCodes.push("LATENCY_REQUIREMENT_UNMET");
  }
  if (
    money.effectiveLiquidity < requirementSet.minimumLiquidity ||
    money.effectiveLiquidity < settlementProfile.minimumLiquidity
  ) {
    reasonCodes.push("LIQUIDITY_INSUFFICIENT");
  }

  const blockingReasons = reasonCodes.length;
  if (
    money.evidenceAgeSeconds > requirementSet.maximumEvidenceAgeSeconds ||
    money.evidenceAgeSeconds > settlementProfile.maximumEvidenceAgeSeconds
  ) {
    reasonCodes.push("LIQUIDITY_EVIDENCE_STALE");
  }

  const overallStatus: CompatibilityStatus =
    blockingReasons > 0
      ? "INCOMPATIBLE"
      : reasonCodes.length > 0
        ? "CONDITIONALLY_COMPATIBLE"
        : "COMPATIBLE";

  return {
    moneyInstrument: money.id,
    overallStatus,
    reasonCodes
  };
}

export function runConformance() {
  const expectations = new Map<string, CompatibilityStatus>([
    ["EUR-X", "COMPATIBLE"],
    ["EUR-Y", "CONDITIONALLY_COMPATIBLE"],
    ["EUR-Z", "INCOMPATIBLE"]
  ]);
  const failures = referenceProfiles
    .map((profile) => ({
      instrument: profile.id,
      expected: expectations.get(profile.id) ?? "UNKNOWN",
      actual: evaluateCompatibility(profile).overallStatus
    }))
    .filter((result) => result.expected !== result.actual);

  return {
    omstVersion: "0.6.0",
    vectors: failures.length === 0 ? "PASS" : "FAIL",
    failures
  };
}

export const referenceProfiles: MoneyProfile[] = [
  {
    id: "EUR-X",
    finality: "qualified",
    settlementAvailability: "24_7",
    atomicSettlement: true,
    effectiveLiquidity: 100_000_000,
    settlementLatencySeconds: 45,
    evidenceAgeSeconds: 3_600
  },
  {
    id: "EUR-Y",
    finality: "contractual",
    settlementAvailability: "24_7",
    atomicSettlement: true,
    effectiveLiquidity: 80_000_000,
    settlementLatencySeconds: 75,
    evidenceAgeSeconds: 172_800
  },
  {
    id: "EUR-Z",
    finality: "probabilistic",
    settlementAvailability: "business_hours",
    atomicSettlement: false,
    effectiveLiquidity: 25_000_000,
    settlementLatencySeconds: 180,
    evidenceAgeSeconds: 3_600
  }
];
