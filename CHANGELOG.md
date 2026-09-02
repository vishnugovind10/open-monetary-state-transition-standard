# Changelog

## v0.7.0

- Added portable `evaluation-package`, `evidence-manifest`, `verification-result`, `settlement-verification-record` and `settlement-evaluation-bundle` schemas.
- Added Python verification APIs and CLI commands for package creation, sealing, verification, bundle verification and tamper-vector generation.
- Added `OMST-VERIFICATION` conformance coverage with valid, modified, stale, missing-evidence and unsupported-ruleset vectors.
- Added an isolated minimal verifier and TypeScript verification entry point for independent implementation checks.
- Added stateless API-shaped verification endpoints under `/api/v1/verification/*`.
- Updated OMST Explorer with a Verification Lab panel for package fingerprints, verifier layers and tamper outcomes.

## v0.6.0

- Added portable settlement interoperability layer with settlement, participant, network and interoperability profile models.
- Added profile fingerprints, decentralized OMST manifest discovery and `.well-known/omst.json`.
- Added settlement request, offer and response examples for cross-party compatibility exchange.
- Added Conformance 2.0 profile declarations, cross-language parity reporting and TypeScript conformance entry point.
- Added MoneyGraph snapshots, fallback/recovery route output and adapter framework documentation for generic, OTAS, ISO 20022 and CDM mappings.
- Added stateless API-shaped endpoints under `/api/v1/*` for profile validation, settlement exchange, route, plan, conformance and adapter mapping.
- Updated Explorer with Profiles, Settlement Exchange and Adapters proof panels.

## v0.5.0

- Added settlement-compatibility profiles with `COMPATIBLE`, `CONDITIONALLY_COMPATIBLE`, `INCOMPATIBLE` and `UNKNOWN` statuses.
- Added machine-readable money requirement sets, evidence policies, reason codes and deterministic compatibility evaluation.
- Added v0.5 conformance vectors proving EUR-X compatible, EUR-Y conditionally compatible and EUR-Z incompatible for the synthetic EUR 50m tokenized-bond DvP scenario.
- Added `omst requirement`, `omst evaluate-settlement --money`, `omst explain`, `omst conformance` and `omst manifest`.
- Added a TypeScript reference compatibility evaluator and updated OMST Explorer to use v0.5 status and reason-code vocabulary.
- Added implementer guidance for independent reproducibility and evidence-boundary handling.

## v0.4.0

- Added OMST Explorer, a Vite/React workbench for synthetic monetary state, settlement, equivalence, graph, stress and conformance inspection.
- Added browser-level Explorer tests and CI web build/test gates.
- Added Vercel deployment configuration for the public Explorer.
- Documented the Explorer evidence boundary and local usage.

## v0.3.0

- Added settlement intent, settlement compatibility, transition plan and settlement bundle primitives.
- Added `omst profile`, `omst capability`, `omst evaluate-settlement`, `omst plan`, `omst graph --format mermaid` and `omst stress`.
- Added DvP scenario files, settlement docs, interoperability levels and executable stress output.
- Added v0.3 schemas and conformance vectors.

## v0.2.0

- Added first-class capability, relation, event, context, requirement, evaluation and equivalence models.
- Added OMST event envelope, state-transition-machine and settlement-context schemas.
- Added whitepaper, RFC process, MkDocs navigation, threat model and expanded regulatory boundary docs.
- Added conformance examples and tests for event semantics, requirement evaluation and monetary equivalence.

## v0.1.0

- Initial experimental reference specification, schemas, Python implementation, CLI, examples, simulations and conformance tests.
