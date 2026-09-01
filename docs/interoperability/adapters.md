# Adapter Profiles

OMST adapter profiles map external representations into OMST concepts without pretending that every field is semantically identical.

## Included Conceptual Adapters

- Generic JSON
- OTAS
- ISO 20022
- ISDA CDM
- FINOS CDM

## Mapping Classifications

- `EXACT`: the external field and OMST field carry the same semantics for the stated scope.
- `APPROXIMATED`: the mapping is usable but loses precision.
- `DERIVED`: the OMST field is computed from one or more external fields.
- `UNSUPPORTED`: the external representation has no available source field.
- `LOSSY`: the mapping drops material semantic information.

## Rule

An adapter may parse data successfully while still producing an uncertain settlement result. Parsing success is not compatibility evidence.
