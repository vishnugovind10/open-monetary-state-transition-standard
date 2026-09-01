# OMST Whitepaper

## Thesis

Same currency does not necessarily mean same settlement capability. OMST makes the difference machine-readable.

Digital money denominated in the same currency can differ by issuer, ledger, legal claim, operating window, access model, settlement finality, redemption path, liquidity, controls and evidence. That means nominal monetary equivalence is not enough for tokenised financial transactions.

## Research Question

When digital money moves between monetary instruments, ledgers or settlement environments, what properties are preserved, degraded, transformed or made uncertain?

## Standard Layers

```text
MoneyProfile -> MoneyCapability -> MoneyState -> MoneyTransition
              -> Evidence -> SettlementContext -> TransitionRequirement
              -> TransitionEvaluation -> TransitionIntegrity -> MoneyGraph
```

## Scope

OMST is a semantic and conformance layer for the monetary leg of tokenised finance. It is protocol-agnostic and can be used with synthetic data, issuer-declared data, observed ledger data, research datasets and future adapters.

## Non-Scope

OMST is not a stablecoin, reserve platform, treasury platform, bank, payment network, bridge, blockchain, compliance engine, oracle, custody system, financial product, official monetary classification, ECB/BIS standard or replacement for ISO, ISDA, FINOS or OTAS.

## OTAS Relationship

OTAS asks what a tokenised asset is and what it can do. OMST asks what the monetary instrument is and what it can do. Together, an asset representation and a monetary representation can support cross-domain settlement compatibility analysis.

No affiliation or formal compatibility is claimed.
