# OMST v0.6 Specification

OMST is an open standard for describing digital money and determining whether it can satisfy settlement requirements across heterogeneous financial systems.

v0.6 defines a portable interoperability layer around the existing monetary state-transition model. It standardizes money profiles, settlement profiles, participant profiles, interoperability profiles, settlement exchange objects, adapter mappings, graph snapshots and conformance profiles.

## Scope

OMST describes monetary behavior. It does not issue, custody, redeem, transfer or settle money. It does not certify regulatory compliance, issuer solvency, reserve quality, legal enforceability or market conditions.

All repository examples are synthetic reference data unless explicitly labelled otherwise.

## Core Inputs

A deterministic settlement evaluation is computed from:

- `MoneyProfile`
- `MoneyState`
- `SettlementProfile`
- `SettlementIntent`
- `MoneyRequirementSet`
- `Evidence`
- `EvidencePolicy`
- ruleset version
- schema version
- evaluation timestamp

Implementations must not infer compatibility from an instrument name alone. Compatibility must emerge from profile fields, state predicates, requirements, evidence and rules.

## MoneyProfile v0.6

`MoneyProfile` describes a monetary instrument's semantic and operational properties. v0.6 adds portable lifecycle metadata:

- `profile_version`
- `profile_lifecycle_status`
- `profile_fingerprint`
- `valid_from`
- `valid_until`
- `schema_uri`
- `implementation_uri`

The profile fingerprint is calculated over canonical JSON with `profile_fingerprint` excluded, so independently hosted copies can be compared.

## SettlementProfile

`SettlementProfile` describes a settlement environment:

- supported currencies
- settlement modes
- finality model
- atomicity support
- operating window
- latency target
- participant requirements
- evidence requirements

It is separate from the money profile because the same monetary instrument may be usable in multiple settlement environments with different rules.

## ParticipantProfile

`ParticipantProfile` describes a party or system participating in settlement:

- participant type
- jurisdiction reference
- eligible roles
- network memberships
- signing and authorization references
- evidence references

OMST does not identify real institutions in synthetic examples.

## SettlementNetworkProfile

`SettlementNetworkProfile` describes a network capable of carrying monetary settlement. It includes network type, supported settlement profiles, availability, finality, routing constraints and participant eligibility constraints.

## InteroperabilityProfile

`InteroperabilityProfile` records how an OMST profile maps to an external representation. v0.6 includes conceptual mappings for:

- generic JSON
- OTAS
- ISO 20022
- ISDA CDM
- FINOS CDM

Mappings must classify each mapped field as `EXACT`, `APPROXIMATED`, `DERIVED`, `UNSUPPORTED` or `LOSSY`. A mapping with approximated or lossy fields must not claim semantic equivalence.

## Settlement Exchange

OMST defines three portable exchange objects:

- `SettlementRequest`: what settlement is being requested and what money properties are required.
- `SettlementOffer`: what a participant or system can offer for the requested settlement.
- `SettlementResponse`: the deterministic compatibility result, accepted requirements, rejected requirements, conditional requirements, route and transition plan.

These objects allow counterparties, routers and applications to exchange machine-readable compatibility information without sharing private operational data.

## Compatibility Status

The settlement evaluator returns:

- `COMPATIBLE`: mandatory requirements and evidence policy checks pass.
- `CONDITIONALLY_COMPATIBLE`: mandatory requirements pass but stale evidence, warnings or assumptions remain.
- `INCOMPATIBLE`: one or more mandatory requirements fail.
- `UNKNOWN`: required state, profile or evidence data is unavailable.

Reason codes are machine-readable and stable within a ruleset version.

## Graph Snapshot and Routing

`MoneyGraphSnapshot` records monetary instruments, settlement networks, route edges, constraints and fallback routes used during an evaluation. Fallback routes are descriptive outputs, not instructions to execute settlement.

## Manifest and Discovery

An OMST implementation may publish:

- `omst-manifest.json`
- `.well-known/omst.json`

The manifest declares implementation version, conformance profiles, supported profile types, settlement exchange support and adapter families.

## API Shape

The reference repository includes stateless API-shaped endpoints under `/api/v1/*`:

- `/api/v1/profile/validate`
- `/api/v1/settlement/request`
- `/api/v1/settlement/evaluate`
- `/api/v1/settlement/response`
- `/api/v1/equivalence`
- `/api/v1/plan`
- `/api/v1/route`
- `/api/v1/conformance`
- `/api/v1/adapter/map`

These endpoints expose synthetic reference responses. They are not production settlement services.

## Conformance 2.0

v0.6 declares the following conformance profiles:

- `OMST-CORE`
- `OMST-MONEY`
- `OMST-STATE`
- `OMST-TRANSITION`
- `OMST-EVIDENCE`
- `OMST-SETTLEMENT`
- `OMST-COMPATIBILITY`
- `OMST-ROUTING`
- `OMST-INTEROPERABILITY`

Conforming implementations must reproduce reference statuses, reason codes and canonical JSON hashes for conformance vectors within the same ruleset version.

## Reference Scenario

The flagship scenario is a synthetic EUR 50m tokenized-bond DvP cash leg:

- `EUR-X` is compatible.
- `EUR-Y` is conditionally compatible because liquidity evidence is stale.
- `EUR-Z` is incompatible because mandatory atomicity, finality, availability, latency and liquidity requirements fail.

This scenario is generated from profiles, state, requirements, evidence policy and rules. It is not issuer evidence or a representation of live market conditions.
