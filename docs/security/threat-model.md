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

## Controls

OMST separates transition integrity from evidence integrity. Implementations must preserve source type, timestamp, method and scope so issuer declarations, observed ledger facts, derived calculations and simulations cannot be silently conflated.
