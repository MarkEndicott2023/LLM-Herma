"""
Minimal JWT implementation (HS256 only), pure stdlib.

NOTE ON REALISM: Auth0 signs with RS256 (asymmetric) by default — Auth0 holds
the private key and publishes the public key at /.well-known/jwks.json, so APIs
can VERIFY but never SIGN. We use HS256 (symmetric, shared secret) here purely
to avoid third-party crypto libraries. The JWT *structure* (base64url segments,
signature over header.payload) is identical either way.
"""

import base64
import hashlib
import hmac
import json
import time


def b64url_encode(data: bytes) -> str:
    # base64url: '+' -> '-', '/' -> '_', padding stripped.
    # This is WHY dots can safely delimit the three segments: '.' never
    # appears in the base64url alphabet.
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(segment: str) -> bytes:
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def encode(payload: dict, secret: str) -> str:
    """Mint a signed JWT: header.payload.signature"""
    header = {"alg": "HS256", "typ": "JWT"}
    signing_input = (
        b64url_encode(json.dumps(header, separators=(",", ":")).encode())
        + "."
        + b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    )
    # Signature is computed over the raw bytes of "header.payload"
    sig = hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()
    return signing_input + "." + b64url_encode(sig)


def is_jwt(token: str) -> bool:
    """Structural check — how a server detects an OPAQUE token.

    The server never sees the original /authorize request, so it can't check
    'was an audience param present?'. All it has is the token: if it doesn't
    parse as three base64url segments with a JSON header, it's opaque.
    """
    parts = token.split(".")
    if len(parts) != 3:
        return False
    try:
        json.loads(b64url_decode(parts[0]))
        return True
    except Exception:
        return False


def decode_header(token: str) -> dict:
    """Step 1 of validation: the header must be readable BEFORE any crypto,
    because it tells you which algorithm/key to use."""
    return json.loads(b64url_decode(token.split(".")[0]))


def decode_payload_UNVERIFIED(token: str) -> dict:
    """Anyone can do this — base64url is encoding, NOT encryption.
    Never trust these claims until the signature is verified."""
    return json.loads(b64url_decode(token.split(".")[1]))


def verify_signature(token: str, secret: str) -> bool:
    header_b64, payload_b64, sig_b64 = token.split(".")
    signing_input = f"{header_b64}.{payload_b64}".encode()
    expected = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    return hmac.compare_digest(expected, b64url_decode(sig_b64))


def now() -> int:
    return int(time.time())
