# OMST Explorer

OMST Explorer is the v0.4 web interface for inspecting the reference model with synthetic public data.

It is designed as a practitioner-facing workbench rather than a marketing page. The first screen exposes instrument state, settlement evaluation, monetary equivalence, the money graph, stress scenarios and conformance status.

## Scope

The Explorer supports:

- instrument search and state inspection
- synthetic settlement compatibility checks
- monetary equivalence verdicts
- graph-based route inspection
- stress scenario selection
- conformance status inspection

## Evidence Boundary

All Explorer data is synthetic. It is not issuer evidence, regulatory evidence, market-condition evidence, legal advice, credit analysis or proof that any real-world instrument is equivalent to another.

The Explorer is a reference implementation for standard primitives. Production deployments must connect it to governed data sources, independent conformance checks and institution-specific controls.

## Local Use

```bash
npm install
npm run web:build
npm run web:test
npm run web:dev
```

The app is deployed from the `web/` source tree using the root `vercel.json`.
