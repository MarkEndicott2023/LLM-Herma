# Identity and Access Management Fundamentals

**Auth0 docs:** https://auth0.com/docs/get-started/identity-fundamentals · https://auth0.com/docs/authenticate/protocols/openid-connect-protocol

## Authentication vs Authorization

- **Authentication (AuthN):** Verifying *who* a user is. Asks "who are you?"
- **Authorization (AuthZ):** Verifying *what* a user can do. Asks "what are you allowed to do?"
- Authentication always precedes authorization. They are distinct concerns and Auth0 implements them with different mechanisms (ID tokens for AuthN, Access tokens for AuthZ).

## Identity Providers (IdPs)

A system that creates, maintains, and manages identity information. Auth0 itself can be an IdP, but it also brokers identities from external IdPs:

- **Social IdPs** — Google, Facebook, Apple, GitHub, Microsoft, LinkedIn, Twitter, etc.
- **Enterprise IdPs** — Azure AD / Entra ID, ADFS, Google Workspace, Okta Workforce, PingFederate, AD/LDAP, OIDC, SAML, WS-Fed
- **Database** — Auth0-hosted or custom (your own database)
- **Passwordless** — Email magic link, email/SMS OTP

## Single Sign-On (SSO)

A user logs in once with an IdP and gets access to multiple applications without re-authenticating. Auth0 enables this via:
- The Auth0 session cookie (tenant-level SSO)
- Federated SSO with upstream IdPs (SAML, OIDC enterprise connections)
- Universal Login (centralized login on Auth0 domain — required for SSO to work cleanly)

## Federation

Trust relationship between two parties allowing identity assertions issued by one to be accepted by the other. SAML and OIDC are the standard federation protocols.

## Identity Standards

| Standard | Purpose |
|---|---|
| **OAuth 2.0** | Authorization framework. Defines flows for issuing access tokens. NOT authentication. |
| **OpenID Connect (OIDC)** | Identity layer on top of OAuth 2.0. Adds ID tokens, userinfo endpoint, standard authentication claims. |
| **JWT** | JSON Web Token. Compact, signed token format used for both ID tokens and access tokens. |
| **SAML 2.0** | XML-based assertion protocol. Mostly used for enterprise SSO. |
| **WS-Federation** | Microsoft-centric federation protocol. Legacy. |

## OAuth 2.0 vs OIDC — the core distinction

> "OAuth 2.0 addresses resource access and sharing, while OIDC focuses on user authentication and single sign-on capabilities." — Auth0 docs

| | OAuth 2.0 | OIDC |
|---|---|---|
| **Purpose** | Authorization (delegated API access) | Authentication (login) |
| **Token issued** | Access token | ID token (always JWT) + Access token |
| **User info** | Not standardized | Standardized claims + `/userinfo` endpoint |
| **Audience** | API / resource server | The application itself |

**Exam shortcut:** OAuth = "what can this app do on my behalf?" OIDC = "who is this user?"

## Standard OIDC Scopes and Claims

| Scope | Claims added to ID token |
|---|---|
| `openid` (required for OIDC) | `sub`, `iss`, `aud`, `exp`, `iat`, `auth_time`, `nonce` |
| `profile` | `name`, `nickname`, `picture`, `given_name`, `family_name`, `gender`, `birthdate`, `locale`, `updated_at` |
| `email` | `email`, `email_verified` |
| `address` | `address` |
| `phone` | `phone_number`, `phone_number_verified` |

Combined example: `scope=openid profile email` returns all three sets of claims.

## OIDC Discovery

Auth0 publishes a discovery document at `https://YOUR_DOMAIN/.well-known/openid-configuration` containing all endpoints, supported scopes/claims, and signing keys location. Clients can auto-configure from this.
