# RFC-0029 Profile Portability

## Status

Accepted for v0.6 reference implementation.

## Summary

OMST profiles should be portable across repositories, APIs and implementations. v0.6 introduces lifecycle metadata, validity windows, schema references and deterministic fingerprints.

## Requirement

Implementations must calculate profile fingerprints from canonical JSON while excluding the fingerprint field itself.
