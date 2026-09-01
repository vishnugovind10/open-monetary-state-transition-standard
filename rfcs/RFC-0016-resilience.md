# RFC-0016: Resilience

Status: draft

## Abstract

Defines future resilience fields for fallback routes, outages, recovery time and manual intervention.

## Motivation

Settlement systems must handle failure, timeout, partial execution and recovery.

## Scope

Roadmap and stress output in v0.3.

## Terminology

Outage, fallback route, recovery state, reconciliation.

## Specification

See `src/omst/stress.py`.

## Examples

Synthetic liquidity shock.

## Security Considerations

Resilience claims require evidence and must not be inferred from availability alone.

## Privacy Considerations

Operational dependency details can be sensitive.

## Compatibility

Adds research and stress-testing hooks.

## Open Questions

How should recovery proof be standardized?
