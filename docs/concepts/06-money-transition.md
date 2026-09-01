# Money Transition

## Definition

`MoneyTransition` records a change from one monetary state, instrument, ledger or settlement environment to another.

## Purpose

Answer what changed when digital money moved.

## Inputs

Source and target instruments, states, quantity, currency, finality, liquidity, constraints and evidence.

## Outputs

Transition integrity, route impact, conformance results and resulting state.

## State Assumptions

Currency cannot silently change and quantity cannot become negative.

## Examples

`EUR-X:AVAILABLE -> EUR-Y:FINAL` for EUR 50m.

## Non-Examples

A bridge transaction without state semantics or evidence lineage.

## Failure Modes

Liquidity exceeded, deadline failure, finality mismatch, partial execution or settlement failure.

## Relationship To Other OMST Concepts

This is the core OMST primitive and links profile, state, evidence, context and evaluation.
