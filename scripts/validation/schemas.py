import json

import jsonschema

from validation.paths import SCHEMA_DIRECTORY


def LoadSchema(name):
    return json.loads((SCHEMA_DIRECTORY / name).read_text(encoding="utf-8"))


def ReadDocument(path, schema, problems):
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        problems.append(f"{path} unreadable json")
        return None

    try:
        jsonschema.validate(document, schema)
    except jsonschema.ValidationError:
        problems.append(f"{path} schema violation")
        return None

    return document
