# Attack Protection (Brute-Force, Suspicious IP, Bot Detection, Breached Password, CSRF/Replay)

**Auth0 docs:** https://auth0.com/docs/secure/attack-protection · https://auth0.com/docs/secure/attack-protection/state-parameters

Dashboard → Security → Attack Protection.

## 1. Brute-Force Protection

Detects repeated failed login attempts from a **single IP to a single user account**.

### Threshold
- **Shield:** "Default" sets the threshold to **10** consecutive failed attempts.
- **Custom:** lets you set the threshold to any value **between 1 and 100**.

### Response Options (configured independently)

1. **Block Brute-force Logins** *(enabled by default)* — restricts further login attempts from the triggering IP address for that user account. The legitimate user can still log in from another IP.

2. **Account Lockout** *(disabled by default)* — stricter: prevents **all** login attempts for the affected user, regardless of IP, until unblocked.

3. **Send notifications to affected users** — Auth0 delivers SMS or email alerts when accounts are blocked.
   - **SMS rate limit: max 1 per hour per identifier.**
   - **Email rate limit: max 1 per hour per IP.**

The "Blocked Account" email template ([[17_email_templates]]) is used for the email notifications.

### Log codes
- `limit_wc` — "An IP address is blocked because it reached the maximum failed login attempts into a single account."
- `f` (failed login), `fp` (incorrect password), `fu` (invalid email/username) — see [[20_logs_and_management_api]]

### Unblocking
- Self-service: user clicks the "Unblock my account" link in the email.
- Admin: Dashboard → User Management → User → Unblock, or Management API `DELETE /api/v2/user-blocks/{id}`.

---

## 2. Suspicious IP Throttling

Detects high-rate login/signup attempts coming from a **single IP** (across many accounts).

### What it catches
Credential-stuffing attacks where the attacker iterates through leaked credentials against many accounts from one IP.

### Configuration
- **Maximum attempts** — login and signup thresholds (rate-based).
- **Detection** — tracks per-IP velocity.

### Response Options
- Block subsequent attempts from the IP.
- Send email to affected users (if their accounts were targeted).
- Notify admins.

### Log code
- `limit_mu` — IP blocked by Suspicious IP Throttling.

---

## 3. Bot Detection

Risk-based CAPTCHA challenge for login attempts that look like bot activity.

### Trigger Modes
| Mode | Behavior |
|---|---|
| **Never** | Never show CAPTCHA. |
| **Always** | Always show CAPTCHA on login. |
| **When Risky** | Show CAPTCHA when Auth0's risk score suggests bot — tune sensitivity. |

### Risk sensitivity (for "When Risky" mode)
- **Low** — fewer false positives, fewer CAPTCHA prompts; lets some bots through.
- **Medium** — balanced.
- **High** — more aggressive; more legitimate users see CAPTCHA but blocks more bots.

### How it scores
Auth0 evaluates IP reputation, request patterns, behavioral signals. Suspicious sources get CAPTCHA-challenged.

### Log code
- `pla` — pre-login bot detection assessment.

---

## 4. Breached Password Detection

Checks user-supplied passwords against a third-party breach database. If the password appears in a known breach, take action.

### Detection sources
Auth0 maintains a database of breached credentials sourced from Have I Been Pwned-style feeds and similar.

### Response Options (configurable per detection)
- **Send email to user** — Password Breach Alert email ([[17_email_templates]]).
- **Block login until password reset** — force password change.
- **Notify admins**.
- **Run an Action** — for custom handling.

### When it checks
- On every login (validates user's password against breach DB).
- On signup (rejects breached passwords).
- On password change (rejects new breached passwords).

### Log code
- `pwd_leak` — breached password detected.

---

## CSRF Protection — the `state` parameter

OAuth flows are vulnerable to CSRF (forged authentication responses, unsolicited authentication). The `state` parameter mitigates this.

### How state works
1. **Generate** a unique, opaque, **non-guessable** value (cryptographic random, e.g., 32+ bytes).
2. **Store** locally:
   - RWA → cookie or session
   - SPA → local browser storage
   - Native → memory or secure storage
3. **Send** with the `/authorize` request:
   ```
   /authorize?...&state=GENERATED_VALUE
   ```
4. Auth0 reflects `state` back on the callback.
5. **Verify** the returned state matches what you stored. Reject if mismatch.

### Also serves application state restoration
State can encode where to return the user after login (e.g., base64-encoded JSON of the original URL).

### Storage signing
If storing state in a cookie, **sign it** to prevent tampering.

---

## Replay Protection — the `nonce` parameter

Specific to **ID tokens** to prevent token replay attacks.

### How nonce works
1. Generate a random `nonce` before redirect.
2. Send with `/authorize`:
   ```
   /authorize?...&nonce=GENERATED_NONCE
   ```
3. Auth0 includes the `nonce` in the issued ID token's claims.
4. App **validates** the `nonce` claim in the ID token matches what was sent.
5. A replayed ID token from a previous session would carry a different nonce → reject.

### Differences vs state
| | `state` | `nonce` |
|---|---|---|
| Protects against | CSRF | ID token replay |
| Validated against | Local storage | ID token claim |
| Used in | Any OAuth flow | OIDC flows that issue ID tokens |
| Carried back via | Callback query param | ID token claim |

Both are independent and **both should be used** in OIDC flows.

---

## Best Practices Summary

1. Enable all four attack protection layers in production.
2. Always send `state` on `/authorize`; always validate on callback.
3. Always send `nonce`; always validate the ID token's `nonce` claim.
4. Pair Bot Detection with MFA — together they're a strong defense against credential stuffing.
5. Monitor logs ([[20_logs_and_management_api]]) for `limit_wc`, `limit_mu`, `pla`, `pwd_leak` event codes.
6. Use Custom Domains so cookies / session bindings work correctly with attack protection signals.
