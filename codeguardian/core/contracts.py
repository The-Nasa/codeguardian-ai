"""Load the versioned contracts distributed with the package."""

import json
from importlib.resources import files

from jsonschema import Draft202012Validator


def validate_contract(name: str, data: object) -> None:
    schema_file = files("codeguardian.schemas").joinpath(f"{name}.schema.json")
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(data)
