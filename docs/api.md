# API Shape

The reference repository exposes stateless API-shaped endpoints under `/api/v1/*`.

## Endpoints

- `/api/v1/profile/validate`
- `/api/v1/settlement/request`
- `/api/v1/settlement/evaluate`
- `/api/v1/settlement/response`
- `/api/v1/equivalence`
- `/api/v1/plan`
- `/api/v1/route`
- `/api/v1/conformance`
- `/api/v1/adapter/map`

## Discovery

Deployments may publish:

- `/omst-manifest.json`
- `/.well-known/omst.json`

## Boundary

The reference endpoints return synthetic data. They are useful for implementers and demos, but they are not issuer systems, production settlement systems, regulatory evidence or market-condition evidence.
