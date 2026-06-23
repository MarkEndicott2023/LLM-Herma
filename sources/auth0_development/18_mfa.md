# Multi-Factor Authentication (MFA)

**Auth0 docs:**
- https://auth0.com/docs/secure/multi-factor-authentication
- https://auth0.com/docs/secure/multi-factor-authentication/adaptive-mfa
- https://auth0.com/docs/secure/multi-factor-authentication/step-up-authentication

## The Three Factor Categories

| Category | aka | Examples |
|---|---|---|
| **Knowledge** | Something you **know** | Password, PIN, security question |
| **Possession** | Something you **have** | Phone (SMS, app), hardware token, smart card, security key |
| **Inherence** | Something you **are** | Fingerprint, Face ID, voiceprint, iris scan |

True MFA requires **at least two factors from different categories**. Two passwords is not MFA.

---

## Supported MFA Factors in Auth0

| Factor | Category | Notes |
|---|---|---|
| **Push Notifications (Auth0 Guardian)** | Possession | Mobile app — best UX |
| **One-Time Password (OTP)** | Possession | TOTP via Authenticator apps |
| **SMS** | Possession | Vulnerable to SIM swap |
| **Voice** | Possession | Phone call delivering code |
| **Email** | Possession | OTP sent to email |
| **WebAuthn with Security Keys (FIDO2 roaming)** | Possession | YubiKey, Titan Key |
| **WebAuthn with Platform Biometrics** | Possession + Inherence | Touch ID, Face ID, Windows Hello |
| **Cisco Duo Security** | Varies | 3rd-party Duo integration |
| **Recovery Codes** | Possession | One-time backup codes |

### Plan availability
"MFA factors are subject to plan availability; some are only available on Professional and Enterprise plans."

---

## Enabling MFA

Dashboard → Security → Multi-factor Auth.

1. **Enable factors** — toggle which factors are available tenant-wide.
2. **Set Policy** — when MFA is enforced.

### Global MFA Policies
| Policy | Behavior |
|---|---|
| **Never** | MFA never enforced (users can still self-enroll if you allow). |
| **Always** | Every login requires MFA. |
| **Use Adaptive** | Adaptive MFA decides based on risk signals (Enterprise plan + addon). |

### Policy Precedence
> Actions methods (`api.multifactor.enable(...)`) override the global tenant policy for that specific login.

So you can run "Never" globally and use an Action to enforce MFA only for admins, or run "Always" globally and skip MFA for low-risk service accounts.

---

## Enrollment

Users enroll a factor:
- On their first MFA-required login (forced enrollment).
- Via the user's account page if you build one (`POST /api/v2/users/{id}/multifactor/...`).
- Through a Guardian invitation email.

A user can have multiple factors enrolled; Auth0 picks one for challenge based on priority/availability.

---

## Adaptive MFA

**Plan requirement: Enterprise + Adaptive MFA addon.**

Risk-based MFA — only challenges when login confidence is low. Reduces friction for legitimate users.

### Three Risk Assessors

| Assessor | Signal |
|---|---|
| **NewDevice** | User signing in from a device not used in the **last 30 days**. Device identification via user agent + browser cookies. |
| **ImpossibleTravel** | Geolocation indicates the user couldn't have traveled between this login and the previous one in the elapsed time. |
| **UntrustedIP** | IP appears on Auth0's threat intelligence as associated with suspicious activity. |

### Confidence Levels
Each assessor returns a confidence: **low**, **medium**, or **high**. Auth0 also computes an overall confidence combining all three.

### Accessing Risk in Actions
```js
exports.onExecutePostLogin = async (event, api) => {
  const risk = event.authentication?.riskAssessment;
  if (!risk) return;

  const { confidence, assessments } = risk;
  // assessments.NewDevice.confidence === "low" | "medium" | "high"
  // assessments.ImpossibleTravel.confidence === ...
  // assessments.UntrustedIP.confidence === ...

  if (confidence === "low") {
    api.multifactor.enable("any");
  }
};
```

### Critical Behavior
> "Adaptive MFA ignores any and all existing MFA sessions...and does not allow users to bypass MFA challenges."

### Supported Flows
✓ Auth Code (+ PKCE), Implicit Form Post, Hybrid, SAML SP-initiated, WS-Fed, AD/LDAP, Universal Login, Classic Login.
✗ Client Credentials, Device Authorization, ROPG (limited), SAML IdP-initiated.

### Social Connection Requirement
Adaptive MFA needs an email for the email challenge. Social connections without email blocked.

---

## Step-Up Authentication

Triggered mid-session when a user requests a **sensitive resource**, even after a successful login.

### vs Adaptive MFA
| | Adaptive MFA | Step-Up |
|---|---|---|
| **Trigger** | Risk signal at login | Resource sensitivity, post-login |
| **When** | Login | After login (during app use) |
| **Decided by** | Auth0 risk score | App business logic |

### Implementation Patterns

#### For APIs (scope-based)
1. App requests a sensitive scope (e.g., `transfer:funds`) at `/authorize`.
2. Post-Login Action detects the requested scope and enables MFA:
```js
exports.onExecutePostLogin = async (event, api) => {
  if (event.transaction.requested_scopes.includes("transfer:funds")) {
    api.multifactor.enable("any");
  }
};
```
3. Auth0 challenges MFA, then issues a token with the sensitive scope.

#### For Web Apps (ID token claim check)
1. App checks user's ID token for `amr` (authentication methods) — if MFA not in `amr`, require MFA.
2. Trigger a re-auth: `/authorize?...&acr_values=...` or `&prompt=login` with MFA enforced via Action.

### Useful claims
- `amr` — Authentication Methods References (array): `["pwd"]`, `["pwd", "mfa"]`, `["pwd", "otp"]`, etc.
- `acr` — Authentication Context Class Reference: e.g., `http://schemas.openid.net/pape/policies/2007/06/multi-factor`
- `auth_time` — when the user authenticated
- `max_age` parameter at `/authorize` forces re-auth if last auth was too long ago

---

## WebAuthn / FIDO2

Public-key cryptography-based authentication. The strongest factor: phishing-resistant.

### Mechanism
1. **Registration:** Browser + authenticator generate a key pair. **Public key** stored in Auth0; **private key** stays on the device.
2. **Authentication:** Auth0 sends a challenge (random bytes). Authenticator signs with the private key. Auth0 verifies with the stored public key.
3. **Origin binding:** The signature is bound to the requesting origin (your custom domain). A phishing site can't reuse the signature.

### Authenticators
- **Roaming (Cross-platform):** Hardware security keys — YubiKey, Google Titan, FIDO2 keys.
- **Platform (Built-in):** Touch ID / Face ID (macOS, iOS), Windows Hello, Android biometrics.

### Why phishing-resistant
The challenge response is signed for a specific origin. If a phishing site (`evil.com` impersonating `bank.com`) tries to relay the challenge, the authenticator refuses because the origin doesn't match the registered relying party ID.

### Device-bound credentials (important!)
- A WebAuthn credential is **bound to a specific device**.
- **New device → new enrollment required.** The user must register WebAuthn separately on each device (or use passkeys for cross-device sync).
- Multiple credentials can be enrolled per user (e.g., one YubiKey + one platform key).

### AAL3 (see below)
WebAuthn with security keys or platform biometrics satisfies AAL3 — the highest assurance level.

---

## Authentication Assurance Levels (AAL)

Defined in NIST 800-63-3.

| AAL | Description | Auth0 Example |
|---|---|---|
| **AAL1** | Single factor | Password only |
| **AAL2** | Two factors, neither necessarily phishing-resistant | Password + SMS OTP, Password + TOTP |
| **AAL3** | Two factors with a **phishing-resistant** factor | Password + WebAuthn (FIDO2) |

**Phishing-resistant factors:** WebAuthn (FIDO2) hardware keys, platform biometrics. NOT SMS, NOT TOTP, NOT email.

---

## Customizing MFA in Actions
Beyond `api.multifactor.enable()`, you can:
- Conditionally challenge based on app, role, risk
- Configure `allowRememberBrowser` for "Trust this browser for 30 days"
- Skip MFA for service accounts

See [[16_actions]] for the API surface, [[19_attack_protection]] for related security signals, and [[06_passwordless]] for passkey-based passwordless (related WebAuthn use).
