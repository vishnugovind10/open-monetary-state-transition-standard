import json
from decimal import Decimal
from pathlib import Path
from typing import Any, cast

from jsonschema import Draft202012Validator

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schemas"

def load_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))

def validate_document(path: Path, schema_name: str | None = None) -> list[str]:
    data = load_json(path)
    kind = schema_name or data.get("omst_type") or path.name.split(".")[0]
    schema_path = SCHEMA_DIR / f"{kind}.schema.json"
    if not schema_path.exists():
        matches = list(SCHEMA_DIR.rglob(f"{kind}.schema.json"))
        if matches:
            schema_path = matches[0]
    if not schema_path.exists():
        return [f"schema not found for {path}"]
    validator = Draft202012Validator(load_json(schema_path))
    return [error.message for error in sorted(validator.iter_errors(data), key=str)]

def decimalize(value: object) -> Decimal:
    return Decimal(str(value))
