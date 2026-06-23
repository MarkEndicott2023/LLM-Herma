# Tokens: ID, Access, Refresh

**Auth0 docs:**
- https://auth0.com/docs/secure/tokens/id-tokens
- https://auth0.com/docs/secure/tokens/access-tokens
- https://auth0.com/docs/secure/tokens/refresh-tokens
- https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation

Auth0 issues three token types from successful flows.

## ID Token

**Purpose:** Authentication. Caches user identity info for the application.

- **Always a JWT** (per OIDC spec).
- Issued when the request includes `openid` scope.
- **Default expiration: 36,000 seconds (10 hours).** Configurable per app.
- **Never send to APIs.** ID tokens are for the app's own consumption.
- The audience (`aud`) is your `client_id`.

### Standard claims (with `openid` scope)
`iss`, `sub` (user ID), `aud`, `exp`, `iat`, `auth_time`, `nonce` (if you sent one), `azp` (if multiple audiences).

### Adding more claims
Request additional scopes: `profile`, `email`, `address`, `phone`. See [[01_iam_fundamentals]] for the full mapping.

### Custom claims via Actions
Use a Post-Login Action to add **namespaced** custom claims:
```js
api.idToken.setCustomClaim("https://myapp.example.com/role", "admin");
```
Non-namespaced custom claims will be stripped unless they match an OIDC standard claim.

## Access Token

**Purpose:** Authorization. Passed to APIs to authorize requests.

### Two formats
| Format | When | Validation |
|---|---|---|
| **JWT** | When you specify `audience` (custom API) or use Management API | Self-contained — verify signature, claims locally |
| **Opaque** | No audience specified — token only works at `/userinfo` | Call `/userinfo` to "validate" by use |

> "Make sure that you validate an access token before assuming that its contents can be trusted."

### Standard JWT access token claims
- `iss` — issuer
- `sub` — user ID (for user-context tokens; for M2M this is the app's client_id)
- `aud` — API identifier (audience)
- `azp` — authorized party (client_id)
- `exp`, `iat` — timing
- `scope` — space-separated list of granted scopes (e.g., `openid profile read:patients`)
- `gty` — grant type (`client-credentials`, `password`, etc., for non-user-interactive tokens)
- `permissions` — array of strings, **present only if** the API has "Add Permissions in the Access Token" enabled and RBAC is on (see [[14_rbac]])

### Default expirations
- **Custom API access token: 86,400 seconds (24 hours).** Configurable per API.
- `/userinfo` (Implicit flow): 7,200 sec (2 hr)
- `/userinfo` (Auth Code / Hybrid): 86,400 sec (24 hr)

### Token size variability
Auth0 docs note that authorization code and access token sizes are variable. Apps must handle this — particularly in browser cookie storage which has size limits.

## Refresh Token

**Purpose:** Get new access tokens (and ID tokens) without the user re-authenticating.

### Requesting refresh tokens
- Include `offline_access` scope in `/authorize`, OR
- Enable **Allow Offline Access** on the API.
- App must be OIDC-conformant (set automatically when audience is specified or OIDC Conformant flag is on).

### Using a refresh token
```
POST /oauth/token
grant_type=refresh_token
&client_id=YOUR_CLIENT_ID
&client_secret=YOUR_CLIENT_SECRET   ← confidential only
&refresh_token=THE_REFRESH_TOKEN
&scope=openid profile email         ← optional; can request narrower scope
```

### Storage rules
- **Confidential apps:** server-side, encrypted at rest.
- **Native apps:** secure platform storage (Keychain / Keystore).
- **SPAs:** memory by default; local storage with rotation if needed.

### Limits
- **Max 200 active refresh tokens per user per application.** Exceeding triggers oldest-first revocation.

### Lifetime configuration (per app)
- **Absolute Expiration** — hard cap regardless of activity.
- **Inactivity Expiration** — expires after a period of non-use.
- Both can be enabled/disabled independently.

## Refresh Token Rotation

Strongly recommended for public clients (SPA, Native).

### Mechanism
Every refresh exchange:
1. Auth0 issues a **new** refresh token along with the new access token.
2. The **previous refresh token is invalidated** (after the Reuse Interval / Rotation Overlap window).
3. Auth0 tracks the **token family** (all RTs descended from the original).

### Automatic Reuse Detection → Family Invalidation
If a previously-used (and rotated-away) refresh token is presented:
1. Auth0 detects the reuse.
2. **The entire token family is invalidated** — every refresh token derived from the original is killed.
3. Legitimate user and attacker both lose access; legitimate user must re-authenticate.
4. Auth0 logs the reuse with event code **`ferrt`**.

### Configuration
- **Allow Refresh Token Rotation** toggle (per application).
- **Rotation Overlap Period** (in seconds) — leeway window where the just-rotated RT is still accepted, in case the new RT didn't reach the client (network glitch).

### Why rotation matters for SPAs
- SPA browser storage isn't perfectly secure.
- Rotation + reuse detection means a stolen RT becomes worthless within one refresh cycle.
- Unlike silent authentication, rotation isn't blocked by ITP (Intelligent Tracking Prevention) since it doesn't depend on the Auth0 session cookie.

### Supported flows
Authorization Code, Authorization Code + PKCE, Device Flow, Resource Owner Password.

## Logout Tokens
Used in Back-Channel Logout. See [[10_sessions_logout]].

## Token Validation Checklist
See [[03_jwt_and_signing]] for the full validation steps. Minimum:
1. Verify signature with the right key (JWKS for RS256)
2. Verify `iss`
3. Verify `aud`
4. Verify `exp` (not expired)
5. Verify `nonce` for ID tokens (matches your sent nonce)
6. Verify `permissions`/`scope` before authorizing operations
