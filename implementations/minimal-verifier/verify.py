from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): canonical(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [canonical(item) for item in value]
    return value


def canonical_hash(value: Any) -> str:
    payload = json.dumps(canonical(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def package_fingerprint(package: dict[str, Any]) -> str:
    payload = dict(package)
    payload["integrity"] = {}
    return canonical_hash(payload)


def verify(path: Path) -> dict[str, Any]:
    package = json.loads(path.read_text(encoding="utf-8"))
    reasons: list[str] = []
    if package.get("omst_type") != "evaluation-package":
        reasons.append("not an evaluation package")
    if package.get("ruleset_version") != "omst-core-0.7":
        reasons.append(f"unsupported ruleset {package.get('ruleset_version')}")
    expected = package.get("integrity", {}).get("package_fingerprint")
    actual = package_fingerprint(package)
    if expected != actual:
        reasons.append("package fingerprint mismatch")
    items = package.get("evidence_manifest", {}).get("evidence_items", [])
    if not items:
        reasons.append("evidence manifest contains no items")
    for item in items:
        inline = item.get("inline_content")
        if inline is not None and item.get("content_hash") != canonical_hash(inline):
            reasons.append(f"{item.get('evidence_id')}: evidence hash mismatch")
        if str(item.get("expires_at", "")) <= "2026-09-02T00:00:00Z":
            reasons.append(f"{item.get('evidence_id')}: evidence expired")
    if package.get("canonical_evaluation_result", {}).get("status") != "COMPATIBLE":
        reasons.append("semantic evaluation differs")
    if any(reason.startswith("unsupported ruleset") for reason in reasons):
        status = "UNSUPPORTED"
    elif any("semantic evaluation differs" in reason for reason in reasons):
        status = "DIFFERENT"
    elif reasons:
        status = "INVALID"
    else:
        status = "VERIFIED"
    return {"status": status, "package_fingerprint": actual, "reasons": reasons}


if __name__ == "__main__":
    result = verify(Path(sys.argv[1]))
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "VERIFIED" else 1)
