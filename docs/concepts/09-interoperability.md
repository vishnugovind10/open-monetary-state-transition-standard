# Interoperability

## Definition

Interoperability is the ability for monetary instruments, ledgers or settlement environments to exchange state-transition information or perform coordinated transitions.

## Purpose

Describe interoperability levels without claiming that systems satisfy them.

## Inputs

Relations, routes, events, ledgers, constraints, settlement modes and evidence.

## Outputs

Interoperability level and route compatibility.

## State Assumptions

Messaging interoperability is weaker than settlement interoperability.

## Examples

L0 no interoperability, L1 messaging, L2 asset transfer, L3 coordinated settlement, L4 atomic settlement, L5 functional equivalence.

## Non-Examples

A generic bridge claim without finality, liquidity and evidence semantics.

## Failure Modes

Cross-ledger mismatch, identity mismatch, trapped liquidity and incompatible operating windows.

## Relationship To Other OMST Concepts

Interoperability is represented through `MoneyRelation`, event envelopes and graph routing.
