# JWT, Signing Algorithms, and JWKS

**Auth0 docs:** https://auth0.com/docs/secure/tokens/json-web-tokens · https://auth0.com/docs/get-started/applications/signing-algorithms

## What is a JWT?

JSON Web Token (RFC 7519) — "a compact and self-contained way for securely transmitting information between parties as a JSON object."

Auth0-issued JWTs are **JSON Web Signatures (JWS)** — signed, not encrypted. **Never store sensitive information in a JWT**; the content is plaintext (just base64url-encoded) even though the signature prevents tampering.

## JWT Structure

A JWT is three base64url-encoded segments separated by dots: `header.payload.signature`

### Header
```json
{ "alg": "RS256", "typ": "JWT", "kid": "abc123..." }
```
- `alg` — signing algorithm
- `typ` — type
- `kid` — key ID, used by the verifier to pick the correct public key from the JWKS

### Payload (Claims)
Three claim categories:
- **Registered claims** — IANA-registered, standardized: `iss`, `sub`, `aud`, `exp`, `iat`, `nbf`, `jti`
- **Public claims** — defined in published standards (e.g., OIDC standard claims like `email`, `name`)
- **Private claims** — custom claims; in Auth0 these must be namespaced (e.g., `https://myapp.example.com/role`) to avoid being stripped

### Signature
Computed over `base64url(header) + "." + base64url(payload)` with the configured algorithm and key.

## Signing Algorithms

### RS256 (RSA SHA-256) — **recommended**
- **Asymmetric.** Auth0 holds the private key; consumers verify with the public key.
- Public key is published at the **JWKS endpoint** (see below).
- Supports key rotation without redeploying clients.

### HS256 (HMAC SHA-256)
- **Symmetric.** Same secret signs and verifies.
- The secret IS the client secret (for app tokens) or the API signing secret.
- Anyone with the secret can both verify *and forge* tokens — never use with public clients.

### PS256 (RSA-PSS SHA-256)
- Asymmetric like RS256 but produces a different signature each time for the same payload (probabilistic). Less commonly used in Auth0.

### Auth0's recommendation
RS256 strongly preferred because:
1. Only Auth0 (private key holder) can sign; anyone with the public key can verify.
2. Key rotation is supported without client redeploys.
3. No shared-secret distribution problem.

## JWKS (JSON Web Key Set)

Public keys for RS256 verification are published at:

```
https://YOUR_DOMAIN/.well-known/jwks.json
```

The JWKS contains an array of public keys, each with a `kid`. When validating a token:
1. Read the `kid` from the JWT header.
2. Look up the matching key in JWKS.
3. Verify the signature with that key.

This enables seamless key rotation — Auth0 can publish a new key with a new `kid`, and clients pick it up automatically.

## JWT Validation Steps (mandatory before trusting any claim)

1. **Signature** — verify with correct key/algorithm
2. **`iss` (issuer)** — matches `https://YOUR_DOMAIN/`
3. **`aud` (audience)** — for ID tokens: matches your client_id. For access tokens: matches the API identifier.
4. **`exp` (expiration)** — current time < exp
5. **`iat` (issued at)** — sanity-check (not in the future)
6. **`nonce`** — for ID tokens from interactive flows: matches the nonce you sent
7. For access tokens with RBAC: check `permissions` or `scope` claim before authorizing the operation

## How Auth0 Uses JWTs

- **ID Tokens** — always JWTs (per OIDC spec). For authentication / user info caching. Never sent to APIs.
- **Access Tokens** — JWT format when an audience is specified (custom API). Opaque format when calling `/userinfo` with no audience.
- **Refresh Tokens** — opaque strings, not JWTs.
- **Logout Tokens** (back-channel logout) — JWTs containing `sid` claim.

See [[09_tokens]] for token lifecycle details.
