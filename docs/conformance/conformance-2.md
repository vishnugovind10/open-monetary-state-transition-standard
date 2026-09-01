# Conformance 2.0

OMST v0.6 expands conformance beyond schema validation.

## Profiles

- `OMST-CORE`
- `OMST-MONEY`
- `OMST-STATE`
- `OMST-TRANSITION`
- `OMST-EVIDENCE`
- `OMST-SETTLEMENT`
- `OMST-COMPATIBILITY`
- `OMST-ROUTING`
- `OMST-INTEROPERABILITY`

## Requirements

A conforming implementation must:

- validate schemas for supported profile types
- preserve canonical JSON behavior
- reject float monetary amounts
- reproduce reference compatibility statuses
- reproduce reference reason codes
- preserve adapter mapping classifications
- report unsupported or lossy mappings explicitly

## Cross-Language Parity

The repository includes Python and TypeScript reference evaluators for the synthetic compatibility vectors. Parity means the implementations produce the same public status and reason-code semantics for the same vector set.
