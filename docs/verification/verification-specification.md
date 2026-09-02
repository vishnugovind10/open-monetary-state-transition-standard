# Verification Specification

An OMST v0.7 verifier evaluates an `evaluation-package` in this order:

1. Validate package shape against the `evaluation-package` schema.
2. Confirm supported `ruleset_version`, `schema_version` and canonicalization profile.
3. Recompute the package fingerprint with the `integrity` object cleared.
4. Recompute the canonical evaluation fingerprint.
5. Validate each evidence item hash and expiry rule.
6. Reproduce or independently compare the canonical evaluation result.
7. Emit a `verification-result` and, when requested, a `settlement-verification-record`.

Implementations must preserve failure classes. Evidence tampering is `INVALID`; semantic result drift is `DIFFERENT`; unsupported rulesets are `UNSUPPORTED`.

The reference vectors intentionally include tampered liquidity, evidence, result, stale evidence, missing evidence, unsupported ruleset and canonicalization-difference cases.
