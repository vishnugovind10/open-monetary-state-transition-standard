# Monetary Instruments

## Definition

A monetary instrument is any represented unit or claim used as the monetary leg of a transaction.

## Purpose

Describe instrument identity without hard-coding legal status.

## Inputs

Issuer, currency, claim type, ledger model, settlement model, redemption model and evidence.

## Outputs

A `MoneyProfile` and related capability assertions.

## State Assumptions

Instrument identity is separate from current operational state.

## Examples

Central-bank money, tokenised deposits, regulated digital money and synthetic test instruments.

## Non-Examples

Tokenised securities, governance tokens and reserve portfolios.

## Failure Modes

Ambiguous issuer, unsupported currency, missing claim context or unsupported evidence.

## Relationship To Other OMST Concepts

Instruments are nodes in the money graph and sources or targets of transitions.
