# Settlement Compatibility

Settlement compatibility evaluates whether a monetary instrument can satisfy an explicit settlement intent under a machine-readable requirement set.

The v0.5 profile is designed for independent reproduction: two conforming implementations given the same settlement intent, money profile, state snapshot, evidence policy and requirement set should produce the same status and reason codes.

## Inputs

- Settlement intent
- Money profile
- Composite money state
- Money requirement set
- Evidence policy
- Evaluation context
- Optional route and transition-plan context

## Output Statuses

- `COMPATIBLE`: all mandatory requirements pass and evidence policy checks pass.
- `CONDITIONALLY_COMPATIBLE`: mandatory requirements pass, but warnings, stale evidence or stated assumptions limit the result.
- `INCOMPATIBLE`: one or more mandatory requirements fail.
- `UNKNOWN`: required state, evidence or profile information is unavailable and the configured assumption policy prevents compatibility inference.

## Reason Codes

Reason codes are machine-readable and stable within a ruleset version. Examples include:

- `ATOMICITY_UNAVAILABLE`
- `FINALITY_MISMATCH`
- `AVAILABILITY_MISMATCH`
- `LATENCY_REQUIREMENT_UNMET`
- `LIQUIDITY_INSUFFICIENT`
- `LIQUIDITY_EVIDENCE_STALE`
- `UNKNOWN_STATE`
- `CONFLICTING_EVIDENCE`

## Reference Scenario

The synthetic EUR 50m tokenized-bond DvP scenario demonstrates the intended behavior:

- `EUR-X` is `COMPATIBLE`.
- `EUR-Y` is `CONDITIONALLY_COMPATIBLE` because liquidity evidence is stale.
- `EUR-Z` is `INCOMPATIBLE` because mandatory settlement requirements fail.

These outcomes are derived from schemas, profiles, state, requirements, evidence policy and rules. They are not hard-coded issuer opinions.

## Boundary

OMST does not execute settlement, custody assets, issue money, provide legal advice, certify compliance or represent actual issuer, regulatory or market-condition evidence. Public examples are synthetic.
