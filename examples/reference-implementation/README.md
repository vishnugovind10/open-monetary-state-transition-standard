# Reference Implementation Flow

This example shows the portable v0.6 workflow:

1. Party A publishes `MoneyProfile`, `SettlementProfile` and `OMST Manifest`.
2. Party B creates a `SettlementRequest`.
3. OMST evaluates money, state, settlement environment, evidence and requirements.
4. OMST returns `Compatibility`, reasons, evidence, transition plan and route.
5. A second implementation consumes the same vectors and returns the same semantic result.

Run:

```bash
omst profile validate examples/profiles/money/eur-x.v06.json
omst settlement-profile examples/settlement-networks/network-a.json
omst exchange --intent examples/tokenized-bond-dvp/settlement-intent.json --money examples/eur-x.json --settlement examples/settlement-networks/network-a.json
omst conformance
```

All files are synthetic reference artifacts, not issuer, regulatory or market-condition evidence.
