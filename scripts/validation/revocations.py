import nacl.exceptions
import nacl.signing

from validation.fingerprints import FINGERPRINT_PATTERN, SIGNATURE_BYTES
from validation.paths import PLACEHOLDER_NAME, REVOKED_DIRECTORY
from validation.schemas import LoadSchema, ReadDocument

SIGNABLE_PREFIX = "wgrd-revoke-v1"


def RevocationSignable(document):
    fields = [
        SIGNABLE_PREFIX,
        document["fingerprint"],
        document["revokedAt"],
        document["reason"],
    ]

    return "\n".join(fields).encode("utf-8")


def CarriesSelfSignature(path, document, publicKeyHex, problems):
    signatureField = document.get("signature")
    if signatureField is None:
        return False

    try:
        signatureBytes = bytes.fromhex(signatureField)
    except ValueError:
        problems.append(f"{path} bad signature hex")
        return False

    if len(signatureBytes) != SIGNATURE_BYTES:
        problems.append(f"{path} wrong signature length")
        return False

    verifier = nacl.signing.VerifyKey(bytes.fromhex(publicKeyHex))

    try:
        verifier.verify(RevocationSignable(document), signatureBytes)
    except nacl.exceptions.BadSignatureError:
        problems.append(f"{path} signature invalid")
        return False

    return True


def ValidateRevocationFile(path, schema, registered, requireSignature, problems):
    if not FINGERPRINT_PATTERN.match(path.stem):
        problems.append(f"{path} bad file name")
        return

    document = ReadDocument(path, schema, problems)
    if document is None:
        return

    fingerprint = document["fingerprint"]
    if fingerprint != path.stem:
        problems.append(f"{path} fingerprint name mismatch")
        return

    if fingerprint not in registered:
        problems.append(f"{path} revokes unknown key")
        return

    signed = CarriesSelfSignature(path, document, registered[fingerprint], problems)

    if not signed and requireSignature:
        problems.append(f"{path} revocation unauthorised")


def CollectRevocations(registered, requireSignature, problems):
    if not REVOKED_DIRECTORY.is_dir():
        return

    schema = LoadSchema("revocation.schema.json")

    for path in sorted(REVOKED_DIRECTORY.glob("*")):
        if path.name == PLACEHOLDER_NAME:
            continue

        if path.suffix != ".json":
            problems.append(f"{path} unexpected file")
            continue

        ValidateRevocationFile(path, schema, registered, requireSignature, problems)
