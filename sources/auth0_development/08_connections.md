# Connections (Database, Social, Enterprise, Custom Database)

**Auth0 docs:**
- https://auth0.com/docs/authenticate/database-connections
- https://auth0.com/docs/authenticate/database-connections/custom-db
- https://auth0.com/docs/authenticate/identity-providers/social-identity-providers
- https://auth0.com/docs/authenticate/identity-providers/enterprise-identity-providers

A **connection** in Auth0 is a source of users. Each application can have multiple connections enabled.

## Connection Categories

| Category | Examples | When to use |
|---|---|---|
| **Database** | Auth0-hosted DB; Custom DB (your store) | Username/password auth |
| **Social** | Google, Facebook, Apple, GitHub, etc. | Consumer login |
| **Enterprise** | SAML, OIDC, Azure AD, ADFS, Google Workspace, Okta, LDAP, WS-Fed | B2B / employee login |
| **Passwordless** | Email, SMS | OTP / magic link |

---

## Database Connections

### Auth0-Hosted Database
- Users stored in Auth0.
- Passwords hashed with **bcrypt** (never stored or logged in plaintext).
- Per-user and per-IP rate limiting on login.
- Optimal performance — all data in Auth0 infrastructure.
- Configurable **password policies** (None, Low, Fair, Good, Excellent — with character/length rules).
- Supports breached password detection.

### Custom Database Connections
Use your own user store. Auth0 calls your scripts during authentication.

#### Two modes
1. **Use Auth0 to authenticate** (lazy migration) — first login pulls from your DB, then user lives in Auth0.
2. **Use my own database** — Auth0 never stores the user; every login hits your DB.

#### Action Scripts (Node.js)
| Script | Required? | Purpose |
|---|---|---|
| Login | **Required** | Authenticate user against your DB |
| Get User | Optional (recommended) | Lookup by email — for password reset, migration |
| Create | Optional | Provision new users in your DB on signup |
| Verify | Optional | Mark email verified |
| Change Password | Optional | Update password in your DB |
| Delete | Optional | Remove user from your DB |
| Change Email | Optional | Update email in your DB |

#### Constraints
- **Combined script size limit: 100 KB.** Move heavy logic to external APIs.
- Runs in Auth0's Node.js sandbox with a limited NPM module allowlist.
- Use `callback(null, profile)` on success, `callback(new WrongUsernameOrPasswordError())` on bad creds, `callback(new Error(...))` on system errors.
- Provided templates: ASP.NET Membership, MongoDB, MySQL, PostgreSQL, SQL Server, Azure SQL, Basic Auth web services.

See [[13_user_migration]] for lazy migration details.

---

## Social Connections

### Setup
- **Dev keys** (default) — quick to enable, but Auth0-shared keys with rate limits and no profile customization. **Not for production.**
- **Production keys** — register your own OAuth app with the provider (Google Cloud Console, Facebook App, etc.), get client ID and secret, paste into Auth0.

### Supported Providers
Google, Facebook, Apple, Microsoft, GitHub, LinkedIn, Twitter (X), Amazon, Yahoo, PayPal, Spotify, and many more (see Auth0 Marketplace). Custom OAuth2 providers also supported via the **Generic OAuth2** connection.

### Scopes
Request additional permissions from the IdP via the **Permissions** setting on the connection (e.g., Google `https://www.googleapis.com/auth/calendar` to access calendar).

### Account Linking with Social
A user who first signs in via Google and later via email typically gets two profiles. Use [[11_users_profile]] account linking to merge.

---

## Enterprise Connections

For B2B / workforce login. Federation with the customer's IdP.

### Supported Types
| Type | Protocol |
|---|---|
| **SAML** | SAML 2.0 — XML assertions |
| **OpenID Connect (OIDC)** | OIDC discovery + standard flows |
| **Azure AD / Microsoft Entra ID (v2)** | OIDC under the hood |
| **Azure AD Native** | Legacy |
| **ADFS** | Active Directory Federation Services (WS-Fed/SAML) |
| **Google Workspace** | OIDC |
| **Okta Workforce** | OIDC + Okta-specific |
| **PingFederate** | SAML |
| **AD/LDAP** | Requires AD/LDAP Connector |
| **OpenLDAP** | Via AD Connector |
| **WS-Fed** | Legacy |
| **SharePoint Apps** | Niche |

### Pricing Note
B2B and Enterprise plans include unlimited Okta Enterprise Connections.

### Home Realm Discovery (HRD)
Enterprise connections can be associated with one or more **email domains**. When a user enters their email at login, Auth0 routes them to the matching connection automatically. See [[12_identifier_first_hrd]].

### JIT Provisioning
First-time enterprise SSO logins auto-create the user in Auth0. Profile is sourced from the SAML assertion / OIDC claims via attribute mapping.

### Attribute Mapping
- **SAML:** Connection's Mappings tab — align IdP attribute names with Auth0 normalized profile.
- **OIDC:** Claim Mapping — map provider claims onto Auth0 profile attributes.
- **AD/LDAP:** `profileMapper.js` runs at authentication time.

---

## Per-App Connection Enablement

Enabling a connection at the tenant level is separate from enabling it for a specific app. By default new apps may auto-connect to all connections — recommended to **disable Application Connections globally** (Tenant Settings → Advanced) and opt in per-app.

See [[15_organizations]] for org-scoped connection assignment, [[03_jwt_and_signing]] for tokens, and [[11_users_profile]] for how connection data populates the normalized user profile.
