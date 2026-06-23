"""
A toy Resource Server — your protected API (e.g. https://api.acme.com/reports).

It never talks to the auth server during a request*. It validates JWT access
tokens entirely LOCALLY, in this exact order:

  1. structural parse  (not a JWT? -> opaque -> can't protect an API with it)
  2. decode header, PIN the algorithm   (alg-confusion defense)
  3. verify signature                   (BEFORE trusting any claim)
  4. check iss / aud / exp              (aud must be OUR OWN identifier)
  5. check scope vs the operation       (authZ: is THIS request allowed?)

(*) In the real RS256 world the one network call is fetching Auth0's JWKS —
once, then cached. With our shared-secret HS256 stand-in there's nothing to
fetch, but step order is identical.
"""

import mini_jwt


class ResourceAPI:
    def __init__(self, identifier: str, issuer: str, verify_secret: str):
        self.identifier = identifier      # this becomes the expected 'aud'
        self.issuer = issuer
        self.verify_secret = verify_secret  # verify-only role (think: public key)
        self.routes = {}                  # (method, path) -> required scope

    def protect(self, method, path, required_scope):
        self.routes[(method, path)] = required_scope

    def handle(self, method, path, authorization_header, verbose=True):
        def step(msg):
            if verbose:
                print(f"      [api] {msg}")

        required_scope = self.routes.get((method, path))
        if required_scope is None:
            return 404, {"error": "not_found"}

        if not authorization_header.startswith("Bearer "):
            return 401, {"error": "missing bearer token"}
        token = authorization_header.removeprefix("Bearer ")

        # 1. structural parse — this is how we detect opaque tokens.
        #    (We never saw the /authorize request, so we can't check whether
        #    an audience param was sent. We only have the token in hand.)
        if not mini_jwt.is_jwt(token):
            step("token does not parse as header.payload.signature -> OPAQUE")
            step("opaque tokens carry no claims we can verify locally -> reject")
            return 401, {"error": "expected a JWT access token (did the client forget the audience param?)"}

        # 2. decode header, pin algorithm. LOCAL.
        header = mini_jwt.decode_header(token)
        step(f"header decoded: {header} (local, no crypto yet)")
        if header.get("alg") != "HS256":
            step(f"alg '{header.get('alg')}' != pinned 'HS256' -> reject (alg-confusion defense)")
            return 401, {"error": "unexpected signing algorithm"}

        # 3. verify signature FIRST — claims are attacker-writable until now. LOCAL.
        if not mini_jwt.verify_signature(token, self.verify_secret):
            step("signature INVALID -> reject before reading any claim")
            return 401, {"error": "invalid signature"}
        step("signature verified (local) -> claims can now be trusted")

        # 4. claim checks. LOCAL.
        claims = mini_jwt.decode_payload_UNVERIFIED(token)  # safe: sig verified
        if claims.get("iss") != self.issuer:
            step(f"iss {claims.get('iss')!r} != {self.issuer!r} -> 401")
            return 401, {"error": "wrong issuer"}
        if claims.get("aud") != self.identifier:
            # The canonical id-token-to-API bug lands here: aud == client_id.
            # Transport (the Bearer header) is agnostic — rejection is
            # SEMANTIC: this token was not minted for this API.
            step(f"aud {claims.get('aud')!r} != our identifier {self.identifier!r} -> 401")
            return 401, {"error": "token not intended for this API (aud mismatch)"}
        if claims.get("exp", 0) <= mini_jwt.now():
            step("token expired -> 401")
            return 401, {"error": "expired"}
        step(f"iss/aud/exp all valid (local). aud={claims['aud']!r} is us.")

        # 5. AuthZ: a real, unexpired token for us is necessary but NOT
        #    sufficient — does it carry the scope for THIS operation?
        granted = claims.get("scope", "").split()
        if required_scope not in granted:
            step(f"scope check: need {required_scope!r}, token has {granted} -> 403")
            return 403, {"error": "insufficient_scope"}  # authenticated, not authorized
        step(f"scope check: {required_scope!r} present -> 200")

        return 200, {"data": f"{method} {path} OK", "sub": claims["sub"]}
