# Role-Based Access Control (RBAC)

**Auth0 docs:** https://auth0.com/docs/manage-users/access-control/rbac

## Concept

RBAC = "assign permissions to users based on their role." Users → Roles → Permissions. Roles bundle permissions so you assign roles to users rather than individual permissions.

### Additive
A user with two roles gets the **union** of both roles' permissions.

### Example
- Permission `read:newsletters` (on API `https://news.example.com`)
- Permission `publish:events` (on API `https://events.example.com`)
- Role `Marketing Publisher` = both permissions
- Assign `Marketing Publisher` to Jane → Jane can do both

---

## Two RBAC Implementations

| | **Authorization Core** | **Authorization Extension** (legacy) |
|---|---|---|
| Recommended | **Yes** | No (legacy) |
| Setup | Built into APIs | Separate extension install |
| Performance | Better, scalable | Older |

Use Authorization Core for new work.

---

## Per-API Configuration

RBAC is enabled **on each API** independently (Dashboard → APIs → [API] → Settings).

### Two key toggles
1. **Enable RBAC** — turn on RBAC for this API.
2. **Add Permissions in the Access Token** — when enabled, every access token for this API includes a `permissions` claim listing the user's effective permissions.

| Both on | Access token has `permissions` array claim |
|---|---|
| **Enable RBAC** on, **Add Permissions** off | Permissions evaluated but not in token — app must check via `/userinfo` or Management API |
| **Enable RBAC** off | No RBAC — only requested scopes appear in `scope` claim |

### Defining Permissions
Dashboard → APIs → [API] → Permissions tab. Add scope strings + descriptions:
- `read:patients`
- `write:patients`
- `delete:patients`

These become the available permissions for roles and the available scopes for `scope` parameter requests.

---

## Roles

Dashboard → User Management → Roles, or via Management API.

### Create a role
```
POST /api/v2/roles
{ "name": "Marketing Publisher", "description": "..." }
```

### Add permissions to a role
```
POST /api/v2/roles/{role_id}/permissions
{
  "permissions": [
    { "resource_server_identifier": "https://news.example.com", "permission_name": "read:newsletters" }
  ]
}
```

### Assign roles to a user
```
POST /api/v2/users/{user_id}/roles
{ "roles": ["rol_xxx", "rol_yyy"] }
```

### Direct permission assignment (bypass roles)
```
POST /api/v2/users/{user_id}/permissions
```
Use sparingly — defeats the purpose of RBAC.

---

## Token Format with RBAC

### `scope` claim
Always present. Contains scopes the app **requested** (subset of what the user has if RBAC is restricting).

### `permissions` claim (when "Add Permissions in the Access Token" is on)
Array of strings — the user's **effective permissions** on this API:
```json
{
  "scope": "openid profile read:patients",
  "permissions": ["read:patients", "write:reports"]
}
```

### Important nuance
- **Scopes** = what the **app** asked for (passed in `scope` param at `/authorize`).
- **Permissions** = what the **user** actually has (via roles).
- These can diverge. When RBAC is on, Auth0 restricts the returned scopes to the intersection of (requested scopes) ∩ (user's permissions).

---

## Enforcing in APIs

Your API code must:
1. Validate the access token ([[03_jwt_and_signing]]).
2. Check the `permissions` claim (or `scope`) for the operation being requested.
3. Return 403 if missing.

Auth0 SDKs and middleware (e.g., `express-oauth2-jwt-bearer`) provide helpers to require specific permissions.

---

## Extending Beyond Plain RBAC
Use **Actions** ([[16_actions]]) for context-aware policies:
- Time-of-day restrictions
- Geo-fencing
- Department-based access
- Tier-based feature gating using `app_metadata`
- Adding custom permission logic to access tokens

---

## RBAC in Organizations
With Organizations ([[15_organizations]]), roles can be scoped **per organization**: the same user can be `Admin` in Org A and `Viewer` in Org B. Use the organization member roles endpoints:
```
POST /api/v2/organizations/{org_id}/members/{user_id}/roles
```

See [[20_logs_and_management_api]] for the full Management API surface.
