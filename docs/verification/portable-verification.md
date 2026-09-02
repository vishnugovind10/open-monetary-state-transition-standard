# Portable Verification

OMST v0.7 adds a portable verification layer for settlement compatibility results.

The purpose is narrow: let an independent implementation verify that a packaged settlement result is structurally valid, canonically represented, internally consistent, supported by the declared ruleset and consistent with its evidence manifest.

## Artifacts

- `evaluation-package`: source references, canonical evaluation result, evidence manifest, canonicalization profile and integrity fingerprints.
- `settlement-evaluation-bundle`: an exchange wrapper that carries an evaluation package with settlement context.
- `verification-result`: machine-readable verifier output.
- `settlement-verification-record`: human-facing technical verification record.

## Status Values

- `VERIFIED`: all required checks pass.
- `VERIFIED_WITH_WARNINGS`: required checks pass with non-blocking warnings.
- `INVALID`: schema, integrity, evidence freshness or evidence hash checks fail.
- `DIFFERENT`: reproduced semantic result differs from the packaged result.
- `UNSUPPORTED`: ruleset or canonicalization profile is not supported.
- `UNKNOWN`: the verifier lacks enough information to decide.

Verification is not settlement execution, issuer approval, reserve assurance, legal analysis or regulatory certification.
