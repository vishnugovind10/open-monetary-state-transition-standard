from pathlib import Path

from omst.io import validate_document


def test_all_examples_validate():
    failures = {}
    for path in Path("examples").rglob("*.json"):
        errors = validate_document(path)
        if errors:
            failures[str(path)] = errors
    assert failures == {}


def test_all_conformance_vectors_validate():
    failures = {}
    for path in Path("conformance/vectors").rglob("*.json"):
        errors = validate_document(path)
        if errors:
            failures[str(path)] = errors
    assert failures == {}

def test_all_schemas_have_required_shape():
    import json
    for path in Path("schemas").rglob("*.schema.json"):
        data = json.loads(path.read_text())
        for key in ["$id","$schema","title","description","type","properties","required","additionalProperties","examples"]:
            assert key in data, path


def test_settlement_intent_example_validates():
    assert validate_document(Path("examples/tokenized-bond-dvp/settlement-intent.json")) == []
