# Threat Model

## Actors

- issuer
- participant
- settlement venue
- malicious observer
- malicious data provider
- compromised adapter
- compromised oracle
- malicious route

## Threats

- false state
- false transition
- false evidence
- stale liquidity
- stale finality
- route manipulation
- identity mismatch
- event replay
- evidence poisoning
- graph poisoning
- privacy leakage
- adapter semantic drift
- fingerprint substitution
- stale discovery manifest
- participant-profile spoofing
- lossy mapping presented as exact mapping

## Controls

OMST separates transition integrity from evidence integrity. Implementations must preserve source type, timestamp, method and scope so issuer declarations, observed ledger facts, derived calculations and simulations cannot be silently conflated.

v0.6 implementations must also preserve profile fingerprints, adapter lossiness classifications, manifest freshness and participant eligibility evidence. Discovery metadata must not be treated as authorization to settle or as proof of issuer, regulatory or market-condition truth.
