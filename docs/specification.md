# OMST v0.6 Specification

OMST defines machine-readable primitives for describing digital money and determining whether it can satisfy settlement requirements across heterogeneous financial systems.

v0.6 adds a portable interoperability layer:

- `MoneyProfile` lifecycle metadata and canonical fingerprints.
- `SettlementProfile`, `ParticipantProfile`, `SettlementNetworkProfile` and `InteroperabilityProfile`.
- `SettlementRequest`, `SettlementOffer` and `SettlementResponse`.
- `MoneyGraphSnapshot` route and fallback-route evidence.
- Adapter mappings for generic JSON, OTAS, ISO 20022, ISDA CDM and FINOS CDM.
- `omst-manifest.json` and `.well-known/omst.json` discovery.
- Conformance 2.0 profiles covering core, money, state, transition, evidence, settlement, compatibility, routing and interoperability behavior.

See the repository root `SPECIFICATION.md` for the full normative text.
