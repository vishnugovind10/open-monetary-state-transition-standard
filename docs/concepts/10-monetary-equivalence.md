# Monetary Equivalence

## Definition

Monetary equivalence compares instruments by nominal, functional, settlement, economic and contextual properties.

## Purpose

Show why same currency does not necessarily mean same settlement capability.

## Inputs

Two money profiles and a transaction context.

## Outputs

`NOMINALLY_EQUIVALENT`, `FUNCTIONALLY_EQUIVALENT`, `SETTLEMENT_EQUIVALENT`, `CONDITIONALLY_EQUIVALENT`, `NOT_EQUIVALENT` or `UNKNOWN`.

## State Assumptions

Equivalence is context-specific.

## Examples

EUR-X and EUR-Y may be nominally equivalent but not settlement-equivalent.

## Non-Examples

An issuer ranking or money quality score.

## Failure Modes

Missing context, unsupported capability or incompatible finality.

## Relationship To Other OMST Concepts

Equivalence uses profiles, capabilities and settlement context.
