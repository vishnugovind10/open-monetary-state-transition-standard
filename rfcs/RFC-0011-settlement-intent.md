# RFC-0011: Settlement Intent

Status: draft

## Abstract

Defines `SettlementIntent` as a machine-readable statement of transaction requirements before a monetary instrument is selected.

## Motivation

Settlement compatibility cannot be evaluated without explicit requirements for cash, finality, latency, availability and atomicity.

## Scope

Cash-leg settlement intents for v0.3 synthetic DvP examples.

## Terminology

Intent, cash leg, finality, atomicity, operating availability.

## Specification

See `schemas/settlement-intent.schema.json`.

## Examples

See `examples/tokenized-bond-dvp/settlement-intent.json`.

## Security Considerations

Intent fields can be manipulated to relax constraints; implementations must preserve requirement provenance.

## Privacy Considerations

Participant references should be synthetic, public or privacy-preserving.

## Compatibility

Backwards compatible with v0.2 because it adds a new object.

## Open Questions

How should asset-side requirements be imported from external standards?
