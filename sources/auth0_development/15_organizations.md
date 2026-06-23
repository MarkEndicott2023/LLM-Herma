# Auth0 Organizations (B2B / Multi-Tenancy)

**Auth0 docs:** https://auth0.com/docs/manage-users/organizations

## Purpose: B2B Multi-Tenancy

Organizations let you represent **your business customers** within a single Auth0 tenant. Each org has its own members, connections, branding, and (optionally) MFA policies — perfect for SaaS apps serving multiple companies.

> Auth0 Organizations enables B2B customers to "manage their partners and customers, and customize the ways that end-users access their applications and APIs."

## Organization vs Tenant

- **Tenant** — your top-level Auth0 environment (one per env: dev, staging, prod).
- **Organization** — a logical grouping of users *within* a tenant, representing one of your business customers.

Multiple orgs share the same tenant's apps, APIs, and global config; each org has its own scoped membership and settings.

---

## Members

Two ways to add users to an org:

### 1. Invitation Flow
- Send invitation: `POST /api/v2/organizations/{org_id}/invitations`
- Auth0 emails the invitee a signed ticket.
- They click the link → land on Auth0 login → upon successful auth, they're added as a member.
- Supports redirect URLs and role assignment in the invitation.

### 2. Direct Assignment via Management API
- `POST /api/v2/organizations/{org_id}/members`
- Body: `{ "members": ["auth0|user1", "auth0|user2", ...] }`
- **Limit: max 10 members per single API call.** Batch larger lists.

### Member Roles
Roles in Auth0 can be scoped **per-org**: same user, different roles in different orgs.
```
POST /api/v2/organizations/{org_id}/members/{user_id}/roles
```

---

## Connections per Organization

Each org has a list of **enabled connections** (database, social, enterprise). When a user authenticates via an org:
- Only that org's enabled connections appear as login options.
- Enterprise connections can be **auto-membership** (any successful enterprise SSO login auto-joins the org) and **assign-membership-on-login** (user is added on first SSO login).

### Connection sharing
A connection can be enabled in multiple orgs. Common pattern: shared social connections, dedicated enterprise SAML connection per customer.

---

## Authentication with Organizations

### Forcing an org context at `/authorize`
```
/authorize?...&organization=org_xxxx&invitation=inv_yyyy
```
- `organization` — the org ID; restricts login to that org's connections + members.
- `invitation` — accepts an invitation ticket (used in the invitation flow).

### Three login modes (Dashboard → Applications → [App] → Organizations tab)
| Mode | Behavior |
|---|---|
| **No organization** | Standard non-org login |
| **Allow membership** | Users can log in to either personal or an org context |
| **Require membership** | Users must select an org; org context is mandatory |

### Token claims for org logins
Every token (ID, access) for an org-context session includes:
```json
{
  "org_id": "org_xxxx",
  "org_name": "acme"
}
```
Your app uses these to scope data/permissions to the org.

---

## Branding per Organization

Each org can override (Dashboard → Organizations → [Org] → Branding):
- Logo URL
- Primary color, Page background color
- Custom prompt text

The Universal Login page renders the org's branding when the org context is present.

> **Limitation:** Orgs do **not** support **per-org custom domains** — all orgs share the tenant's domain.

---

## Critical Limitations (exam-tested)

| Limitation | Detail |
|---|---|
| **New Universal Login only** | Classic Login not supported |
| **No per-org custom domain** | All orgs share `tenant.auth0.com` (or the tenant's single custom domain) |
| **No Resource Owner Password Grant (ROPG)** | Use redirect flows |
| **No Device Authorization Flow** | |
| **No WS-Federation** | |
| **Max 10 members per bulk-add API call** | Batch larger lists |
| **Invitation ticket validity** | Time-limited (days, not weeks) |

---

## Management API for Organizations

Top-level resources:
```
GET/POST   /api/v2/organizations
GET/PATCH/DELETE  /api/v2/organizations/{org_id}
GET/POST/DELETE  /api/v2/organizations/{org_id}/members
GET/POST/DELETE  /api/v2/organizations/{org_id}/members/{user_id}/roles
GET/POST/DELETE  /api/v2/organizations/{org_id}/enabled_connections
GET/POST/DELETE  /api/v2/organizations/{org_id}/invitations
```

See [[20_logs_and_management_api]] for pagination, rate limits, and full Management API patterns. See [[14_rbac]] for per-org role assignment, and [[08_connections]] for enterprise connection setup.
