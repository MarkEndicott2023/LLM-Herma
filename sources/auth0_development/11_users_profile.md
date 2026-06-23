# User Profiles, Metadata, and Account Linking

**Auth0 docs:**
- https://auth0.com/docs/manage-users/user-accounts/user-profiles
- https://auth0.com/docs/manage-users/user-accounts/metadata
- https://auth0.com/docs/manage-users/user-accounts/user-account-linking

## The Normalized User Profile

Different connections (Google, SAML IdP, custom DB, etc.) return user attributes under different names. Auth0 normalizes them into a single consistent schema so apps don't have to special-case each IdP.

### Core Profile Attributes
- `user_id` — unique identifier in Auth0, format: `connection|external_id` (e.g., `auth0|abc123`, `google-oauth2|987...`)
- `name`, `nickname`, `given_name`, `family_name`
- `email`, `email_verified`
- `phone_number`, `phone_number_verified`
- `picture`
- `created_at`, `updated_at`, `last_login`, `last_ip`, `logins_count`
- `identities` — array of identity objects (one per linked connection)
- `user_metadata`, `app_metadata`
- `multifactor` — array of enrolled MFA factors
- `blocked` — boolean

### The `identities` Array
Each identity in the array contains:
- `connection` — name of the connection
- `user_id` — ID at the upstream provider
- `provider` — e.g., `auth0`, `google-oauth2`, `samlp`
- `isSocial` — boolean
- `profileData` — original profile from the IdP (only for linked secondary identities)

### Where attributes come from
- **Social/Enterprise:** sourced from the IdP via attribute mapping (or `profileMapper.js` for AD/LDAP, or Mappings tab for SAML).
- **Database:** from signup form + custom database scripts.
- **Auth0 caches** the profile from connections before passing to apps. Cache refreshes on each authentication.

### Critical limitation on multi-identity profiles
> "Auth0 does not merge user profile attributes from multiple providers. Auth0 sources core user profile attributes from the first provider used."

After account linking, only one identity's core attributes win — the rest are accessible only through `identities[].profileData`.

---

## User Metadata vs App Metadata

Two separate metadata bags, with very different rules.

| | `user_metadata` | `app_metadata` |
|---|---|---|
| **Purpose** | User-managed preferences | Authorization-critical data |
| **Who can edit** | The user themselves (via app UI) | Admins / backend only |
| **Example contents** | Language preference, hobby, color theme | Plan tier, internal user IDs, roles list, permissions |
| **Use in authorization decisions?** | **No** — untrusted | **Yes** — trusted |
| **Editable via** | Logged-in user's session, Management API, Actions | Management API, Actions (admins) |

### Size limits
- Each metadata field's total payload should stay reasonable.
- Custom DB signups via `/dbconnections/signup`: max 10 string fields, 500 chars total.

### Client Metadata
Distinct from user metadata. Lives on the **client (application)** object:
- `client_metadata` on Client objects
- `context.clientMetadata` in Rules
- `event.client.metadata` in Actions
Example: app's home page URL, custom settings.

### Reading/Writing via Management API
| Action | Endpoint | Required Scope |
|---|---|---|
| View | `GET /api/v2/users/{id}` | `read:users` |
| Update | `PATCH /api/v2/users/{id}` | `update:users`, `update:users_app_metadata` |

### Reading/Writing via Actions
```js
// Read
event.user.user_metadata.theme
event.user.app_metadata.plan

// Write (Post-Login)
api.user.setUserMetadata("theme", "dark");
api.user.setAppMetadata("plan", "enterprise");
```
See [[16_actions]].

---

## Account Linking

Merge multiple identities (different connections) into one user profile.

### Primary vs Secondary
- **Primary account** — keeps its `user_id`. Its core profile attributes (name, email, picture, etc.) remain.
- **Secondary account** — gets absorbed; its identity moves into the primary's `identities` array under `profileData`. Disappears from the users list.
- **`user_metadata` and `app_metadata` of secondary are discarded** unless you merge them manually via Management API.
- Deleting the primary deletes all linked secondaries.

### How to Link

#### Manual / User-Initiated (via Management API)
```
POST /api/v2/users/{primary_user_id}/identities
{
  "provider": "google-oauth2",
  "user_id": "secondary_user_id"
}
```
Must use a **Management API access token** with appropriate scopes.

Alternative: pass an `link_with` ID token for the secondary account.

> **Deprecation:** ID tokens for linking/unlinking are deprecated; use access tokens.

#### Suggested Linking (UI Prompt)
App detects two accounts with the same verified email and prompts the user to link. The Account Link Extension provides a turn-key implementation.

#### Automatic Linking
Not enabled by default. Can be implemented via a Post-Login Action that detects same-email matches and calls the linking endpoint.

### Security Requirement
> "Your tenant should request authentication for **both** accounts before linking occurs."

Without this, an attacker could link their account to a victim's. Always verify ownership of both identities (e.g., require fresh authentication on the secondary).

### Unlinking
```
DELETE /api/v2/users/{primary_user_id}/identities/{provider}/{secondary_user_id}
```
Unlinking restores the secondary as its own separate user.

## Restricted Attributes
Some profile attributes are immutable or restricted (e.g., `user_id` always immutable; `email` immutable on certain connections). Auth0 docs list restrictions per connection type.
