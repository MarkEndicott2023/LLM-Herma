"""
A toy 'Auth0' — the Authorization Server.

It owns the signing secret, the user store, the registered Applications
(clients) and APIs (resource servers). It mints all tokens; resource APIs
only ever VERIFY.

The two independent switches it implements (the whole point of the demo):

  switch 1: human present AND 'openid' in scope  ->  is an id_token issued?
  switch 2: 'audience' param present             ->  access token FORMAT
                                                     (JWT if present, opaque if not)

Neither switch touches the other's token.
"""

import secrets as _secrets

import mini_jwt

# What each OIDC scope contributes to the id_token / userinfo claims.
# 'openid' is the issuance switch + base claims; the others only ENRICH.
SCOPE_TO_CLAIMS = {
    "profile": ["name", "nickname", "picture"],
    "email": ["email", "email_verified"],
}

ID_TOKEN_TTL = 36_000     # 10 hours  (Auth0 default for ID tokens)
ACCESS_TOKEN_TTL = 86_400  # 24 hours (Auth0 default for custom-API access tokens)


class AuthServer:
    def __init__(self, tenant_domain: str):
        self.issuer = f"https://{tenant_domain}/"
        self.signing_secret = "demo-signing-secret-do-not-do-this-in-prod"
        self.users = {}            # username -> {password, claims}
        self.clients = {}          # client_id -> {client_secret, name}
        self.apis = {}             # identifier -> {scopes}
        self.opaque_store = {}     # opaque token -> {sub, granted_scopes}

    # ----- tenant setup (what you'd do in the Auth0 dashboard) -----

    def register_user(self, username, password, claims):
        self.users[username] = {"password": password, "claims": claims}

    def register_client(self, client_id, client_secret, name):
        self.clients[client_id] = {"client_secret": client_secret, "name": name}

    def register_api(self, identifier, scopes):
        self.apis[identifier] = {"scopes": scopes}

    # ----- the token endpoints -----

    def login(self, client_id, username, password, scope, audience=None):
        """Simulates /authorize + code exchange for a HUMAN login.

        Returns the token response dict, shaped like Auth0's
        POST /oauth/token response.
        """
        assert client_id in self.clients, "unknown client_id"
        user = self.users.get(username)
        assert user and user["password"] == password, "bad credentials"

        scopes = scope.split()
        response = {"token_type": "Bearer", "expires_in": ACCESS_TOKEN_TTL}

        # ---- SWITCH 1: id_token — needs a human (we have one) + 'openid' ----
        if "openid" in scopes:
            claims = {
                "iss": self.issuer,
                "sub": user["claims"]["sub"],
                "aud": client_id,  # id_token audience is ALWAYS the client_id
                "exp": mini_jwt.now() + ID_TOKEN_TTL,
                "iat": mini_jwt.now(),
            }
            # profile/email scopes enrich the id_token with more claims
            for s in scopes:
                for claim in SCOPE_TO_CLAIMS.get(s, []):
                    if claim in user["claims"]:
                        claims[claim] = user["claims"][claim]
            # An id_token is ALWAYS a JWT, per the OIDC spec. No exceptions.
            response["id_token"] = mini_jwt.encode(claims, self.signing_secret)

        # ---- SWITCH 2: access token format — decided ONLY by audience ----
        api_scopes = [s for s in scopes if s not in ("openid", "profile", "email")]
        if audience is not None:
            assert audience in self.apis, f"no API registered with identifier {audience}"
            response["access_token"] = mini_jwt.encode(
                {
                    "iss": self.issuer,
                    "sub": user["claims"]["sub"],
                    "aud": audience,  # access token audience = API identifier
                    "azp": client_id,
                    "exp": mini_jwt.now() + ACCESS_TOKEN_TTL,
                    "iat": mini_jwt.now(),
                    "scope": " ".join(scopes),
                },
                self.signing_secret,
            )
        else:
            # No audience -> OPAQUE: a random reference string. The claims it
            # can fetch at /userinfo are FIXED by the scopes granted NOW,
            # at issuance — not by anything sent later.
            token = _secrets.token_urlsafe(24)
            self.opaque_store[token] = {
                "sub": user["claims"]["sub"],
                "granted_scopes": scopes,
            }
            response["access_token"] = token

        response["scope"] = " ".join(scopes) or None
        _ = api_scopes  # (kept for readability; scope claim carries them)
        return response

    def client_credentials(self, client_id, client_secret, scope, audience):
        """Simulates POST /oauth/token with grant_type=client_credentials (M2M).

        NO HUMAN -> NO id_token. Ever. 'openid' in scope is silently ignored,
        because an id_token describes a person who logged in, and nobody did.
        """
        client = self.clients.get(client_id)
        assert client and client["client_secret"] == client_secret, "bad client auth"
        assert audience in self.apis, f"no API registered with identifier {audience}"

        return {
            "token_type": "Bearer",
            "expires_in": ACCESS_TOKEN_TTL,
            "access_token": mini_jwt.encode(
                {
                    "iss": self.issuer,
                    "sub": client_id,        # M2M: sub is the app's own client_id
                    "aud": audience,
                    "azp": client_id,
                    "gty": "client-credentials",
                    "exp": mini_jwt.now() + ACCESS_TOKEN_TTL,
                    "iat": mini_jwt.now(),
                    "scope": " ".join(s for s in scope.split() if s != "openid"),
                },
                self.signing_secret,
            ),
            # note: no "id_token" key. This is correct behavior, not a bug.
        }

    # ----- the /userinfo endpoint (an OIDC addition, not OAuth) -----

    def userinfo(self, authorization_header: str):
        """GET /userinfo

        Auth: 'Authorization: Bearer <access_token>' header. There is NO
        scope query param — the claims returned are fixed by the scopes
        granted at issuance.
        Works for opaque AND JWT access tokens; opaque tokens work ONLY here.
        """
        if not authorization_header.startswith("Bearer "):
            return 401, {"error": "missing bearer token"}
        token = authorization_header.removeprefix("Bearer ")

        if mini_jwt.is_jwt(token):
            if not mini_jwt.verify_signature(token, self.signing_secret):
                return 401, {"error": "invalid signature"}
            payload = mini_jwt.decode_payload_UNVERIFIED(token)
            granted = payload.get("scope", "").split()
            sub = payload["sub"]
        else:
            entry = self.opaque_store.get(token)
            if entry is None:
                return 401, {"error": "unknown token"}
            granted = entry["granted_scopes"]
            sub = entry["sub"]

        if "openid" not in granted:
            return 401, {"error": "token was not granted openid scope"}

        user = next(u for u in self.users.values() if u["claims"]["sub"] == sub)
        claims = {"sub": sub}
        for s in granted:
            for claim in SCOPE_TO_CLAIMS.get(s, []):
                if claim in user["claims"]:
                    claims[claim] = user["claims"][claim]
        return 200, claims
