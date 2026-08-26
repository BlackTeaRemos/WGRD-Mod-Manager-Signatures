import re

from blake3 import blake3

FINGERPRINT_PATTERN = re.compile(r"^[0-9a-f]{16}$")

PUBLIC_KEY_BYTES = 32
FINGERPRINT_BYTES = 8
SIGNATURE_BYTES = 64


def DeriveFingerprint(publicKeyBytes):
    digest = blake3(publicKeyBytes).digest()
    return digest[:FINGERPRINT_BYTES].hex()
