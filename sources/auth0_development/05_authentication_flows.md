# Authentication Flows (Auth Code, PKCE, Client Credentials, Legacy)

**Auth0 docs:**
- https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow
- https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce
- https://auth0.com/docs/get-started/authentication-and-authorization-flow/client-credentials-flow
- https://auth0.com/docs/get-started/authentication-and-authorization-flow/implicit-flow-with-form-post
- https://auth0.com/docs/get-started/authentication-and-authorization-flow/resource-owner-password-flow

## Flow Selection Matrix

| Flow | App Type | Client Type | Tokens Returned |
|---|---|---|---|
| **Authorization Code** | Regular Web App | Confidential | ID + Access + Refresh |
| **Authorization Code with PKCE** | SPA, Native | Public | ID + Access + Refresh |
| **Client Credentials** | Machine-to-Machine | Confidential | Access only |
| **Implicit with Form Post** | RWA login-only (legacy) | Confidential | ID only |
| **Resource Owner Password (ROPG)** | Highly-trusted first-party (legacy) | Either | Access (+ ID if openid scope) |
| **Device Authorization** | Native (limited input devices) | Public | Access + Refresh |

**Default modern picks:** Auth Code Flow (server apps), Auth Code Flow + PKCE (SPA/Native), Client Credentials (M2M).

---

## 1. Authorization Code Flow (Regular Web App)

Confidential clients only. The authorization code is exchanged for tokens server-side using the client secret.

### Steps
1. User clicks login. App redirects browser to `/authorize`:
   ```
   GET /authorize?
       response_type=code
       &client_id=YOUR_CLIENT_ID
       &redirect_uri=https://yourapp.com/callback
       &scope=openid profile email
       &audience=https://api.example.com   ← optional, for access token
       &state=RANDOM_STATE
   ```
2. User authenticates (and consents if 3rd party).
3. Auth0 redirects to `redirect_uri?code=AUTHZ_CODE&state=STATE` (verify state matches).
4. App **server** POSTs to `/oauth/token`:
   ```
   POST /oauth/token
   grant_type=authorization_code
   &client_id=YOUR_CLIENT_ID
   &client_secret=YOUR_CLIENT_SECRET
   &code=AUTHZ_CODE
   &redirect_uri=https://yourapp.com/callback
   ```
5. Auth0 verifies parameters, returns `{access_token, id_token, refresh_token (if offline_access scope), expires_in, token_type}`.
6. App uses access token to call APIs.

### Security note
> "Browser-based applications making POST requests to `/oauth/token` will not receive refresh tokens even with rotation enabled" — prevents token proliferation in less-secure environments.

---

## 2. Authorization Code Flow with PKCE (SPA, Native)

Public clients (cannot hold a secret). PKCE = Proof Key for Code Exchange (RFC 7636).

### Why PKCE
Without a client secret, an attacker who intercepts the authorization code could exchange it for tokens. PKCE binds the code to a secret known only to the original requester.

### code_verifier and code_challenge
- **code_verifier** — cryptographically-random string (43–128 chars), generated client-side per request
- **code_challenge** — derived from verifier:
  - `S256` (recommended): `BASE64URL(SHA256(verifier))`
  - `plain` (discouraged): equals the verifier
- **code_challenge_method** — `S256` or `plain`

### Steps
1. SDK generates `code_verifier`, derives `code_challenge`.
2. Browser → `/authorize` with `code_challenge` + `code_challenge_method=S256` (no client_secret).
3. User authenticates.
4. Auth0 stores the challenge, returns `code`.
5. SDK POSTs to `/oauth/token` with `code` + `code_verifier` (no client_secret).
6. Auth0 verifies `SHA256(code_verifier) == challenge`. Issues tokens.

> "A malicious attacker can only intercept the Authorization Code; they cannot exchange it for a token without the Code Verifier."

### Custom URI schemes
Auth0 **strongly discourages** custom URI schemes (e.g., `myapp://`) for native apps because they can be hijacked. Prefer App Links (Android) / Universal Links (iOS).

---

## 3. Client Credentials Flow (Machine-to-Machine)

No user is involved. The app authenticates *as itself*.

### Request
```
POST /oauth/token
grant_type=client_credentials
&client_id=YOUR_CLIENT_ID
&client_secret=YOUR_CLIENT_SECRET
&audience=https://api.example.com
```

### Response
- **Access token only.** No ID token (no user). No refresh token (just request a new access token).
- Scopes available are those granted to the M2M app at the API (Dashboard → APIs → Machine to Machine Applications).

### Use cases
Backend services, CLIs, daemons, IoT devices, scheduled jobs, server-to-server calls.

---

## 4. Implicit Flow with Form Post (Legacy — Login-Only)

For traditional web apps that need **only an ID token** (login only, no API access).

### Parameters
- `response_type=id_token` (login-only) or `response_type=token id_token`
- `response_mode=form_post` (POST to redirect_uri instead of URL fragment — avoids browser history leakage)

### When to use vs when NOT to
- **Use:** RWA that needs ID token only, no API access.
- **Don't use:** SPAs requesting access tokens. The OAuth Working Group deprecated Implicit Flow for SPAs in favor of Auth Code + PKCE.

> "Although OAuth now discourages the use of the implicit grant for obtaining access tokens in SPAs, the scenario addressed by Implicit Flow with Form Post is completely different and is unaffected by the security issues" that motivated PKCE.

---

## 5. Resource Owner Password Flow (ROPG) — Legacy

**Use only for highly-trusted first-party apps where redirect-based flows are impossible.** Never use for third-party.

### Request
```
POST /oauth/token
grant_type=password
&username=USER_EMAIL_OR_USERNAME
&password=USER_PASSWORD
&audience=https://api.example.com
&scope=openid profile
&client_id=YOUR_CLIENT_ID
&client_secret=YOUR_CLIENT_SECRET  ← if confidential
```

### Realm extension
Use `realm=Username-Password-Authentication` (or other connection name) to target a specific connection. Useful when you have multiple user directories.

### Critical limitations
- App handles the user's password directly — huge trust requirement.
- **Incompatible with:**
  - Auth0 Organizations
  - Redirect Rules / redirect Actions (`api.redirect.sendUserTo`)
  - Some attack protection signals
  - Adaptive MFA (limited)
- MFA can work via dedicated MFA endpoints (`/mfa/challenge`, `/mfa/verify`).

---

## Common Parameters Across Flows

| Parameter | Purpose |
|---|---|
| `client_id` | Identifies the application |
| `client_secret` | Authenticates confidential apps |
| `redirect_uri` | Where Auth0 sends the user after authz |
| `response_type` | `code`, `token`, `id_token`, or combinations |
| `scope` | Permissions requested (must include `openid` for OIDC) |
| `audience` | API identifier — triggers access token issuance for that API |
| `state` | CSRF protection ([[19_attack_protection]]) |
| `nonce` | Replay protection for ID tokens ([[19_attack_protection]]) |
| `prompt` | `none`, `login`, `consent`, `select_account` |
| `connection` | Force a specific connection |
| `organization` | Target an org context ([[15_organizations]]) |
| `code_challenge`, `code_challenge_method` | PKCE |
| `code_verifier` | PKCE (token request) |
| `grant_type` | `authorization_code`, `client_credentials`, `password`, `refresh_token`, etc. |
