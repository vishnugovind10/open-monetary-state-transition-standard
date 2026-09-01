# Money Profile

## Definition

`MoneyProfile` describes the identity, function, settlement, redemption, transfer, access, control, network and evidence metadata of a digital-money instrument.

## Purpose

Provide the stable instrument context needed to interpret state and transitions.

## Inputs

Identity, issuer, currency, claim type, monetary-layer reference, capabilities, constraints and evidence.

## Outputs

A strict JSON document or typed Python object.

## State Assumptions

Profiles do not prove current availability or settlement readiness by themselves.

## Examples

`examples/synthetic-eur-stablecoin/eur-x.json`.

## Non-Examples

Reserve sufficiency certificates, legal opinions or issuer authorisation records.

## Failure Modes

Unsupported schema fields, stale evidence, missing capability scope or ambiguous classification.

## Relationship To Other OMST Concepts

Profiles provide inputs to equivalence, routing, integrity and transition evaluation.
