# Identifier-First Login, Home Realm Discovery, Flexible Identifiers

**Auth0 docs:** https://auth0.com/docs/authenticate/login/auth0-universal-login/identifier-first

## Identifier-First Authentication

Two-step login: user enters identifier first, then provides credentials on a separate screen. The first screen lets Auth0 route the user to the right connection (especially for enterprise SSO).

> "Prompt users for their identifier and authentication method in two separate steps."

Available **only in New Universal Login**.

### How it works
1. User lands on login page → sees only an identifier field (email, username, or phone).
2. User enters identifier.
3. Auth0 checks if the domain (for email) matches an enterprise connection.
4. **If match:** redirect to the enterprise IdP. User never enters a password on Auth0.
5. **If no match:** show password prompt (or biometrics) on Auth0's screen using the database connection.

### Three Authentication Profile Flows (Dashboard → Authentication → Authentication Profile)

| Flow | Description |
|---|---|
| **Identifier + Password** | Both fields on the same screen (default). |
| **Identifier First** | Two screens. Email → routing via HRD → password OR enterprise. |
| **Identifier First + Biometrics** | Same as above but also offers WebAuthn/passkey enrollment. |

### Benefits
- **Personalized experience** — show the right login method per user.
- **Enterprise SSO routing** — `user@acme.com` → ACME's IdP automatically.
- **Multiple credential types** — passwords, biometrics, passwordless.
- **B2B flexibility** — pairs naturally with Organizations.

---

## Home Realm Discovery (HRD)

The mechanism that routes a user to the correct enterprise connection based on the **domain part of their email**.

### Configuration
Dashboard → Authentication → Enterprise → [your connection] → **Domains**

Add the domains the connection should handle (e.g., `acme.com`, `acme.co.uk`).

### Limit
- **Maximum 1,000 domains per enterprise connection** for HRD.

### Behavior
1. User types `bob@acme.com` on the identifier-first screen.
2. Auth0 looks at the domain (`acme.com`).
3. Finds it matches the ACME SAML connection.
4. Redirects to ACME's IdP — Bob signs in there with his ACME credentials.
5. ACME returns the SAML assertion → Auth0 creates/updates the user → app gets the tokens.

### When no domain matches
Auth0 falls back to the configured database / passwordless connection, prompting for password.

### Forcing a connection at `/authorize`
Apps can also force a specific connection per request:
```
/authorize?...&connection=acme-saml
```
This bypasses HRD discovery — useful for "Login with ACME" buttons.

---

## Flexible Identifiers

By default the identifier is **email**. Flexible Identifiers let you accept **email, username, or phone number** as the login identifier on database connections.

### Configuration
Dashboard → Authentication → Database → [connection] → **Attributes**:
- **Email** — toggle as identifier, require verification, allow unique
- **Username** — toggle as identifier, set length/format rules
- **Phone Number** — toggle as identifier, require verification

You can enable any combination. Users may then sign up and log in with any enabled identifier.

### Implications
- Identifier-first flow must accept all enabled types.
- Account linking complexity grows — different identifiers may create separate profiles.
- Some IdPs may not return all identifier types in their claims.

---

## Exam-relevant integration points

| Concept | Relevant area |
|---|---|
| Identifier-first requires New Universal Login | [[07_universal_login]] |
| HRD configured per enterprise connection | [[08_connections]] |
| HRD max 1000 domains per connection | This doc |
| `connection` param at `/authorize` bypasses HRD | [[05_authentication_flows]] |
| Flexible identifiers on database connections | [[08_connections]] |
| Multiple identifiers may create multiple profiles | [[11_users_profile]] account linking |
