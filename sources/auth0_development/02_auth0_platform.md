# Auth0 Platform: Tenants, Applications, APIs

**Auth0 docs:** https://auth0.com/docs/get-started/tenant-settings · https://auth0.com/docs/get-started/applications · https://auth0.com/docs/get-started/apis

## Tenant

A tenant is an isolated Auth0 environment with its own URL (`YOUR_DOMAIN.auth0.com` or `YOUR_DOMAIN.REGION.auth0.com`). Each tenant has its own users, applications, APIs, connections, branding, signing keys, and rate limits.

### Tenant Settings — General Tab
- **Friendly Name** — displayed on Universal Login
- **Logo URL** — minimum 200×200 px recommended
- **Support Email**, **Support URL**
- **Environment Tag** — Production / Staging / Development (affects rate limits)
- **Default Audience** — API identifier defaulted into authz flows
- **Default Directory** — connection name used for Resource Owner Password Flow and Universal Login
- **Error Pages** — custom or generic
- **Languages** — default and supported

### Tenant Settings — Advanced Tab
- **Tenant Login URI** — for OIDC-initiated login
- **Allowed Logout URLs** — global allowlist for SSO scenarios
- **Allowed ACR Values**
- **RP-Initiated Logout endpoint controls**
- **Login Session Management (SSO):**
  - Inactivity timeout (default plan cap: 4,320 min; Enterprise: 144,000 min)
  - Require log in after (default plan cap: 43,200 min; Enterprise: 525,600 min)
- **Device Flow User Code Format**
- Advanced flags: Change Password Flow v2, Dynamic Client Registration (disabled by default), Resource Parameter Compatibility, Enable Application Connections (recommended disabled), Refresh Token Revocation Deletes Grant, Allow Organization Names in Authentication API, Allow Pushed Authorization Requests

### Other Tabs
- **Custom Domains** — branded login domain
- **Signing Keys** — manage signing certificate rotation
- **Tenant Members** — dashboard user management with MFA

## Applications

Auth0 categorizes applications by where they run and whether they can hold a secret.

### Four Application Types

| Type | Example | Confidential/Public |
|---|---|---|
| **Regular Web Application (RWA)** | Express, ASP.NET, Rails server-rendered apps | Confidential |
| **Single Page Application (SPA)** | React, Angular, Vue running in browser | Public |
| **Native Application** | iOS, Android, Electron, desktop apps | Public |
| **Machine-to-Machine (M2M)** | CLI, daemon, IoT, backend service | Confidential |

### Confidential vs Public Clients

| | Confidential | Public |
|---|---|---|
| Can securely store a client secret? | **Yes** | **No** |
| Types | RWA, M2M | SPA, Native |
| Auth methods | Client secret, Private Key JWT, mTLS | None (PKCE provides equivalent security) |

> **Critical security rule:** "Never include [client secrets] in mobile or browser-based apps." Decompiling a native app reveals embedded secrets; SPAs ship source to the browser.

### Application Ownership
- **First-party** — controlled by the org that owns the Auth0 tenant
- **Third-party** — external partners; subject to consent screen and enhanced security

### Core Credentials
- **Client ID** — unique public identifier
- **Client Secret** — secret known to app and Auth0; rotate if compromised, then update authorized apps

### Application Credential Methods (token endpoint authentication)
1. Client Secret (Post / Basic)
2. Private Key JWT
3. mTLS

### Grant Types
Each app type ships with a default set of allowed grant types. The `grant_types` array on the app controls which OAuth flows are permitted.

### JWT Signing Algorithm (per application)
- **HS256** (symmetric, uses client secret)
- **RS256** (asymmetric, public key via JWKS) — recommended

See [[03_jwt_and_signing]] for algorithm details and [[04_uri_configuration]] for callback/logout/origins.

---

## APIs (Resource Servers)

An API in Auth0 represents an external resource that accepts protected requests. In OAuth terms, this is the **Resource Server**.

### Key API Settings
- **Identifier (audience)** — typically the API's URL, e.g., `https://api.example.com`. Used as the `audience` parameter in `/authorize` and `/oauth/token` requests, and appears as the `aud` claim in access tokens. *Immutable once set.*
- **Signing Algorithm** — HS256 or RS256 (RS256 strongly preferred for APIs)
- **Token Expiration** — default 86,400 seconds (24 hours) for custom APIs
- **Token Expiration for Browser Flows** — separate, typically shorter
- **Allow Offline Access** — enables refresh tokens for this API (requires the `offline_access` scope)
- **Allow Skipping User Consent** — only works for first-party apps
- **Enable RBAC** — turn on per-API role-based access control
- **Add Permissions in the Access Token** — when enabled, adds the `permissions` claim (array of strings) to access tokens

### Permissions / Scopes
- Permissions are defined per API as scope strings, e.g., `read:patients`, `create:reports`.
- Apps request them via the `scope` parameter at `/authorize`.
- With RBAC enabled, roles bundle permissions and are assigned to users.

### M2M Authorization
Machine-to-Machine apps must be explicitly authorized against an API (Dashboard → APIs → [API] → Machine to Machine Applications) and granted specific scopes.

### Built-in: Auth0 Management API
Every tenant has a built-in `Auth0 Management API` (audience `https://YOUR_DOMAIN/api/v2/`). See [[20_logs_and_management_api]].
