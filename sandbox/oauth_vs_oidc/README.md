# OAuth 2.0 vs OIDC — runnable demo

Pure stdlib, no dependencies:

```
python3 demo.py
```

## The three players

| File | Role | Real-world counterpart |
|---|---|---|
| `auth_server.py` | Authorization Server — mints all tokens, hosts `/userinfo` | Auth0 tenant (`https://acme-prod.us.auth0.com`) |
| `api_server.py` | Resource Server — validates JWTs locally, never mints | Your API (`https://api.acme.com/reports`) |
| `mini_jwt.py` | JWT plumbing — base64url, sign, verify, structural parse | `jsonwebtoken` / `pyjwt` + Auth0's signing keys |

`demo.py` plays the client (SPA / M2M daemon) and narrates four scenarios.

## Concept → code map

- **The two switches** — `AuthServer.login()`: the `if "openid" in scopes`
  block (switch 1, id_token issuance) and the `if audience is not None`
  block (switch 2, access-token format) are visibly independent code paths.
- **No human → no id_token** — `AuthServer.client_credentials()` simply has
  no id_token code path at all. `openid` is filtered out of the scope claim.
- **aud rules** — id_token gets `aud=client_id` (login), access token gets
  `aud=audience` (API identifier). Grep `"aud"` in `auth_server.py`.
- **Opaque detection is structural** — `mini_jwt.is_jwt()`: the API never saw
  the `/authorize` request, it can only inspect the token in hand.
- **Local validation order** — `ResourceAPI.handle()` steps 1–5: parse →
  pin alg → verify signature → iss/aud/exp → scope-vs-operation. The scope
  check is the final step (authenticated ≠ authorized → 403 not 401).
- **`/userinfo` mechanics** — `AuthServer.userinfo()`: Bearer header, no
  scope param, claims fixed by scopes granted at issuance, accepts JWT *and*
  opaque (opaque works *only* there).
- **id-token-to-API bug** — scenario 4: signature verifies fine, rejection is
  the semantic `aud` mismatch at step 4.

## One deliberate simplification

Real Auth0 signs with **RS256** (asymmetric): Auth0 keeps the private key and
publishes the public key at `/.well-known/jwks.json`, so APIs can verify but
can never sign. This demo uses **HS256** (shared secret) to stay
dependency-free — which means `ResourceAPI` *could* technically mint tokens
here. That's exactly the HS256 weakness from your JWT Anatomy sessions. The
validation order and every claim check are identical either way; the only
missing piece is the one-time (cached) JWKS network fetch.

## Things to try breaking

1. **Tamper with a claim:** decode a JWT payload, change `scope`, re-encode it
   without re-signing, send it to the API. Watch step 3 catch it.
2. **Delete `openid` from scenario 2's scope** — confirm the id_token
   disappears while the access token is unaffected (switch independence).
3. **Add a `verbose` print of `decode_payload_UNVERIFIED` before signature
   verification** in `api_server.py` and forge a token — see exactly what an
   API that "checks claims first" would wrongly trust.
4. **Expire a token:** set `ACCESS_TOKEN_TTL = -1` and watch which step fails.
5. **Point the opaque token at `/userinfo` with extra scopes** — confirm you
   can't widen claims after issuance.
