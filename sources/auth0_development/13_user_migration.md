# User Migration

**Auth0 docs:** https://auth0.com/docs/manage-users/user-migration

Two strategies for moving users from a legacy identity store into Auth0.

## Strategy 1: Automatic (Lazy) Migration

Users migrate **gradually**, as they log in for the first time. No forced password reset.

### How it works
1. Configure a **Custom Database Connection** ([[08_connections]]) with at least the Login and Get User scripts pointing to your legacy DB.
2. Enable the **"Import Users to Auth0"** (lazy migration) toggle on the connection.
3. When a user attempts to log in:
   - Auth0 first checks its own DB for the user.
   - If **not found**, Auth0 calls your Login script against the legacy DB.
   - On successful auth, the user is **created in Auth0** (with their plaintext password being hashed by Auth0 and stored).
4. **Subsequent logins** go straight to Auth0 — no more calls to the legacy DB for that user.

### Pros
- Zero disruption to users — they don't notice the migration.
- No password resets needed.
- No bulk export/import of credentials.

### Cons
- Migration takes weeks/months depending on user login cadence.
- Users who never log in are never migrated.
- Legacy DB must stay online until everyone migrates.

### Plan requirement
Custom database connections (and therefore lazy migration) depend on your Auth0 plan.

---

## Strategy 2: Bulk User Import

One-shot import via the Management API or the Dashboard UI.

### Method A — Management API (`/jobs/users-imports`)
```
POST /api/v2/jobs/users-imports
Authorization: Bearer MGMT_TOKEN
Content-Type: multipart/form-data

connection_id=con_xxxx
users=@users.json
upsert=false
external_id=correlation_id
```

The `users.json` is a JSON **array** of user objects. Auth0 processes asynchronously and returns a job ID. Poll `GET /jobs/{id}` and `GET /jobs/{id}/errors`.

### Method B — Dashboard UI
Dashboard → User Management → Users → Import Users. Upload the same JSON format.

> **Deprecation:** The legacy User Import/Export Extension was deprecated in September 2025. Bulk import is now in the main Dashboard.

### Permissions
| Operation | Required Dashboard Role |
|---|---|
| Bulk Import | Editor - Users **or** Admin |
| Bulk Export | Viewer - Users, Editor - Users, **or** Admin |

### Bulk import JSON format
Per-user fields include:
```json
{
  "user_id": "external_id_123",       // optional
  "email": "user@example.com",
  "email_verified": true,
  "given_name": "Jane",
  "family_name": "Doe",
  "name": "Jane Doe",
  "nickname": "jane",
  "username": "jane.doe",
  "password_hash": "$2b$10$...",     // bcrypt hash — DO NOT use plaintext
  "blocked": false,
  "app_metadata": { "plan": "pro" },
  "user_metadata": { "theme": "dark" }
}
```

### Password Hash Compatibility
- Use the `password_hash` field with a **bcrypt hash** (the format Auth0 uses natively).
- Other formats supported via specific fields:
  - `custom_password_hash` for non-bcrypt (PBKDF2, MD5, etc.) — describes algorithm and parameters
- If your legacy DB uses a different hashing scheme that can't be expressed, you must either:
  1. Force password reset for all users, OR
  2. Use lazy migration so Auth0 captures plaintext at login and re-hashes with bcrypt.

---

## Gradual Migration Pattern (Hybrid)

Many real migrations combine both:
1. Run **lazy migration** for active users (the long tail).
2. After 3–6 months, run a **bulk import** for everyone still in the legacy DB but who hasn't logged in. Either force-reset their passwords, or import as blocked and invite to reset.
3. Decommission the legacy DB.

## Important Considerations
- Always test in a non-prod tenant first.
- Bulk import has rate limits — chunk large user sets.
- Keep external user IDs (`user_id` field) stable so app-side references don't break.
- Email verification status carries over — set `email_verified: true` for users you trust.

See [[08_connections]] for custom database setup and [[20_logs_and_management_api]] for the Jobs endpoint patterns.
