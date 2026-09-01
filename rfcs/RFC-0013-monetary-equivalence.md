# RFC-0013: Monetary Equivalence

Status: draft

## Abstract

Defines nominal, functional, settlement, economic and contextual equivalence.

## Motivation

Same currency denomination does not necessarily imply operational settlement equivalence.

## Scope

Contextual comparison of two `MoneyProfile` records.

## Terminology

Nominal equivalence, functional equivalence, settlement equivalence.

## Specification

See `src/omst/equivalence.py`.

## Examples

EUR-X and EUR-Z can be functionally equivalent but not settlement-equivalent.

## Security Considerations

Equivalence output must not be misrepresented as issuer quality or regulatory status.

## Privacy Considerations

No private issuer data should be included in public examples.

## Compatibility

Extends v0.2 equivalence semantics.

## Open Questions

How should economic equivalence thresholds be represented without false precision?
