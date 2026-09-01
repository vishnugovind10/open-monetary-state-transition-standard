# Portable Profiles

OMST v0.6 separates monetary, settlement, participant and adapter semantics into portable profiles.

## Profile Types

- `MoneyProfile` describes the instrument and its monetary properties.
- `SettlementProfile` describes the environment in which settlement is evaluated.
- `ParticipantProfile` describes participant roles, eligibility and authorization references.
- `SettlementNetworkProfile` describes a network that may carry settlement.
- `InteroperabilityProfile` describes mappings between OMST and an external representation.

## Fingerprints

Profile fingerprints are calculated over canonical JSON with the fingerprint field excluded. Implementations use fingerprints to compare independently distributed profiles without trusting filenames or hosting locations.

## Lifecycle

Profiles may be `DRAFT`, `ACTIVE`, `DEPRECATED`, `SUPERSEDED` or `REVOKED`. A revoked or expired profile should not be treated as current evidence.

## Boundary

Profiles are structured claims. They are not proof that settlement can occur, that a participant is authorized, or that a real issuer has attested to the profile.
