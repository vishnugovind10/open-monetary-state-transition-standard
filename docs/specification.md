# OMST v0.7 Specification

OMST defines machine-readable primitives for describing digital money and determining whether it can satisfy settlement requirements across heterogeneous financial systems.

v0.7 adds portable settlement verification:

- `evaluation-package` artifacts carrying canonical settlement results, evidence manifests and integrity fingerprints.
- `settlement-evaluation-bundle` artifacts for portable review and archival.
- `verification-result` and `settlement-verification-record` outputs.
- `OMST-VERIFICATION` conformance vectors for valid, tampered, stale, missing and unsupported package cases.
- Python reference verifier, isolated minimal verifier and TypeScript verification entry point.
- API-shaped verification endpoints under `/api/v1/verification/*`.

See the repository root `SPECIFICATION.md` for the full normative text.
