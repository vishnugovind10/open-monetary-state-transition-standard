# Building an Independent Verifier

An independent OMST verifier should start with the v0.7 conformance vectors:

```bash
omst verify examples/verification/valid-package.json
python implementations/minimal-verifier/verify.py examples/verification/valid-package.json
npm run verify
```

Required behavior:

- accept `examples/verification/valid-package.json` as `VERIFIED`
- reject changed package content as `INVALID`
- reject changed evidence hashes as `INVALID`
- classify changed canonical result semantics as `DIFFERENT`
- classify unsupported rulesets as `UNSUPPORTED`
- avoid treating synthetic examples as issuer, regulatory or market-condition evidence

The minimal verifier under `implementations/minimal-verifier/` is intentionally isolated from the Python package so implementers can inspect the verification algorithm without relying on the reference library imports.
