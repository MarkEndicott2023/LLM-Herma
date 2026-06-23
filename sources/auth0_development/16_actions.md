# Auth0 Actions

**Auth0 docs:** https://auth0.com/docs/customize/actions

## What Actions Are

> "Actions are secure, tenant-specific, versioned functions written in Node.js that execute at certain points within the Auth0 platform."

Auth0's modern extensibility model. Actions run as Node.js functions at specific **triggers** in the auth pipeline. They replace the legacy Rules and Hooks.

### Rules / Hooks deprecation (exam-critical)
- **Rules and Hooks reach end-of-life on November 18, 2026.**
- New work must use Actions.
- During the transition, if all three coexist on the same trigger, the execution order is: **Rules → Hooks → Actions**.

### Why Actions
- Versioned, tested in Dashboard before deploy.
- Async-first (promise-based).
- NPM package support.
- Real-time logging.
- Per-trigger ordering: arrange multiple Actions in a chain.

---

## Triggers (Flows)

| Trigger | Sync/Async | When it fires | Common uses |
|---|---|---|---|
| **post-login** | **Blocking** | After authentication, before tokens issued | Deny login, add custom claims, redirect, enable MFA |
| **pre-user-registration** | **Blocking** | Before user is created (DB/passwordless only) | Validate signup, deny user |
| **post-user-registration** | **Async** | After user is created (excludes social — that happens later) | Side effects: CRM sync, welcome flow, audit log |
| **post-change-password** | **Async** | After password change (excludes social) | Notify, audit |
| **send-phone-message** | Blocking | Phone delivery for MFA enrollment/challenge | Use custom SMS provider (Twilio, etc.) |
| **credentials-exchange** (M2M) | Blocking | Before access token returned for client_credentials | Add custom claims, deny based on app metadata |
| **password-reset-post-challenge** | Blocking | After password reset challenge, before reset | Additional validation |

**Blocking** = the flow waits for the Action. Errors block authentication.
**Async** = fire-and-forget. Errors logged but don't block the user.

---

## Action Anatomy

```js
exports.onExecutePostLogin = async (event, api) => {
  // your code here
};

// Optional second handler (Post-Login only)
exports.onContinuePostLogin = async (event, api) => {
  // runs when returning from api.redirect.sendUserTo
};
```

Each trigger has its own handler signature; here we focus on Post-Login since it's the most exam-relevant.

---

## The `event` Object

What the Action receives.

| Field | Contents |
|---|---|
| `event.user` | Full user profile: `user_id`, `email`, `email_verified`, `user_metadata`, `app_metadata`, `identities`, `phone_number`, `name`, `picture`, `created_at`, etc. |
| `event.client` | The application: `client_id`, `name`, `metadata` |
| `event.connection` | The connection used: `id`, `name`, `strategy` |
| `event.organization` | If org context: `id`, `name`, `display_name`, `metadata` |
| `event.request` | `ip`, `method`, `language`, `user_agent`, `geoip` (country, city), `hostname`, `query` |
| `event.transaction` | `protocol`, `redirect_uri`, `requested_scopes`, `acr_values` |
| `event.authentication` | `methods` (array of `{name, timestamp}`), `riskAssessment` (Adaptive MFA — see [[18_mfa]]) |
| `event.secrets` | Secrets configured for this Action (you set them in the Dashboard) |
| `event.stats` | `logins_count` |

---

## The `api` Object — Methods

### Deny login
```js
api.access.deny("reason_code", "User-facing message");
```

### Set custom claims (must be namespaced)
```js
api.idToken.setCustomClaim("https://myapp.example.com/role", "admin");
api.accessToken.setCustomClaim("https://myapp.example.com/role", "admin");
```
> Namespaced URI prevents Auth0 from stripping the claim. Use a URI you own (doesn't have to resolve).

### Set metadata
```js
api.user.setUserMetadata("theme", "dark");
api.user.setAppMetadata("plan", "enterprise");
```
Changes are persisted to the user profile after the Action completes.

### Redirect mid-flow (progressive profiling, terms acceptance)
```js
api.redirect.sendUserTo("https://myapp.example.com/profile-complete", {
  query: { session_token: api.redirect.encodeToken({ secret: event.secrets.MY_SECRET, payload: { ... } }) }
});
```
Pause auth, redirect user to your page, then resume with `onContinuePostLogin` when they return.

### Enable MFA
```js
api.multifactor.enable("any", { allowRememberBrowser: true });
// or specifically: api.multifactor.enable("guardian", { ... })
```

### Step-up / specific factor challenge
```js
api.authentication.challengeWith({ type: "otp" });   // newer API for explicit MFA selection
```

### Cache (across executions)
```js
api.cache.set("key", "value", { ttl: 60000 });
api.cache.get("key");
```

### Add authentication methods (for tracking purposes)
```js
api.authentication.recordMethod("https://example.com/methods/custom");
```

---

## Secrets

Per-Action secrets stored encrypted. Access via `event.secrets.NAME`. Set in the Action editor; never hardcode in source.

## Dependencies (NPM)
Add packages in the Action editor — Auth0 installs them in the runtime sandbox. Common: `axios`, `jsonwebtoken`, vendor SDKs.

## Versioning
Every save creates a new draft. **Deploy** to make it live. Roll back to any prior deployed version.

## Testing
Each trigger has a built-in test runner with a sample event payload. Edit the payload to simulate cases.

## Multiple Actions per trigger
Drag-and-drop ordering. Each Action runs in sequence on the same flow.

---

## Common Patterns

### Custom claim from app_metadata
```js
exports.onExecutePostLogin = async (event, api) => {
  const role = event.user.app_metadata.role || "member";
  api.idToken.setCustomClaim("https://myapp.example.com/role", role);
  api.accessToken.setCustomClaim("https://myapp.example.com/role", role);
};
```

### Block disposable email signups
```js
exports.onExecutePreUserRegistration = async (event, api) => {
  if (event.user.email.endsWith("@10minutemail.com")) {
    api.access.deny("disposable_email", "Please use a permanent email.");
  }
};
```

### Force MFA for admins
```js
exports.onExecutePostLogin = async (event, api) => {
  if (event.user.app_metadata.role === "admin") {
    api.multifactor.enable("any");
  }
};
```

### Use Adaptive MFA risk
```js
exports.onExecutePostLogin = async (event, api) => {
  const risk = event.authentication?.riskAssessment;
  if (risk?.confidence === "low") {
    api.multifactor.enable("any");
  }
};
```

See [[18_mfa]] for MFA + Adaptive details and [[14_rbac]] for using Actions to enrich tokens with RBAC data.
