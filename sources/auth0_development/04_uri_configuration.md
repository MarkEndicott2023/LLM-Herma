# URI Configuration (Callbacks, Logout URLs, Web Origins, CORS)

**Auth0 docs:** https://auth0.com/docs/get-started/applications/application-settings

Per-application URL allowlists protect against open-redirect and CSRF attacks. Auth0 only redirects users or honors origins listed here.

## Allowed Callback URLs

**Purpose:** Destinations Auth0 may redirect to after `/authorize` succeeds (i.e., the `redirect_uri`).

- Multiple URLs supported, comma-separated.
- The first URL listed is the default callback.
- Production: do not use `localhost`.
- **Validation:** query string and hash fragments are **ignored** during validation.
- **Wildcards:** subdomain wildcards like `https://*.example.com/callback` are supported but **not recommended** in production.
- **Placeholders:** `{organization_name}` for multi-tenant B2B, `{custom_domain.metadata.KEY}` for custom domain metadata.

## Allowed Logout URLs

**Purpose:** Valid destinations for the `returnTo` (or `post_logout_redirect_uri`) parameter on the logout endpoint.

- **Limit: 100 URLs** per application.
- Query strings and hash fragments ignored during validation.
- Wildcards and placeholders supported.
- Tenant-level allowed logout URLs also exist (Tenant Settings → Advanced) for SSO scenarios.

## Allowed Web Origins (Cross-Origin Authentication)

**Purpose:** Origins permitted for:
- Cross-Origin Authentication (embedded login)
- Device Flow
- `web_message` response mode (silent authentication via hidden iframe)

- **Limit: 100 URLs** per application.
- Validation ignores path, query, and hash.
- Wildcards and custom domain placeholders supported.

## Allowed Origins (CORS)

**Purpose:** Origins allowed to make cross-origin requests against Auth0 endpoints (e.g., calls to `/oauth/token` from a browser).

Distinct from Allowed Web Origins:
- **Allowed Web Origins** → cross-origin **authentication** (login-related calls)
- **Allowed Origins (CORS)** → general CORS for browser-originated API calls

## Token Endpoint Authentication Method

For confidential apps, the method used to authenticate to `/oauth/token`:
- `client_secret_post` — secret in form body
- `client_secret_basic` — secret in HTTP Basic Auth header
- `private_key_jwt` — sign a JWT with private key
- `mTLS` — mutual TLS

## Other Application Settings

- **ID Token Expiration** — default 36000 seconds (10 hours)
- **Refresh Token Expiration** — absolute and inactivity timeouts, both toggleable
- **Refresh Token Rotation** — enable + Rotation Overlap Period (leeway in seconds)
- **JWT Signature Algorithm** — HS256 vs RS256 ([[03_jwt_and_signing]])
- **OIDC Conformant** — when enabled, strict OIDC behavior (recommended; usually default for modern apps)

## Exam-relevant numbers (memorize)

| Setting | Limit / Default |
|---|---|
| Allowed Callback URLs | No hard limit documented; comma-separated |
| Allowed Logout URLs | **100** |
| Allowed Web Origins | **100** |
| ID Token default expiration | **36,000 seconds (10 hours)** |
| Custom API access token default expiration | **86,400 seconds (24 hours)** |
| `/userinfo` access token (Implicit flow) | 7,200 seconds (2 hours) |
| `/userinfo` access token (Auth Code/Hybrid) | 86,400 seconds (24 hours) |
