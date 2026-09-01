# Money State

## Definition

`MoneyState` represents the operational state of money in a transition lifecycle.

## Purpose

Prevent systems from treating pending, failed, final, reverted and unknown states as interchangeable.

## Inputs

Instrument, state, timestamp, evidence and optional composite state dimensions.

## Outputs

Validated state or state-transition errors.

## State Assumptions

`UNKNOWN` cannot be treated as success.

## Examples

`AVAILABLE`, `SETTLING`, `FINAL`, `FAILED`.

## Non-Examples

Official monetary aggregate classification or legal status.

## Failure Modes

Illegal backward transition, final state reversal without explicit semantics, or missing timestamp.

## Relationship To Other OMST Concepts

States are consumed by `MoneyTransition`, `MoneyEvent` and the state-transition machine.
