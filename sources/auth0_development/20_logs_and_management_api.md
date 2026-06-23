# Tenant Logs, Log Streams, and Management API

**Auth0 docs:**
- https://auth0.com/docs/deploy-monitor/logs
- https://auth0.com/docs/customize/log-streams
- https://auth0.com/docs/api/management/v2

---

## Tenant Logs

Dashboard → Monitoring → Logs.

### What's logged
- Tenant admin actions
- User authentication events (success/failure)
- Management API calls
- Attack protection actions
- Action execution / errors
- Login transactions with X-Correlation-ID

### Retention
Varies by plan — typically a few days for free tier, up to 30 days for paid tiers, longer with log streams to external storage.

### Event Type Codes (authoritative — from https://auth0.com/docs/deploy-monitor/logs/log-event-type-codes)

Naming convention: prefix `s` = success, `f` = failed, `gd_` = Guardian (MFA), `limit_` = rate/attack limits.

#### Login / Auth
| Code | Meaning |
|---|---|
| `s` | Successful login |
| `f` | Failed login |
| `fp` | Failed login (incorrect password) |
| `fu` | Failed login (invalid email/username) |
| `fsa` | Failed silent authentication |
| `ssa` | Successful silent authentication |
| `w` / `wum` | Warning during login / user management |
| `scoa` / `fcoa` | Success / failed cross-origin authentication |
| `fco` | Origin is not in the Allowed Origins list for the application |

#### Signup / Invitations
| Code | Meaning |
|---|---|
| `ss` | Successful signup |
| `fs` | Failed signup |
| `si` | Successfully accepted a user invitation |
| `fi` | Failed to accept invitation (e.g., different email than invited) |

#### Logout
| Code | Meaning |
|---|---|
| `slo` | User successfully logged out |
| `flo` | User logout failed |
| `federated_logout_failed` | Failed to logout of the upstream Identity Provider |
| `oidc_backchannel_logout_succeeded` | Successful OIDC Back-Channel Logout request |
| `oidc_backchannel_logout_failed` | Failed OIDC Back-Channel Logout request |
| `universal_logout_succeeded` | Successful Universal Logout request |
| `universal_logout_failed` | Failed Universal Logout request |
| `srrt` | Successfully revoked a refresh token |

#### Token Exchange (`eXft` = exchange-X-for-token)
| Code | Meaning |
|---|---|
| `seacft` / `feacft` | Auth code → access token (success / failed) |
| `seccft` / `feccft` | Client credentials → access token |
| `sede` / `fede` | Device code → access token |
| `sertft` / `fertft` | Refresh token → access token |
| **`ferrt`** | **Rotating Refresh Token reuse detected — entire family invalidated** |
| `sepft` / `fepft` | Password → access token (ROPG) |
| `seoobft` / `feoobft` | Password + OOB MFA challenge → access token |
| `seotpft` / `feotpft` | Password + OTP challenge → access token |
| `sercft` / `fercft` | Password + MFA recovery code → access token |
| `fepotpft` | Failed exchange of passwordless OTP for access token |
| `sens` / `fens` | Native social login exchange |
| `secte` / `fecte` | Custom Token Exchange |

#### Password & Credentials
| Code | Meaning |
|---|---|
| `pwd_leak` | **Login attempt with a leaked (breached) password** |
| `signup_pwd_leak` | Signup attempt with a leaked password |
| `reset_pwd_leak` | Password reset attempt with a leaked password |
| `scp` / `fcp` | Success / failed change password |
| `scpr` / `fcpr` | Success / failed change password request |

#### User Management
| Code | Meaning |
|---|---|
| `sdu` | User successfully deleted |
| `fdu` | Failed user deletion |
| `scu` / `fcu` | Success / failed change username |
| `sce` / `fce` | Success / failed change email |
| `scpn` / `fcpn` | Success / failed change phone number |
| `sui` / `fui` | Success / failed user import |
| `scv` | Successful credential validation |

#### Email Verification
| Code | Meaning |
|---|---|
| `sv` | Successfully consumed email verification link |
| `fv` | Failed to send verification email |
| `svr` / `fvr` | Success / failed verification email **request** |

#### Rate Limits & Attack Protection
| Code | Meaning |
|---|---|
| **`limit_wc`** | **IP blocked because it reached the max failed logins into a single account (Brute-Force Protection)** |
| **`limit_mu`** | **IP blocked because it attempted too many failed logins without a successful login (Suspicious IP Throttling)** |
| `limit_sul` | User temporarily prevented from logging in — too many logins per time period |
| `limit_delegation` | Rate limit exceeded to `/delegation` endpoint |
| **`api_limit`** | **Max requests to Authentication or Management APIs reached** |
| `api_limit_warning` | API rate limit about to be reached |
| **`pla`** | **Pre-login bot detection assessment** (monitoring without enforcement) |
| `ublkdu` | User-block from anomaly detection has been released |

#### MFA / Guardian
| Code | Meaning |
|---|---|
| `mfar` | User prompted for MFA |
| `gd_start_auth` | Second-factor auth started |
| `gd_start_enroll` | MFA enrollment started |
| `gd_enrollment_complete` | First-time MFA user successfully enrolled |
| `gd_auth_succeed` | MFA success |
| `gd_auth_failed` | MFA failed (wrong code) |
| `gd_auth_rejected` | User rejected MFA push notification |
| `gd_send_sms` / `gd_send_sms_failure` | SMS sent / failed |
| `gd_send_email` / `gd_send_email_verification_failure` | Email sent / failed |
| `gd_send_pn` / `gd_send_pn_failure` | Push notification sent / failed |
| `gd_send_voice` / `gd_send_voice_failure` | Voice call sent / failed |
| `gd_otp_rate_limit_exceed` | User sent >10 requests to their device within one hour |
| `gd_recovery_succeed` / `gd_recovery_failed` | Recovery code success / failed |
| `gd_recovery_rate_limit_exceed` | Too many wrong recovery codes |
| `gd_unenroll` | Device unenrolled from second factor |
| `gd_update_device_account` | Second-factor device updated |
| `gd_webauthn_challenge_failed` | WebAuthn factor verification failed |
| `gd_webauthn_enrollment_failed` | WebAuthn enrollment failed |
| `gd_tenant_update` | Guardian tenant update |

#### Passkeys (Native)
| Code | Meaning |
|---|---|
| `passkey_challenge_started` | Native passkey challenge initiated |
| `passkey_challenge_failed` | Native passkey challenge failed |
| `sepkoobft` | Successful exchange of Passkey + OOB challenge for access token |
| `sepkotpft` | Successful exchange of Passkey + OTP challenge for access token |
| `sepkrcft` | Successful exchange of Passkey + MFA recovery code for access token |

#### Passwordless
| Code | Meaning |
|---|---|
| `cls` | Passwordless login code/link sent |
| `cs` | Passwordless login code sent |

#### CIBA (Backchannel Authentication)
| Code | Meaning |
|---|---|
| `ciba_start_succeeded` / `ciba_start_failed` | CIBA flow initiated success / failed |
| `ciba_exchange_succeeded` / `ciba_exchange_failed` | AuthReqId → access token success / failed |

#### Device Flow
| Code | Meaning |
|---|---|
| `fdeaz` | Device authorization request failed |
| `fdeac` | Failed to activate device |
| `fdecc` | User did not confirm device |

#### Hooks / Actions / Flows / Forms
| Code | Meaning |
|---|---|
| `actions_execution_failed` | Action execution failed |
| `fcph` | Failed Post-Change-Password Hook |
| `fpurh` | Failed Post-User-Registration Hook |
| `flows_execution_completed` / `flows_execution_failed` | Flows execution events |
| `forms_submission_succeeded` / `forms_submission_failed` | Forms submission events |

#### Management API
| Code | Meaning |
|---|---|
| `sapi` | Successful Management API write |
| `mgmt_api_read` | API GET returning secrets succeeded |

#### Organizations / SCIM
| Code | Meaning |
|---|---|
| `organization_member_added` | Successfully added member to organization |
| `sscim` | SCIM operation succeeded |

#### Delegation / Connector
| Code | Meaning |
|---|---|
| `sd` / `fd` | Success / failed delegation token |
| `fcpro` | Failed to provision AD/LDAP connector |
| `fc` | Failed by Connector |

#### Notifications & Admin
| Code | Meaning |
|---|---|
| `fn` | Failed to send notification |
| `wn` | Warnings during notification sending |
| `depnote` | Deprecation Notice |
| `appi` | Increases elevated Authentication API limits |
| `too_many_records` | User created max amount of authenticators |
| `resource_cleanup` | Resources exceeding defined limits removed |

### Searching
- Filter by event type code: `type:s` or `type:fp`
- Filter by user: `user_id:auth0|abc123`
- Filter by client: `client_id:YOUR_CLIENT_ID`
- Time range filter built into Dashboard
- Combine: `type:f AND ip:1.2.3.4`

### Correlation
Pass `X-Correlation-ID` header in API calls (max 64 chars) — appears in logs for tracing.

---

## Log Streams

Real-time export of logs to external systems. Dashboard → Monitoring → Streams.

### Delivery semantics
- "Delivers each log to your server as it is triggered in our system."
- **At-least-once** delivery, up to 3 retries per log.
- **Order not guaranteed** by default — apps must sort if chronological order matters.

### Supported Destinations
| Category | Integrations |
|---|---|
| **Cloud event buses** | Amazon EventBridge, Azure Event Grid |
| **SIEM / observability** | Datadog, Splunk, Sumo Logic, Elastic, Logz.io |
| **Data platforms** | Mixpanel, Segment |
| **Security / SOC** | Panther, Pangea, Perch, MDR ONE, Oort, Oodle AI |
| **Messaging** | Slack |
| **Generic** | HTTP webhook |

### Event filtering
Select which event categories to stream / exclude.

### PII Obfuscation
Two methods:
- **Masking** — replace value with asterisks.
- **xxHash** — non-cryptographic hash (deterministic for joins).

Fields that can be obfuscated: `first_name`/`given_name`, `last_name`/`family_name`, `email`, `phone`/`phone_number`, `address`, `username`/`user_name`.

### Stream Health
- Streams **auto-pause after 7 consecutive days of delivery failures**.
- Manual intervention required to resume.
- Errors visible in Dashboard.

### Operational note
"Log streams should not be used in your application's critical path or for real-time decision-making" — they're for monitoring and audit, not authorization.

---

## Management API

Base URL: `https://YOUR_DOMAIN/api/v2/`

### Authentication
- Get an access token via **Client Credentials** flow ([[05_authentication_flows]]).
- **Audience:** `https://YOUR_DOMAIN/api/v2/`
- Token sent as `Authorization: Bearer ACCESS_TOKEN`.
- **Token expires** based on M2M settings (typically 24h). Cache and refresh.

### Authorization
Scope-based. Examples: `read:users`, `update:users`, `create:roles`, `read:logs`, `read:client_grants`.

Request returns:
- `200/201/204` — success
- `401` — invalid/expired token
- `403` — token lacks required scope
- `404` — resource not found
- **`429`** — rate limit exceeded → check `X-RateLimit-Reset` header, retry with exponential backoff
- `5xx` — server error → retry

### Pagination

#### Offset-based (for small datasets, < ~1,000 items)
```
GET /api/v2/users?page=0&per_page=50
```
- `page` — zero-indexed.
- `per_page` — max 50 (Public Cloud) / 100 (Private Cloud).
- Suitable for UI pagination of small collections.
- **Don't use** for full table scans — perf degrades.

#### Checkpoint-based (for large datasets, > 1,000 items)
```
GET /api/v2/clients?take=50&from=Cg1HRUY3NEszUERFME40GgAi...
```
- `take` — page size (max 50 Public Cloud / 100 Private).
- `from` — opaque checkpoint from previous response's `next` field.
- **Forward-only** (no jumping to arbitrary pages).
- **Checkpoint validity: 24 hours.** After that, restart from beginning.
- Use for full exports / bulk processing.

### Naming Conventions
- **Multi-word resources use hyphens**, NOT camelCase:
  - `/api/v2/jobs/users-exports` ✓
  - `/api/v2/jobs/usersExports` ✗
  - `/api/v2/client-grants` ✓
- Many-to-many relationships exposed on both sides (e.g., `/users/{id}/roles` AND `/roles/{id}/users`).

### Payload size
- Max request body: **1 MB**.

### Rate Limits
Strict per-endpoint limits. Hit a limit → 429 → respect `Retry-After` header → exponential backoff.

### Correlation IDs
`x-correlation-id` header (max 64 chars) for log correlation.

---

## Key Endpoint Reference

### Users
```
GET    /api/v2/users
POST   /api/v2/users
GET    /api/v2/users/{id}
PATCH  /api/v2/users/{id}
DELETE /api/v2/users/{id}
GET    /api/v2/users-by-email      ← hyphenated
GET    /api/v2/users/{id}/logs
GET    /api/v2/users/{id}/permissions
POST   /api/v2/users/{id}/permissions
DELETE /api/v2/users/{id}/permissions
GET    /api/v2/users/{id}/roles
POST   /api/v2/users/{id}/roles
DELETE /api/v2/users/{id}/roles
GET    /api/v2/users/{id}/multifactor/{provider}
DELETE /api/v2/users/{id}/multifactor/{provider}
POST   /api/v2/users/{id}/identities      ← account linking
DELETE /api/v2/users/{id}/identities/{provider}/{secondary_user_id}
```

### Roles
```
GET    /api/v2/roles
POST   /api/v2/roles
GET    /api/v2/roles/{id}
PATCH  /api/v2/roles/{id}
DELETE /api/v2/roles/{id}
GET    /api/v2/roles/{id}/permissions
POST   /api/v2/roles/{id}/permissions
DELETE /api/v2/roles/{id}/permissions
GET    /api/v2/roles/{id}/users
```

### Organizations
```
GET    /api/v2/organizations
POST   /api/v2/organizations
GET    /api/v2/organizations/{id}
PATCH  /api/v2/organizations/{id}
DELETE /api/v2/organizations/{id}
GET    /api/v2/organizations/{id}/members
POST   /api/v2/organizations/{id}/members        ← max 10 members per call
DELETE /api/v2/organizations/{id}/members
GET    /api/v2/organizations/{id}/members/{user_id}/roles
POST   /api/v2/organizations/{id}/members/{user_id}/roles
DELETE /api/v2/organizations/{id}/members/{user_id}/roles
GET    /api/v2/organizations/{id}/enabled_connections
POST   /api/v2/organizations/{id}/enabled_connections
GET    /api/v2/organizations/{id}/invitations
POST   /api/v2/organizations/{id}/invitations
```

### Jobs (bulk async operations)
```
POST /api/v2/jobs/users-exports     ← hyphenated
POST /api/v2/jobs/users-imports
POST /api/v2/jobs/verification-email
GET  /api/v2/jobs/{id}
GET  /api/v2/jobs/{id}/errors
```

### Tickets (generate one-off action links)
```
POST /api/v2/tickets/email-verification
POST /api/v2/tickets/password-change
```

### Connections, Clients, Resource Servers
```
GET/POST/PATCH/DELETE  /api/v2/connections
GET/POST/PATCH/DELETE  /api/v2/clients
GET/POST/PATCH/DELETE  /api/v2/resource-servers    ← APIs (hyphenated)
GET/POST/DELETE        /api/v2/client-grants       ← M2M grants
```

### Attack Protection
```
GET    /api/v2/attack-protection/brute-force-protection
PATCH  /api/v2/attack-protection/brute-force-protection
GET    /api/v2/attack-protection/suspicious-ip-throttling
PATCH  /api/v2/attack-protection/suspicious-ip-throttling
GET    /api/v2/attack-protection/breached-password-detection
PATCH  /api/v2/attack-protection/breached-password-detection
DELETE /api/v2/user-blocks/{id}                    ← unblock a user
```

### Logs
```
GET /api/v2/logs
GET /api/v2/logs/{id}
GET /api/v2/log-streams
POST /api/v2/log-streams
```

## Path Construction Heuristics
- Top-level collection: `/api/v2/{collection}` (e.g., `/users`, `/roles`).
- Single item: `/api/v2/{collection}/{id}`.
- Sub-collection: `/api/v2/{collection}/{id}/{sub-collection}` (e.g., `/users/{id}/roles`).
- Bulk async operations: under `/api/v2/jobs/` with **hyphenated** names; POST to start, GET to poll.
- One-shot link generation: under `/api/v2/tickets/`; POST to create.
- All paths start with `/api/v2`. The auth endpoints (`/authorize`, `/oauth/token`, `/oidc/logout`, `/userinfo`, `/passwordless/*`, `/mfa/*`) live at the tenant root, not under `/api/v2`.
