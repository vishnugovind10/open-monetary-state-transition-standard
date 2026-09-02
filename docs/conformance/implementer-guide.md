# Implementer Guide

This guide describes the minimum behavior expected from an OMST settlement-compatibility and verification implementation.

## Required Inputs

An implementation must accept:

- A settlement intent.
- A money profile.
- A settlement profile.
- A participant profile when participant eligibility is in scope.
- A money state snapshot.
- A money requirement set.
- An evidence policy.
- An evaluation context containing OMST version, ruleset version and evaluation timestamp.

## Required Evaluation Behavior

An implementation must:

- Evaluate mandatory requirements before preferred and optional requirements.
- Treat unknown mandatory information as `UNKNOWN` unless the requirement can be proven false.
- Return `INCOMPATIBLE` when any mandatory requirement fails.
- Return `CONDITIONALLY_COMPATIBLE` when mandatory requirements pass but evidence is stale, warning-level reason codes exist or explicit assumptions are needed.
- Return `COMPATIBLE` only when mandatory requirements and evidence policy checks pass.
- Preserve machine-readable reason codes in output.
- Produce deterministic canonical JSON for conformance vectors.

## Reference Commands

```bash
omst requirement examples/requirements/tokenized-bond-dvp.json
omst evaluate-settlement examples/tokenized-bond-dvp/settlement-intent.json --money examples/eur-x.json
omst evaluate-settlement examples/tokenized-bond-dvp/settlement-intent.json --money examples/eur-x.json --settlement examples/settlement-networks/network-a.json
omst evaluate-settlement examples/tokenized-bond-dvp/settlement-intent.json --money examples/eur-y.json
omst evaluate-settlement examples/tokenized-bond-dvp/settlement-intent.json --money examples/eur-z.json
omst settlement-profile examples/settlement-networks/network-a.json
omst participant examples/participants/party-a.json
omst interoperability examples/interoperability/iso20022-conceptual.json
omst adapter iso20022
omst exchange --intent examples/tokenized-bond-dvp/settlement-intent.json --money examples/eur-x.json --settlement examples/settlement-networks/network-a.json
omst conformance --profile OMST-INTEROPERABILITY
omst conformance
```

## Independent Implementations

The Python and TypeScript reference implementations intentionally use the same public statuses and reason-code vocabulary. The TypeScript implementation is scoped to compatibility-profile reproduction and is not a web UI dependency.

Conformance 2.0 reports profile-level results for `OMST-CORE`, `OMST-MONEY`, `OMST-STATE`, `OMST-TRANSITION`, `OMST-EVIDENCE`, `OMST-SETTLEMENT`, `OMST-COMPATIBILITY`, `OMST-ROUTING` and `OMST-INTEROPERABILITY`.

## Evidence Boundary

Conformance validates implementation behavior against synthetic vectors. It is not an audit opinion, issuer attestation, regulatory determination, market-data feed or production settlement certification.
