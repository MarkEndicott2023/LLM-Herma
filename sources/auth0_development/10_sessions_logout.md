# Sessions and Logout

**Auth0 docs:** https://auth0.com/docs/manage-users/sessions · https://auth0.com/docs/authenticate/login/logout

## The Three Session Layers

A user logging in via Auth0 typically establishes **three independent sessions**:

| Layer | Where | What it tracks |
|---|---|---|
| **1. Application Session** | Your app (e.g., `app.example.com`) | "User is logged in to MY app" |
| **2. Auth0 (Authorization Server) Session** | Auth0 domain (e.g., `tenant.auth0.com`) | "User has authenticated with Auth0" — enables SSO across all apps in the tenant |
| **3. Identity Provider Session** | Upstream IdP (e.g., Google, Azure AD) | "User is logged in to their Google/Azure account" |

**Implication:** Logging out of the app does NOT log out of Auth0 (still SSO'd to other apps). Logging out of Auth0 does NOT log out of the upstream IdP. Each layer must be explicitly addressed.

## Session Triggers

Sessions reset or end when:
- User explicitly logs out
- Session lifetime is reached
- Password is updated
- Email, phone, or username changes
- New standard login occurs (session resets)

## Session Management Approaches

| App type | Approach |
|---|---|
| **Regular Web App** | Local session via `Set-Cookie` |
| **SPA** | Silent authentication: hidden iframe to `/authorize?prompt=none`, returns tokens via `web_message` postMessage (uses Auth0 session cookie) |
| **Native** | Refresh token + secure storage |

### Auth0 Session Lifetime Settings (Tenant → Advanced)
- **Inactivity Timeout** — minutes of inactivity before Auth0 session ends. Capped at 4,320 min (standard) / 144,000 min (Enterprise).
- **Require Log In After** — absolute timeout. Capped at 43,200 min (standard) / 525,600 min (Enterprise).

## Logout

### Three logout scopes — must be addressed independently

#### 1. Application Logout
- Clear your app's session cookie.
- Up to you to implement.

#### 2. Auth0 (SSO) Logout — RP-Initiated Logout
Two endpoints:

**Legacy** (`/v2/logout`):
```
GET https://YOUR_DOMAIN/v2/logout?
    client_id=YOUR_CLIENT_ID
    &returnTo=https://yourapp.com/after-logout
    &federated   ← optional: also logs out of upstream IdP
```

**OIDC RP-Initiated Logout** (`/oidc/logout`) — recommended, OIDC-spec compliant:
```
GET https://YOUR_DOMAIN/oidc/logout?
    id_token_hint=USER_ID_TOKEN
    &post_logout_redirect_uri=https://yourapp.com/after-logout
    &client_id=YOUR_CLIENT_ID
    &logout_hint=SESSION_HINT   ← optional
```

Parameters:
- `id_token_hint` — the user's ID token; identifies which session to log out
- `post_logout_redirect_uri` — must be in **Allowed Logout URLs**
- `client_id` — required if no id_token_hint
- `logout_hint` — optional session ID hint

#### 3. Identity Provider Logout — Federated Logout
Add `federated` to the legacy endpoint, or include `federated=true` to also terminate the upstream IdP session. Only some IdPs support this.

### Allowed Logout URLs
- Per-app: Application Settings → Allowed Logout URLs (limit 100, [[04_uri_configuration]])
- Tenant-level: Tenant Settings → Advanced → Allowed Logout URLs (for SSO scenarios spanning apps)

## Back-Channel Logout

Auth0 → app server-to-server logout notification. The OIDC Back-Channel Logout spec.

- Auth0 POSTs a signed **logout_token** (JWT) to your registered Back-Channel Logout URI.
- The logout_token contains:
  - `iss`, `aud`, `iat`, `jti`
  - `sub` (user ID) and/or `sid` (session ID)
  - `events` claim: `{"http://schemas.openid.net/event/backchannel-logout": {}}`
- Your app verifies the token and terminates the user's local session.
- No user-facing redirect — purely server-to-server.

**When to use:** When the user logs out from one app, all other apps in the same SSO session can be notified to terminate their local sessions even without the user visiting them.

## Front-Channel Logout

Browser-based propagation. Auth0 renders hidden iframes/redirects to each participating app's front-channel logout URI to clear their cookies. Less reliable than back-channel; subject to third-party cookie blocking.

## Universal Logout

The newest standard. Revokes **refresh tokens** and propagates logout across all sessions for a user. Used in enterprise scenarios for centralized session termination.

## Configuration Locations

- App: Application Settings → Application URIs (Logout URLs, Back-Channel Logout URI, Front-Channel Logout URI)
- Tenant: Tenant Settings → Advanced (RP-Initiated Logout endpoint enablement, global Allowed Logout URLs)

## Logout Event Logs
- `slo` — successful logout
- `ferrt` — refresh token reuse (also fires on Universal Logout) — see [[20_logs_and_management_api]]

See [[09_tokens]] for the relationship between sessions and refresh tokens.
