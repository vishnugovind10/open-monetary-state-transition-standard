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
    omst_version: "0.7.0",
    ruleset_version: "omst-core-0.7",
    money_instrument: "EUR-X",
    settlement_profile: "settlement-network-a",
    overall_status: "COMPATIBLE",
    reasons: [],
    evaluation_hash: "synthetic-api-reference-evaluation"
  };
}

export function verificationPackage() {
  return {
    omst_type: "evaluation-package",
    package_id: "pkg-tokenized-bond-dvp-eur-x-v07",
    package_version: "0.7.0",
    lifecycle_status: "SEALED",
    omst_version: "0.7.0",
    schema_version: "0.7.0",
    ruleset_version: "omst-core-0.7",
    canonicalization: {
      profile: "OMST-CANONICAL-JSON-0.7",
      monetary_amounts: "decimal-string",
      timestamps: "RFC3339-UTC"
    },
    integrity: {
      package_fingerprint: "75ed62b3db676808ca7bf915046f381177fba931023f0995778f46d44bf6ce9f",
      evaluation_fingerprint: "cb7849ecba0d4afbbcbbf71d49b5220a2e6a410b1b3fc3a24107ac1f133b5252"
    },
    canonical_evaluation_result: {
      status: "COMPATIBLE",
      reason_codes: [],
      blocking_conditions: [],
      warnings: [],
      evidence_status: "VALID"
    },
    evidence_manifest: {
      manifest_id: "evidence-tokenized-bond-dvp-eur-x-v07",
      evidence_items: [
        {
          evidence_id: "liq-eur-x-001",
          type: "OBSERVED",
          content_reference: "synthetic://evidence/liq-eur-x-001",
          content_hash: "dcdcf5a41d51ea2e903fc08b16d090a8c0ea6d29ee5ed48449d8146821eb52fc",
          status: "VALID"
        }
      ]
    },
    metadata: {
      synthetic: true,
      boundary: "Technical verification artifact. Not regulatory certification, legal advice, credit assessment, reserve attestation or issuer endorsement."
    }
  };
}

export function verificationResult() {
  return {
    omst_type: "verification-result",
    verification_id: "verify-pkg-tokenized-bond-dvp-eur-x-v07",
    status: "VERIFIED",
    checks: [
      { layer: "Schema", status: "PASS" },
      { layer: "Canonicalization", status: "PASS" },
      { layer: "Integrity", status: "PASS" },
      { layer: "Evidence", status: "PASS" },
      { layer: "Ruleset", status: "PASS" },
      { layer: "Semantic evaluation", status: "PASS" },
      { layer: "Semantic parity", status: "PASS" }
    ],
    semantic_equivalence: "SEMANTICALLY_EQUIVALENT",
    reasons: []
  };
}

export function verificationRecord() {
  return {
    omst_type: "settlement-verification-record",
    verification_id: "record-pkg-tokenized-bond-dvp-eur-x-v07",
    package_fingerprint: "75ed62b3db676808ca7bf915046f381177fba931023f0995778f46d44bf6ce9f",
    evaluation_fingerprint: "cb7849ecba0d4afbbcbbf71d49b5220a2e6a410b1b3fc3a24107ac1f133b5252",
    status: "VERIFIED",
    omst_version: "0.7.0",
    ruleset_version: "omst-core-0.7",
    schema_version: "0.7.0",
    verified_at: "2026-09-02T00:00:00Z",
    verifier: "OMST Reference Verifier",
    conformance_profile: "OMST-VERIFICATION",
    warnings: [],
    boundary: "Technical verification artifact. Not regulatory certification, legal advice, credit assessment, reserve attestation or issuer endorsement."
  };
}

export function verificationTamper() {
  return {
    omst_type: "verification-result",
    verification_id: "verify-tampered-liquidity-v07",
    status: "INVALID",
    checks: [
      { layer: "Integrity", status: "FAIL", reason: "package fingerprint mismatch" },
      { layer: "Evidence", status: "FAIL", reason: "evidence hash mismatch" }
    ],
    semantic_equivalence: "SEMANTICALLY_DIFFERENT",
    reasons: ["package fingerprint mismatch", "liq-eur-x-001: evidence hash mismatch"]
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
      snapshot_id: "graph-snapshot-v07-tokenized-bond-dvp",
      settlement_profile: "settlement-network-a",
      settlement_profile_fingerprint: "eb0004a2b945a4bd5a8fd99116be681dd973f39af26740121968bd726d995092",
      primary: ["EUR-X", "CBM", "EUR-Y"],
      fallback: ["EUR-X", "REDEMPTION", "BANK_MONEY", "EUR-Y"]
    },
    valid_until: "2026-09-03T00:00:00Z"
  };
}

export function adapterMap() {
  return {
    profile_id: "adapter-iso20022-v07",
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
