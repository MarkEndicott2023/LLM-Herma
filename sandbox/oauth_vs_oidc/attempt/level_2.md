# Level 2 — `auth_server.py` spec

```
MODULE  auth_server.py        (the Authorization Server — your toy "Auth0")
IMPORTS  import secrets        (stdlib, for opaque tokens)
         import mini_jwt       (YOUR level-1 module — same folder)
RULES   work in this folder; import your own mini_jwt; don't peek at ../solution/
        it MINTS every token. Resource APIs (level 3) only ever VERIFY.
```

The whole level is one class, `AuthServer`, and it exists to make **two
independent switches** visible in code:

```
switch 1   human present AND 'openid' in scope   ->  is an id_token issued?
switch 2   'audience' param present              ->  access-token FORMAT
                                                     (JWT if present, opaque if not)
```

Neither switch touches the other's token. Hold that as you build.

---

## 0. Prereq patch — `mini_jwt.now()`

Your level-1 `encode()` signed payloads with no timestamps. Real tokens carry
`exp`/`iat`, so the AuthServer stamps them — it needs a clock.

```
add to mini_jwt.py:
  import time
  def now() -> int: return int(time.time())
```

**Checkpoint**

```python
import mini_jwt
assert isinstance(mini_jwt.now(), int)
```

> Side effect to notice: once payloads contain `now()`, tokens stop being
> byte-deterministic. That's why every checkpoint below decodes the token and
> asserts on **claims**, never on an exact token string like level 1 did.

---

## 1. The tenant — registries + setup methods

> PRE-Q: in the Auth0 dashboard you register Users, Applications (clients), and
> APIs as three separate things. Before reading on: which of those three owns
> the value that becomes a JWT's `aud` when an API token is minted?

```
__init__(self, tenant_domain):
  self.issuer         = "https://" + tenant_domain + "/"   # trailing slash matters
  self.signing_secret = "demo-signing-secret-do-not-do-this-in-prod"
  self.users        = {}    # username   -> {"password", "claims"}
  self.clients      = {}    # client_id  -> {"client_secret", "name"}
  self.apis         = {}    # identifier -> {"scopes"}
  self.opaque_store = {}    # opaque token -> {"sub", "granted_scopes"}

register_user(username, password, claims)   # claims holds sub, name, email, ...
register_client(client_id, client_secret, name)
register_api(identifier, scopes)
```

**Checkpoint**

```python
auth0 = AuthServer("acme-demo.us.auth0.example")
assert auth0.issuer == "https://acme-demo.us.auth0.example/"

auth0.register_user("mark", "hunter2", {
    "sub": "auth0|6841f2", "name": "Mark",
    "picture": "https://img.example/mark.png",
    "email": "mark@acme.example", "email_verified": True,
})
auth0.register_client("spa_3xY9kQ", None, "Acme Dashboard (SPA)")
auth0.register_client("m2m_7pLw2R", "shhh-machine-secret", "Invoice Sync Daemon")
auth0.register_api("https://api.acme.example/reports", ["read:reports", "write:reports"])
assert "https://api.acme.example/reports" in auth0.apis
```

---

## 2. `login(client_id, username, password, scope, audience=None)` — SWITCH 1

This one method simulates `/authorize` + the code exchange for a **human**.
Build it in two passes: switch 1 here, switch 2 in section 3.

> PRE-Q (retrieve, no notes): an id_token is the app's *login receipt* — it
> answers "who signed in?". So what is its `aud`: the API it'll be sent to, or
> the app that requested the login? (only one is true, and it's the one that
> makes id-tokens useless as API keys — section 4 of level 1's sibling bug.)

```
assert client_id in self.clients          # unknown client_id
user = self.users.get(username)
assert user and user["password"] == password
scopes = scope.split()
response = {"token_type": "Bearer", "expires_in": ACCESS_TOKEN_TTL}

# ---- SWITCH 1: needs a human (we have one) + 'openid' in scope ----
if "openid" in scopes:
    claims = {
      "iss": self.issuer,
      "sub": user["claims"]["sub"],
      "aud": client_id,                 # <- id_token aud is ALWAYS the client_id
      "exp": mini_jwt.now() + ID_TOKEN_TTL,
      "iat": mini_jwt.now(),
    }
    # profile/email scopes ENRICH the id_token; openid alone is just identity
    for s in scopes:
      for claim in SCOPE_TO_CLAIMS.get(s, []):
        if claim in user["claims"]:
          claims[claim] = user["claims"][claim]
    response["id_token"] = mini_jwt.encode(claims, self.signing_secret)  # id_token is ALWAYS a JWT
```

Constants + the scope→claims map, near the top of the file:

```python
SCOPE_TO_CLAIMS = {
    "profile": ["name", "nickname", "picture"],
    "email":   ["email", "email_verified"],
}
ID_TOKEN_TTL     = 36_000    # 10h
ACCESS_TOKEN_TTL = 86_400    # 24h
```

**Checkpoint** (no audience yet → only the id_token half is exercised)

```python
resp = auth0.login("spa_3xY9kQ", "mark", "hunter2", scope="openid profile email")
assert mini_jwt.is_jwt(resp["id_token"])
idp = mini_jwt.decode_payload_UNVERIFIED(resp["id_token"])
assert idp["aud"] == "spa_3xY9kQ"            # client_id, NOT an API
assert idp["sub"] == "auth0|6841f2"
assert idp["name"] == "Mark"                 # profile enriched it
assert idp["email"] == "mark@acme.example"   # email enriched it
assert mini_jwt.verify_signature(resp["id_token"], auth0.signing_secret)
```

```
DEBUG  name/email missing  -> SCOPE_TO_CLAIMS loop or the user's claims dict
       aud == an API id     -> you copied the access-token rule; id_token aud = client_id
```

---

## 3. `login(...)` continued — SWITCH 2 (access-token format)

> PRE-Q: an opaque token is `f71kVhF11Mzdxoarka93QB62lWTlRVlJ` — a random
> reference string with nothing to decode. A JWT carries its claims inline.
> Which one can your *API* validate without phoning home? And so: which single
> input decides that the SPA gets the validatable one — the scope, or the
> `audience`?

Append below switch 1, **same method**:

```
# ---- SWITCH 2: format decided ONLY by `audience`, never by scope ----
if audience is not None:
    assert audience in self.apis            # no API registered with that identifier
    response["access_token"] = mini_jwt.encode({
        "iss": self.issuer,
        "sub": user["claims"]["sub"],
        "aud": audience,                    # <- access-token aud = the API identifier
        "azp": client_id,                   # authorized party = the app that asked
        "exp": mini_jwt.now() + ACCESS_TOKEN_TTL,
        "iat": mini_jwt.now(),
        "scope": " ".join(scopes),          # scopes travel INSIDE the JWT
    }, self.signing_secret)
else:
    # no audience -> OPAQUE reference string; its claims are FROZEN at issuance
    token = secrets.token_urlsafe(24)
    self.opaque_store[token] = {"sub": user["claims"]["sub"], "granted_scopes": scopes}
    response["access_token"] = token

response["scope"] = " ".join(scopes) or None
return response
```

**Checkpoint A — switch 2 OFF (the section-2 call): access token is OPAQUE**

```python
assert not mini_jwt.is_jwt(resp["access_token"])     # random string, not 3 segments
assert resp["access_token"] in auth0.opaque_store
```

**Checkpoint B — switch 2 ON: access token is a JWT, and note the TWO audiences**

```python
resp2 = auth0.login("spa_3xY9kQ", "mark", "hunter2",
                    scope="openid profile email read:reports",
                    audience="https://api.acme.example/reports")

# switch 1 is UNCHANGED — same id_token rule, still aud == client_id
assert mini_jwt.decode_payload_UNVERIFIED(resp2["id_token"])["aud"] == "spa_3xY9kQ"

# switch 2 flipped the ACCESS token to a JWT aimed at the API
assert mini_jwt.is_jwt(resp2["access_token"])
ap = mini_jwt.decode_payload_UNVERIFIED(resp2["access_token"])
assert ap["aud"] == "https://api.acme.example/reports"   # the API, not the client
assert ap["azp"] == "spa_3xY9kQ"
assert ap["scope"] == "openid profile email read:reports"
assert mini_jwt.verify_signature(resp2["access_token"], auth0.signing_secret)
```

> Say it back: the id_token's `aud` is `spa_3xY9kQ`, the access token's `aud`
> is the API identifier. Same login, same user, two different audiences — that
> mismatch is exactly what blows up when someone sends the id_token to the API.

---

## 4. `client_credentials(client_id, client_secret, scope, audience)` — M2M

> PRE-Q: a nightly invoice daemon authenticates with its own `client_secret`
> and asks for `scope="openid read:reports"`. No browser, no person. What does
> the `openid` do here? (trick: who would the id_token describe?)

```
client = self.clients.get(client_id)
assert client and client["client_secret"] == client_secret   # bad client auth
assert audience in self.apis

return {
  "token_type": "Bearer",
  "expires_in": ACCESS_TOKEN_TTL,
  "access_token": mini_jwt.encode({
      "iss": self.issuer,
      "sub": client_id,                 # <- M2M: sub is the APP's own client_id
      "aud": audience,
      "azp": client_id,
      "gty": "client-credentials",
      "exp": mini_jwt.now() + ACCESS_TOKEN_TTL,
      "iat": mini_jwt.now(),
      "scope": " ".join(s for s in scope.split() if s != "openid"),  # openid FILTERED OUT
  }, self.signing_secret),
  # NO "id_token" key. There's no human to describe. This is correct, not a bug.
}
```

**Checkpoint**

```python
resp3 = auth0.client_credentials("m2m_7pLw2R", "shhh-machine-secret",
                                 scope="openid read:reports",
                                 audience="https://api.acme.example/reports")
assert "id_token" not in resp3                 # no human -> no id_token, ever
cp = mini_jwt.decode_payload_UNVERIFIED(resp3["access_token"])
assert cp["sub"] == "m2m_7pLw2R"               # sub == client_id, not a user
assert cp["gty"] == "client-credentials"
assert cp["scope"] == "read:reports"           # openid silently dropped
assert "openid" not in cp["scope"].split()
```

```
DEBUG  'openid' still in scope claim -> your filter ran on the wrong variable
       sub is a username/auth0|...   -> M2M sub must be the client_id
```

---

## 5. `userinfo(authorization_header)` — the OIDC-only endpoint

> PRE-Q: the request is literally `GET /userinfo` with header
> `Authorization: Bearer <token>` and **no scope param at all**. So where do the
> returned claims come from — something the caller sends now, or something fixed
> earlier? And which token types should this accept: JWT, opaque, or both?

```
if not header.startswith("Bearer "):  return 401, {"error": "missing bearer token"}
token = header.removeprefix("Bearer ")

if mini_jwt.is_jwt(token):
    if not mini_jwt.verify_signature(token, self.signing_secret):
        return 401, {"error": "invalid signature"}
    payload = mini_jwt.decode_payload_UNVERIFIED(token)
    granted = payload.get("scope", "").split()
    sub     = payload["sub"]
else:
    entry = self.opaque_store.get(token)
    if entry is None:  return 401, {"error": "unknown token"}
    granted = entry["granted_scopes"]      # <- claims FROZEN at issuance
    sub     = entry["sub"]

if "openid" not in granted:  return 401, {"error": "token was not granted openid scope"}

user = next(u for u in self.users.values() if u["claims"]["sub"] == sub)
claims = {"sub": sub}
for s in granted:
    for claim in SCOPE_TO_CLAIMS.get(s, []):
        if claim in user["claims"]:
            claims[claim] = user["claims"][claim]
return 200, claims
```

**Checkpoint — the opaque token works ONLY here; JWT works too; openid is required**

```python
# the OPAQUE token from section 3's `resp` resolves its frozen scopes here
status, claims = auth0.userinfo(f"Bearer {resp['access_token']}")
assert status == 200
assert claims["sub"]  == "auth0|6841f2"
assert claims["name"] == "Mark"
assert claims["email"] == "mark@acme.example"

# a JWT access token works at /userinfo as well
assert auth0.userinfo(f"Bearer {resp2['access_token']}")[0] == 200

# no/garbage bearer -> 401
assert auth0.userinfo("garbage")[0] == 401

# a token granted WITHOUT openid cannot widen later -> 401
resp_no_oidc = auth0.login("spa_3xY9kQ", "mark", "hunter2", scope="profile")
assert auth0.userinfo(f"Bearer {resp_no_oidc['access_token']}")[0] == 401

# the M2M token (openid filtered out at mint) -> 401 here, never reaches user lookup
assert auth0.userinfo(f"Bearer {resp3['access_token']}")[0] == 401
```

```
DEBUG  opaque token 500s/KeyErrors -> you tried to decode it as a JWT;
       branch on mini_jwt.is_jwt FIRST
```

---

## Done?

All checkpoints pass → tell me. Then:

```
1. quiz: trace WHY resp2's id_token and access_token carry different `aud`s,
   from your own code — no notes
2. break it: take resp2["id_token"], send it where an access token belongs,
   predict the failure BEFORE level 3 builds the API that catches it
3. unlock level_3.md — ResourceAPI: the 5-step local validation order,
   alg-pinning (alg-confusion defense), and the aud-mismatch 401
   (needs one more mini_jwt helper: decode_header)
```
