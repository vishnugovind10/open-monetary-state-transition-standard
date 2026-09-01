# Changelog

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
