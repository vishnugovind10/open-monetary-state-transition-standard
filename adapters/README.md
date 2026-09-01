# Adapters

Adapters map OMST primitives to adjacent standards without claiming equivalence where semantics differ.

Each adapter must document:

- scope
- supported objects
- mapping classification
- lossiness
- limitations
- examples
- tests

Mapping classifications:

- `EXACT`
- `LOSSLESS`
- `LOSSY`
- `DERIVED`
- `APPROXIMATED`
- `UNSUPPORTED`

Adapters are not official integrations unless separately stated by the relevant standards body or project. Live adapters must preserve evidence lineage and avoid silently upgrading declared facts into observed facts.
