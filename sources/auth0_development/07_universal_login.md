# Universal Login (vs Embedded) and Branding

**Auth0 docs:** https://auth0.com/docs/authenticate/login/auth0-universal-login · https://auth0.com/docs/customize/universal-login-pages

## What is Universal Login

Centralized login experience hosted on the Auth0 Authorization Server domain (e.g., `YOUR_DOMAIN.auth0.com` or your custom domain). Applications redirect users to Auth0 for authentication, then Auth0 redirects back with a code/tokens.

> "Universal Login is hosted on Auth0's Authorization Server, to verify a user's identity."

## Universal vs Embedded Login

| Aspect | Universal Login | Embedded Login |
|---|---|---|
| **Where it runs** | Auth0 domain (centralized) | Inside the application itself |
| **Architecture** | Redirect to `/authorize` | Auth widget on app's domain |
| **CORS issues** | None (no cross-origin) | Requires Allowed Web Origins + Allow Cross-Origin Auth |
| **Updates** | Automatic; no code change | Manual SDK updates |
| **SSO** | Works naturally (Auth0 cookie shared) | Harder; requires same-origin tricks |
| **Compliance / Security** | Smaller attack surface | App handles credentials directly |
| **Recommended?** | **Yes** — strongly preferred | Only when redirect is impossible |

> Auth0 strongly recommends Universal Login. Embedded Login should be used only when the redirect-based flow is impossible.

## Universal Login Experiences

### New Universal Login (NUL) — Recommended
- Modern, page-based.
- No JavaScript hooks to maintain.
- Customized via Page Templates, Branding, and i18n (Prompts).
- Receives active development.
- **Required for Auth0 Organizations.**

### Classic Login — Legacy
- JavaScript-based Lock widget.
- Custom HTML/JS injected.
- No new features; only specific legacy needs.
- **Required for** email magic links.

## Benefits of Universal Login

- **Flexibility** — add passwordless, social, MFA without app code changes.
- **Security** — no CORS, no embedded credentials, smaller attack surface.
- **SSO** — centralized session enables cross-app SSO.
- **Consistency** — same branded login across all apps.
- **Accessibility** — WCAG 2.2 AA and EN 301 549 compliant.

## Required `/authorize` Parameters
```
response_type   code | token | id_token
client_id       app ID
redirect_uri    must match Allowed Callback URLs
state           CSRF protection
```
Optional: `connection`, `scope`, `audience`, `prompt`, `organization`, `nonce`, `screen_hint=signup`.

## Customization

### Branding (Dashboard → Branding)
- **Logo URL**
- **Primary color** and **Page background color**
- **Favicon**
- **Custom Font URL**

### Page Templates (Branding → Universal Login → Advanced Options)
- Liquid-based HTML templates surrounding the prompt.
- Inject custom HTML/CSS, change the page chrome.

### Prompts and Text Customization
- Dashboard → Branding → Universal Login → Customize Text.
- Override copy on each prompt (login, signup, MFA, etc.) per language.
- 30+ supported languages.

### Page-level Customization
- Some prompts can be replaced wholesale via Custom Pages (Management API).

### Custom Domains
- Set up `auth.yourdomain.com` instead of `tenant.auth0.com` — required for production branding and avoids third-party cookie issues.
- **Recommended to enable early** to avoid callback URL churn later.

## Cross-Origin Authentication (Embedded Login support)

If you must embed login:
1. Enable **Allow Cross-Origin Authentication** on the app.
2. Populate **Allowed Web Origins** ([[04_uri_configuration]]).
3. Set **Cross-Origin Verification URL** (a page hosted by your app for fallback).

## Accessibility Features
- Screen-reader-accessible inline validation
- WCAG color contrast
- ARIA attributes
- Required field indicators
- Distinct page titles per screen

See [[16_actions]] for triggering custom logic during the Universal Login flow, [[15_organizations]] for per-org branding, and [[17_email_templates]] for transactional emails.
