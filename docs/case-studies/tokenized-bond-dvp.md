# Synthetic EUR 50m Tokenized Bond DvP

Synthetic example. Not an issuer assessment. Not a regulatory assessment. Not a representation of actual market conditions.

## Institutional Problem

A tokenized bond transaction requires a EUR cash leg that can settle within 60 seconds with qualified finality and atomicity assumptions.

## Where OMST Fits

OMST represents the cash instrument, state, route, transition plan, liquidity, finality and evidence assumptions.

## What OMST Does Not Solve

OMST does not execute the DvP, custody assets, settle central-bank money or provide legal/regulatory certification.

## Reproduce

```bash
omst evaluate-settlement examples/tokenized-bond-dvp/
omst plan examples/tokenized-bond-dvp/
omst graph --format mermaid
```
