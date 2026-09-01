# RFC-0014: Multi-Leg Settlement

Status: draft

## Abstract

Defines `SettlementBundle` for cash, asset, FX, collateral and fee legs.

## Motivation

Real settlement workflows often involve more than one leg.

## Scope

Schema-level representation in v0.3.

## Terminology

Atomic, conditional atomic, sequenced, netted, partially atomic, non-atomic.

## Specification

See `schemas/settlement-bundle.schema.json`.

## Examples

Synthetic tokenized-bond DvP bundle.

## Security Considerations

Partial execution and rollback semantics must remain explicit.

## Privacy Considerations

Bundle leg metadata may reveal trading relationships and should be minimized.

## Compatibility

Adds a new object.

## Open Questions

How should asset-leg conformance be shared with OTAS-like models?
