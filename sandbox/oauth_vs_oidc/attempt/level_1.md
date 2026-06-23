# Level 1 — `mini_jwt.py` spec

```
MODULE  mini_jwt.py          (build this first — auth/api servers sit on top)
IMPORTS stdlib only: base64, hashlib, hmac, json
RULES   work in this folder; don't peek at ../solution/; verify via checkpoints
```

---

## 1. `b64url_encode(data: bytes) -> str`

> PRE-Q: why can `.` safely delimit JWT segments? (same reason base64*url* exists)

```
encode data with the URL-safe base64 alphabet
strip trailing '=' padding            # real JWTs do
return as str
```

**Checkpoint**

```python
assert b64url_encode(b'{"alg":"HS256"}') == "eyJhbGciOiJIUzI1NiJ9"
```

---

## 2. `b64url_decode(segment: str) -> bytes`

```
re-pad: append '=' until len(segment) % 4 == 0    # one-liner: '=' * (-len(s) % 4)
decode with the URL-safe alphabet
return bytes
```

**Checkpoint**

```python
assert b64url_decode(b64url_encode(b"any bytes at all!")) == b"any bytes at all!"
```

---

## 3. `encode(payload: dict, secret: str) -> str`

> PRE-Q (retrieve, no notes): which *exact bytes* does the signature cover?
> Not the decoded JSON — the encoded segments.

```
header  = {"alg": "HS256", "typ": "JWT"}          # exactly this, in this order
seg1    = b64url_encode(compact_json(header))     # compact: separators=(",", ":")
seg2    = b64url_encode(compact_json(payload))    # don't sort keys
sig     = HMAC_SHA256(key=secret, msg=seg1 + "." + seg2)   # hmac.new(...).digest()
seg3    = b64url_encode(sig)
return  seg1 + "." + seg2 + "." + seg3
```

**Checkpoint** (deterministic — no timestamps)

```python
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
```

```
DEBUG  seg1/seg2 wrong → JSON serialization (compactness / key order)
       seg3 only wrong → HMAC input or key
```

---

## 4. `is_jwt(token: str) -> bool`

> PRE-Q: this is how an API tells JWT from opaque. Why can't it just check
> whether the client sent an `audience` param? (you corrected this one yesterday)

```
structural check, two properties:
  1. token splits on "." into exactly 3 segments
  2. segment 1 b64url-decodes to valid JSON      # wrap in try/except — garbage must not crash
return both true
```

**Checkpoint**

```python
assert is_jwt(tok) is True
assert is_jwt("f71kVhF11Mzdxoarka93QB62lWTlRVlJ") is False   # opaque
assert is_jwt("a.b.c") is False                               # 3 segments, no JSON header
```

---

## 5. `decode_payload_UNVERIFIED(token: str) -> dict`

```
split on "." → take segment 2
b64url_decode → json.loads → return dict
NO verification of any kind                      # the name is the point
```

> Say out loud: why must this exist (debuggers; claim-checks *after* verify),
> and why is its output attacker-writable until step 6 passes?
> base64url is encoding, not encryption.

**Checkpoint**

```python
assert decode_payload_UNVERIFIED(tok)["sub"] == "auth0|6841f2"
```

---

## 6. `verify_signature(token: str, secret: str) -> bool`

> PRE-Q (HS256 vs RS256, you've drilled it): with HS256, do you *recompute the
> signature* or *recompute a hash to compare*? Which would RS256 be?

```
split token → seg1, seg2, seg3
expected = b64url_encode(HMAC_SHA256(secret, seg1 + "." + seg2))   # same math as encode()
return hmac.compare_digest(expected, seg3)       # not == ; look up why (timing attack)
```

**Checkpoint — including your first forgery**

```python
assert verify_signature(tok, "level1-secret") is True
assert verify_signature(tok, "wrong-secret") is False

# BE the attacker: rebuild tok with payload sub="auth0|EVIL" but the ORIGINAL
# signature, using your own b64url helpers. verify_signature must return False.
```

```
DEBUG  tampered token verifies → your "which bytes get signed" wiring is wrong
```

---

## Done?

All checkpoints pass → tell me. Then:

```
1. quiz on a couple of "why"s from your own code
2. unlock level_2.md — AuthServer: the two switches, /userinfo, M2M endpoint
```
