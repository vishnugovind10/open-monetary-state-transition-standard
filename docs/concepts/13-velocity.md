# Velocity

## Definition

Settlement velocity measures how intensively settlement-ready balances support settlement activity over an observation window.

## Purpose

Analyse settlement capacity without confusing it with macroeconomic money velocity.

## Inputs

Settlement value and time-weighted settlement-ready balance.

## Outputs

Gross, net, state-specific, intraday or venue-specific velocity where data permits.

## State Assumptions

Velocity must be qualified by instrument, state, venue, transaction type and time window.

## Examples

EUR 5bn settled over EUR 500m settlement-ready balance gives velocity 10.0.

## Non-Examples

Official macroeconomic velocity.

## Failure Modes

Zero denominator, stale volume, unsupported aggregation or missing state data.

## Relationship To Other OMST Concepts

Velocity informs mobility, stress simulations and fragmentation analysis.
