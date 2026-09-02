# RFC-0034 Verification Semantics

Status: Draft

Defines verification statuses: `VERIFIED`, `VERIFIED_WITH_WARNINGS`, `INVALID`, `DIFFERENT`, `UNSUPPORTED` and `UNKNOWN`.

Implementations must not collapse evidence failures, semantic drift and unsupported rulesets into one generic error.
