# Minimal Verifier

This verifier is intentionally isolated from the Python reference implementation.

It does not import `omst`. It reads a portable `EvaluationPackage`, recalculates canonical hashes, checks evidence item hashes and ruleset support, and returns a verification status.

```bash
python implementations/minimal-verifier/verify.py examples/verification/valid-package.json
```
