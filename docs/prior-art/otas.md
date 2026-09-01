# OTAS Relationship

```mermaid
flowchart LR
    ASSET[Tokenised Asset]
    OTAS[OTAS]
    MONEY[Digital Money]
    OMST[OMST]
    TX[Institutional Transaction]
    ASSET --> OTAS
    MONEY --> OMST
    OTAS --> TX
    OMST --> TX
```

OTAS can describe the capabilities of the asset being settled. OMST can describe the state and transition properties of the monetary leg. This repository does not claim affiliation or formal compatibility.
