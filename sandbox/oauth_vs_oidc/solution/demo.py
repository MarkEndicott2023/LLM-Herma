"""
OAuth 2.0 vs OIDC — runnable walkthrough.

    python3 demo.py

Four scenarios:
  1. Human login, openid scope, NO audience  -> id_token (JWT) + OPAQUE access token -> /userinfo
  2. Human login, openid scope, WITH audience -> id_token (JWT) + JWT access token -> local validation
  3. M2M client_credentials (openid requested!) -> access token ONLY, no id_token
  4. The classic bug: sending the id_token to an API -> 401 aud mismatch
"""

import json

import mini_jwt
from auth_server import AuthServer
from api_server import ResourceAPI


def banner(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def show_token(label, token):
    if mini_jwt.is_jwt(token):
        print(f"   {label}: JWT  {token[:38]}...")
        print(f"      decoded payload: {json.dumps(mini_jwt.decode_payload_UNVERIFIED(token))}")
    else:
        print(f"   {label}: OPAQUE  {token}")
        print("      (random reference string — no segments, nothing to decode)")


# ---------------------------------------------------------------- tenant setup
auth0 = AuthServer("acme-demo.us.auth0.example")          # the Authorization Server
auth0.register_user("mark", "hunter2", {
    "sub": "auth0|6841f2", "name": "Mark", "picture": "https://img.example/mark.png",
    "email": "mark@acme.example", "email_verified": True,
})
auth0.register_client("spa_3xY9kQ", None, "Acme Dashboard (SPA)")
auth0.register_client("m2m_7pLw2R", "shhh-machine-secret", "Invoice Sync Daemon")
auth0.register_api("https://api.acme.example/reports", ["read:reports", "write:reports"])

reports_api = ResourceAPI(
    identifier="https://api.acme.example/reports",
    issuer=auth0.issuer,
    verify_secret=auth0.signing_secret,   # real world: fetches PUBLIC key via JWKS
)
reports_api.protect("GET", "/reports", required_scope="read:reports")


# ------------------------------------------------------------------ scenario 1
banner("SCENARIO 1 — human login, scope='openid profile email', NO audience\n"
       "switch 1 ON (human + openid) -> id_token | switch 2 OFF -> opaque access token")

resp = auth0.login("spa_3xY9kQ", "mark", "hunter2", scope="openid profile email")
show_token("id_token     ", resp["id_token"])
show_token("access_token ", resp["access_token"])

print("\n   The opaque token is useless at our API:")
status, body = reports_api.handle("GET", "/reports", f"Bearer {resp['access_token']}")
print(f"   -> API says {status}: {body['error']}")

print("\n   ...but it works at /userinfo (Bearer header, NO scope param —")
print("   claims are fixed by the scopes granted AT ISSUANCE):")
status, claims = auth0.userinfo(f"Bearer {resp['access_token']}")
print(f"   -> /userinfo {status}: {json.dumps(claims)}")


# ------------------------------------------------------------------ scenario 2
banner("SCENARIO 2 — same login + audience='https://api.acme.example/reports'\n"
       "switch 1 unchanged -> same id_token | switch 2 ON -> JWT access token")

resp2 = auth0.login("spa_3xY9kQ", "mark", "hunter2",
                    scope="openid profile email read:reports",
                    audience="https://api.acme.example/reports")
show_token("id_token     ", resp2["id_token"])
show_token("access_token ", resp2["access_token"])
print("\n   Note the two different audiences:")
print(f"      id_token     aud = {mini_jwt.decode_payload_UNVERIFIED(resp2['id_token'])['aud']!r}  (client_id)")
print(f"      access_token aud = {mini_jwt.decode_payload_UNVERIFIED(resp2['access_token'])['aud']!r}  (API identifier)")

print("\n   The API validates it LOCALLY, step by step:")
status, body = reports_api.handle("GET", "/reports", f"Bearer {resp2['access_token']}")
print(f"   -> API says {status}: {json.dumps(body)}")

print("\n   Same token, but a route needing a scope we weren't granted:")
reports_api.protect("POST", "/reports", required_scope="write:reports")
status, body = reports_api.handle("POST", "/reports", f"Bearer {resp2['access_token']}", verbose=False)
print(f"   -> API says {status}: {body['error']}   (401 = not valid here; 403 = valid but not allowed)")


# ------------------------------------------------------------------ scenario 3
banner("SCENARIO 3 — M2M: grant_type=client_credentials, scope INCLUDES 'openid'\n"
       "no human -> no id_token, regardless of scope. Not a bug.")

resp3 = auth0.client_credentials("m2m_7pLw2R", "shhh-machine-secret",
                                 scope="openid read:reports",
                                 audience="https://api.acme.example/reports")
print(f"   response keys: {sorted(resp3.keys())}   <- no 'id_token', openid ignored")
show_token("access_token ", resp3["access_token"])
print("   note: sub == the app's own client_id, and gty='client-credentials'")

status, body = reports_api.handle("GET", "/reports", f"Bearer {resp3['access_token']}", verbose=False)
print(f"\n   The daemon calls the API -> {status}: {json.dumps(body)}")


# ------------------------------------------------------------------ scenario 4
banner("SCENARIO 4 — the classic bug: sending the ID TOKEN to the API")

print("   The id_token from scenario 2 is a perfectly valid JWT, correctly signed")
print("   by the same tenant. The Bearer header happily transports it. And yet:\n")
status, body = reports_api.handle("GET", "/reports", f"Bearer {resp2['id_token']}")
print(f"   -> API says {status}: {body['error']}")
print("\n   Rejection is SEMANTIC, not transport: aud=client_id marks it as the")
print("   app's login receipt (authN). It carries no scopes — it cannot authorize")
print("   anything. Send the ACCESS token to APIs; the id_token stays in the app.")

print()
