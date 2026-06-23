
import base64
import json
import hmac
import hashlib
import time

# Base64url encoder/decoder

def b64url_encode(data: bytes) -> str:
    # Goal: encode incoming byte literal without padding
    # Encode -> convert ascii in bytes to str -> strip padding
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")

def b64url_decode(data: str) -> bytes:
    # Decode string into byte literal
    # Fill padding for decoding
    padding = (-len(data) % 4) * "="
    # Decode back to byte literal
    return base64.urlsafe_b64decode(data + padding)

# Basic Assertions
assert b64url_encode(b'{"alg":"HS256"}') == "eyJhbGciOiJIUzI1NiJ9"
assert b64url_decode(b64url_encode(b"any bytes at all!")) == b"any bytes at all!"

###################################################

# Mint a token

def encode(payload: dict, secret: str) -> str:

    # Fixed
    header  = {"alg": "HS256", "typ": "JWT"}

    # Serialize -> encode in bytes -> encode in bash64
    header_bytes = json.dumps(header, separators=(",",":")).encode("utf-8")
    seg1 = b64url_encode(header_bytes)

    # Serialize -> encode in bytes -> encode in bash64
    payload_bytes = json.dumps(payload, separators=(",",":")).encode("utf-8")
    seg2 = b64url_encode(payload_bytes)

    # Construct message array for minting signature
    message_bytes = (seg1 + "." + seg2).encode("utf-8")

    # Minting signature
    secret_bytes = secret.encode("utf-8")
    sig_hmac = hmac.new(key=secret_bytes, msg=message_bytes, digestmod=hashlib.sha256)
    sig = b64url_encode(sig_hmac.digest())

    # Constructing jwt
    jwt = seg1 + "." + seg2 + "." + sig

    return jwt

tok = encode(
    {"iss": "https://acme-demo.us.auth0.example/",
     "sub": "auth0|6841f2",
     "aud": "spa_3xY9kQ"},
    "level1-secret",
)
assert tok == (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJodHRwczovL2FjbWUtZGVtby51cy5hdXRoMC5leGFtcGxlLyIsInN1YiI6ImF1dGgwfDY4NDFmMiIsImF1ZCI6InNwYV8zeFk5a1EifQ"
    ".fuF8HxZdpRaON_qh2bhvrfbMJe2Hpbe0kgDrQHkTF5g"
)

###################################################

# Token verification

def is_jwt(tok) -> str:
    
    tok_lst = tok.split(".")

    if len(tok_lst) == 3:
        pass
    else:
        return False
    try:
        header = b64url_decode(tok_lst[0]).decode("utf-8")
        return True
    except:  
        return False
    
assert is_jwt(tok) is True
assert is_jwt("f71kVhF11Mzdxoarka93QB62lWTlRVlJ") is False   # opaque
assert is_jwt("a.b.c") is False   

def decode_payload_UNVERIFIED(tok: str) -> dict:
    # Processes unverified tokens into a dict
    # I.e. — json.loads deserializes the string
    tok_lst = tok.split(".")
    payload_str = b64url_decode(tok_lst[1]).decode()
    return json.loads(payload_str)

assert decode_payload_UNVERIFIED(tok)["sub"] == "auth0|6841f2"

def verify_signature(tok: str, secret: str) -> bool:
    # Verifies token signature using header, payload, and secret key
    tok_lst = tok.split(".")
    message = (tok_lst[0] + "." + tok_lst[1]).encode("utf-8")
    decoded_sig = hmac.new(secret.encode("utf-8"), message, digestmod=hashlib.sha256).digest()
    new_sig = b64url_encode(decoded_sig)
    return hmac.compare_digest(tok_lst[2], new_sig)

assert verify_signature(tok, "level1-secret") is True
assert verify_signature(tok, "wrong-secret") is False

# Adding payload exp helper
def now() -> int:
    return int(time.time())

assert isinstance(now(), int)

print("ALL THINGS PASS!")