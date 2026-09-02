import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

export type VerificationStatus = "VERIFIED" | "DIFFERENT" | "INVALID" | "UNSUPPORTED" | "UNKNOWN";

export type VerificationCheck = {
  layer: string;
  status: "PASS" | "FAIL";
  reason: string;
};

type JsonValue = null | boolean | number | string | JsonValue[] | { [key: string]: JsonValue };
type JsonObject = { [key: string]: JsonValue };

export function canonicalize(value: JsonValue): JsonValue {
  if (Array.isArray(value)) {
    return value.map((item) => canonicalize(item));
  }
  if (value !== null && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, canonicalize(value[key])])
    );
  }
  return value;
}

export function canonicalHash(value: JsonValue): string {
  return createHash("sha256")
    .update(JSON.stringify(canonicalize(value)))
    .digest("hex");
}

export function packageFingerprint(pkg: JsonObject): string {
  return canonicalHash({ ...pkg, integrity: {} });
}

export function evidenceErrors(pkg: JsonObject): string[] {
  const manifest = pkg.evidence_manifest as JsonObject | undefined;
  const items = Array.isArray(manifest?.evidence_items) ? manifest.evidence_items : [];
  const errors: string[] = [];

  if (items.length === 0) {
    errors.push("evidence manifest contains no items");
    return errors;
  }

  for (const rawItem of items) {
    const item = rawItem as JsonObject;
    const evidenceId = String(item.evidence_id ?? "unknown");
    const inline = item.inline_content as JsonValue | undefined;
    if (inline === undefined) {
      if (item.status === "MISSING") {
        errors.push(`${evidenceId}: missing evidence`);
      }
      continue;
    }
    if (item.content_hash !== canonicalHash(inline)) {
      errors.push(`${evidenceId}: evidence hash mismatch`);
    }
    if (String(item.expires_at ?? "") <= "2026-09-02T00:00:00Z") {
      errors.push(`${evidenceId}: evidence expired`);
    }
  }
  return errors;
}

export function verifyPackage(pkg: JsonObject) {
  const checks: VerificationCheck[] = [];
  const reasons: string[] = [];
  const addCheck = (layer: string, status: "PASS" | "FAIL", reason = "") => {
    checks.push({ layer, status, reason });
    if (status === "FAIL" && reason) {
      reasons.push(reason);
    }
  };

  addCheck(
    "Schema",
    pkg.omst_type === "evaluation-package" ? "PASS" : "FAIL",
    pkg.omst_type === "evaluation-package" ? "" : "not an evaluation package"
  );
  const integrity = pkg.integrity as JsonObject | undefined;
  const expectedPackage = integrity?.package_fingerprint;
  const actualPackage = packageFingerprint(pkg);
  addCheck(
    "Integrity",
    expectedPackage === actualPackage ? "PASS" : "FAIL",
    expectedPackage === actualPackage ? "" : "package fingerprint mismatch"
  );
  const evidence = evidenceErrors(pkg);
  addCheck("Evidence", evidence.length === 0 ? "PASS" : "FAIL", evidence.join("; "));
  addCheck(
    "Ruleset",
    pkg.ruleset_version === "omst-core-0.7" ? "PASS" : "FAIL",
    pkg.ruleset_version === "omst-core-0.7" ? "" : `unsupported ruleset ${String(pkg.ruleset_version)}`
  );
  addCheck(
    "Semantic evaluation",
    (pkg.canonical_evaluation_result as JsonObject | undefined)?.status === "COMPATIBLE" ? "PASS" : "FAIL",
    (pkg.canonical_evaluation_result as JsonObject | undefined)?.status === "COMPATIBLE"
      ? ""
      : "semantic evaluation differs"
  );

  const failedLayers = new Set(checks.filter((check) => check.status === "FAIL").map((check) => check.layer));
  let status: VerificationStatus = "VERIFIED";
  if (failedLayers.has("Ruleset")) {
    status = "UNSUPPORTED";
  } else if (failedLayers.has("Semantic evaluation")) {
    status = "DIFFERENT";
  } else if (failedLayers.size > 0) {
    status = "INVALID";
  }

  return {
    omst_type: "verification-result",
    status,
    checks,
    semantic_equivalence: status === "VERIFIED" ? "SEMANTICALLY_EQUIVALENT" : "SEMANTICALLY_DIFFERENT",
    reasons
  };
}

export function verifyPackageFile(path: string) {
  return verifyPackage(JSON.parse(readFileSync(path, "utf8")) as JsonObject);
}
