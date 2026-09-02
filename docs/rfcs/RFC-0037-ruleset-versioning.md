# RFC-0037 Ruleset Versioning

Status: Draft

Defines ruleset version handling for v0.7 verification.

A verifier must return `UNSUPPORTED` when it cannot evaluate the declared ruleset. It must not silently substitute another ruleset and return `VERIFIED`.
