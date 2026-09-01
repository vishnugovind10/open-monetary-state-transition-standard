const headers = { "content-type": "application/json; charset=utf-8" };

export function respond(res, body) {
  res.statusCode = 200;
  Object.entries(headers).forEach(([key, value]) => res.setHeader(key, value));
  res.end(JSON.stringify(body, null, 2));
}

export function profile() {
  return {
    status: "VALID",
    fingerprint: "synthetic-reference-profile-fingerprint",
    boundary: "Synthetic reference response. Not issuer, regulatory or market-condition evidence."
  };
}

export function settlementEvaluation() {
  return {
    evaluation_id: "eval-intent-tokenized-bond-dvp-EUR-X",
    omst_version: "0.6.0",
    ruleset_version: "omst-core-0.6",
    money_instrument: "EUR-X",
    settlement_profile: "settlement-network-a",
    overall_status: "COMPATIBLE",
    reasons: [],
    evaluation_hash: "synthetic-api-reference-evaluation"
  };
}

export function settlementRequest() {
  return {
    request_id: "request-tokenized-bond-dvp-eur-50m",
    settlement_intent: "examples/tokenized-bond-dvp/settlement-intent.json",
    required_money: "EUR",
    required_capabilities: ["DVP", "ATOMIC_SETTLEMENT"],
    amount: "50000000",
    deadline: "2026-09-02T00:00:00Z"
  };
}

export function settlementResponse() {
  return {
    request_id: "request-tokenized-bond-dvp-eur-50m",
    status: "COMPATIBLE",
    accepted_requirements: ["atomicity", "finality", "availability", "effective_liquidity"],
    rejected_requirements: [],
    conditional_requirements: [],
    transition_plan: { plan_id: "plan-tokenized-bond-dvp" },
    route: {
      snapshot_id: "graph-snapshot-v06-tokenized-bond-dvp",
      settlement_profile: "settlement-network-a",
      settlement_profile_fingerprint: "eb0004a2b945a4bd5a8fd99116be681dd973f39af26740121968bd726d995092",
      primary: ["EUR-X", "CBM", "EUR-Y"],
      fallback: ["EUR-X", "REDEMPTION", "BANK_MONEY", "EUR-Y"]
    },
    valid_until: "2026-09-02T00:00:00Z"
  };
}

export function adapterMap() {
  return {
    profile_id: "adapter-iso20022-v06",
    external_standard: "ISO 20022",
    mapping_direction: "EXTERNAL_TO_OMST",
    supported_fields: {
      amount: "EXACT",
      currency: "EXACT",
      settlement_state: "APPROXIMATED"
    },
    lossiness: "APPROXIMATED"
  };
}
