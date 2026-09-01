# RFC-0012: Transition Plan

Status: draft

## Abstract

Defines `TransitionPlan` as an ordered set of monetary transitions intended to satisfy a settlement intent.

## Motivation

Institutional workflows need auditable plans, not only single-hop route results.

## Scope

Synthetic cash-leg transition plans in v0.3.

## Terminology

Plan, step, expected state, failure path.

## Specification

See `schemas/transition-plan.schema.json`.

## Examples

EUR-X to CBM to EUR-Y.

## Security Considerations

Route manipulation and graph poisoning can produce unsafe plans.

## Privacy Considerations

Plans should avoid exposing private participant identity.

## Compatibility

Adds a new object without changing v0.2 transitions.

## Open Questions

How should formal recovery semantics be represented?
