# Settlement Exchange

OMST v0.6 defines portable settlement exchange objects for counterparties, routers and implementations.

## SettlementRequest

`SettlementRequest` declares the requested settlement, required money properties, amount, deadline and evidence expectations.

## SettlementOffer

`SettlementOffer` declares what a participant or system can offer in response to a request. Offers may include assumptions and validity windows.

## SettlementResponse

`SettlementResponse` records:

- compatibility status
- accepted requirements
- rejected requirements
- conditional requirements
- transition-plan reference
- route or graph snapshot reference
- validity window

Responses are deterministic for the same inputs and ruleset version.

## Boundary

A settlement response is a compatibility result. It is not an instruction to move money and it is not confirmation that settlement occurred.
