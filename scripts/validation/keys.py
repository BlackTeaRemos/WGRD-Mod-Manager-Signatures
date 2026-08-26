from validation.fingerprints import (
    DeriveFingerprint,
    FINGERPRINT_PATTERN,
    PUBLIC_KEY_BYTES,
)
from validation.paths import KEYS_DIRECTORY, PLACEHOLDER_NAME
from validation.schemas import LoadSchema, ReadDocument


def ValidateKeyFile(path, schema, problems):
    if not FINGERPRINT_PATTERN.match(path.stem):
        problems.append(f"{path} bad file name")
        return None

    document = ReadDocument(path, schema, problems)
    if document is None:
        return None

    fingerprint = document["fingerprint"]
    if fingerprint != path.stem:
        problems.append(f"{path} fingerprint name mismatch")
        return None

    try:
        publicKeyBytes = bytes.fromhex(document["publicKey"])
    except ValueError:
        problems.append(f"{path} bad hex")
        return None

    if len(publicKeyBytes) != PUBLIC_KEY_BYTES:
        problems.append(f"{path} wrong key length")
        return None

    if DeriveFingerprint(publicKeyBytes) != fingerprint:
        problems.append(f"{path} fingerprint mismatch")
        return None

    return {"fingerprint": fingerprint, "publicKey": document["publicKey"]}


def CollectKeys(problems):
    registered = {}
    seenPublicKeys = {}

    if not KEYS_DIRECTORY.is_dir():
        return registered

    schema = LoadSchema("key.schema.json")

    for path in sorted(KEYS_DIRECTORY.glob("*")):
        if path.name == PLACEHOLDER_NAME:
            continue

        if path.suffix != ".json":
            problems.append(f"{path} unexpected file")
            continue

        record = ValidateKeyFile(path, schema, problems)
        if record is None:
            continue

        publicKey = record["publicKey"]
        if publicKey in seenPublicKeys:
            problems.append(f"{path} duplicate public key")
            continue

        seenPublicKeys[publicKey] = path
        registered[record["fingerprint"]] = publicKey

    return registered
