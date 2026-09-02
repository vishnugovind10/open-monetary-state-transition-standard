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

OMST is a semantic and conformance layer for the monetary leg of tokenised finance. It is protocol-agnostic and can be used with synthetic data, issuer-declared data, observed ledger data, research datasets and adapter mappings.

v0.6 expands the model into a portable profile layer. Money profiles, settlement profiles, participant profiles and interoperability profiles can be exchanged independently, fingerprinted deterministically and evaluated against the same settlement intent without depending on a single implementation.

v0.7 adds portable verification. A settlement evaluator can package its canonical result, input references, evidence manifest and integrity fingerprints so a second implementation can check schema validity, canonicalization, evidence integrity, ruleset support and semantic parity.

## Non-Scope

OMST is not a stablecoin, reserve platform, treasury platform, bank, payment network, bridge, blockchain, compliance engine, oracle, custody system, financial product, official monetary classification, ECB/BIS standard or replacement for ISO, ISDA, FINOS or OTAS.

## OTAS Relationship

OTAS asks what a tokenised asset is and what it can do. OMST asks what the monetary instrument is and what it can do. Together, an asset representation and a monetary representation can support cross-domain settlement compatibility analysis.

No affiliation or formal compatibility is claimed.

## v0.6 Interoperability Thesis

Settlement interoperability needs more than message translation. A payment, DvP leg, PvP leg, repo movement, collateral movement or redemption flow requires compatible monetary state, finality, availability, atomicity, eligibility, evidence freshness and route constraints.

OMST v0.6 treats external standards as adapter surfaces. An adapter may map fields exactly, approximately, derivatively or lossily. The mapping classification is part of the result, so semantic uncertainty is not hidden behind a successful parse.

## v0.7 Verification Thesis

Portable settlement claims need reproducible evidence boundaries. A `COMPATIBLE` result is useful only if another implementation can verify what inputs, evidence, ruleset and canonical result produced it.

OMST v0.7 treats verification as a technical conformance artifact. A verifier can say `VERIFIED`, `INVALID`, `DIFFERENT`, `UNSUPPORTED` or `UNKNOWN`, but it must not convert synthetic examples into issuer evidence, regulatory evidence, market-condition evidence, reserve assurance or authorization to settle.
