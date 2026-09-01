# Money Capabilities

## Definition

`MoneyCapability` is a first-class assertion that an instrument supports, does not support, conditionally supports or has unknown support for a function.

## Purpose

Make capabilities scoped, conditional, evidence-bearing and time-bounded.

## Inputs

Capability type, status, conditions, scope, evidence and validity period.

## Outputs

Capability assertions used by transition requirements and equivalence analysis.

## State Assumptions

`SUPPORTED` is not regulatory approval. It means the represented capability is supported according to supplied evidence.

## Examples

`DELIVERY_VERSUS_PAYMENT` with status `CONDITIONAL`.

## Non-Examples

Legal authorisation, settlement guarantee or reserve attestation.

## Failure Modes

Expired validity, condition mismatch, insufficient evidence or unsupported capability.

## Relationship To Other OMST Concepts

Capabilities are checked by `TransitionRequirement` and `TransitionEvaluation`.
