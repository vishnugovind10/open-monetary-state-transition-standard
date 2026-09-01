# Settlement

## Definition

Settlement is the process by which a monetary transition reaches an agreed final state for a transaction context.

## Purpose

Represent DvP, PvP, FoP, escrow, net settlement, gross settlement, atomic settlement and conditional settlement.

## Inputs

Settlement context, conditions, legs, dependencies, finality and evidence.

## Outputs

Compatibility and integrity findings.

## State Assumptions

Do not assume atomicity merely because a protocol claims atomic settlement.

## Examples

EUR cash leg for a synthetic tokenised-bond DvP.

## Non-Examples

Execution by a settlement rail.

## Failure Modes

Timeout, partial execution, rollback, reconciliation required and manual intervention.

## Relationship To Other OMST Concepts

Settlement context constrains transition evaluation and route selection.
