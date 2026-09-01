from pathlib import Path

from omst.io import validate_document


def test_all_examples_validate():
    failures = {}
    for path in Path("examples").rglob("*.json"):
        errors = validate_document(path)
        if errors:
            failures[str(path)] = errors
    assert failures == {}

def test_all_schemas_have_required_shape():
    import json
    for path in Path("schemas").glob("*.schema.json"):
        data = json.loads(path.read_text())
        for key in ["$id","$schema","title","description","type","properties","required","additionalProperties","examples"]:
            assert key in data, path
