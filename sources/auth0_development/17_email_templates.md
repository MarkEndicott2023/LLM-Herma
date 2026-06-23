# Email Templates and SMTP

**Auth0 docs:** https://auth0.com/docs/customize/email/email-templates · https://auth0.com/docs/customize/email/smtp-email-providers

## Default Email Provider

Built-in, no setup, but **for development only**:
- **From address locked** to `no-reply@auth0user.net`.
- **Rate limit: 10 emails per minute** across all email types.
- No template customization allowed.
- High bounce rates trigger sending restrictions.

For production: configure an external SMTP provider.

## Email Templates Available

Dashboard → Branding → Email Templates.

| Template | Trigger |
|---|---|
| **Verification Email (Link)** | User signs up or first login — link to verify email |
| **Verification Email (Code)** | When code-based verification is enabled |
| **Welcome Email** | After email is verified (or after signup if no verification required) |
| **Change Password (Link)** | User requests password reset |
| **Change Password (Code)** | Code-based password change |
| **Blocked Account** | Brute-force protection blocked the account |
| **Password Breach Alert** | Breached Password Detection notified the user |
| **MFA Enrollment** | Admin sends Guardian invitation |
| **MFA Verification Code** | Email-channel MFA OTP |
| **Passwordless OTP** | Passwordless email OTP — configured separately |
| **User Invitation** | Org invitation |
| **Async User Notification** | Custom notifications |

### Liquid Templating
Email templates use **Liquid** syntax:
```liquid
Hello {{ user.name }},

Welcome to {{ application.name }}!

{% if user.email_verified %}
  Your email is verified.
{% else %}
  Please verify: {{ url }}
{% endif %}
```

### Common Liquid variables
- `{{ user.name }}`, `{{ user.email }}`, `{{ user.email_verified }}`
- `{{ application.name }}`, `{{ application.logo_url }}`, `{{ application.callback_domain }}`
- `{{ connection.name }}`
- `{{ url }}` — the verification/reset link
- `{{ code }}` — the OTP code
- `{{ organization.name }}`, `{{ organization.display_name }}` — for org-scoped emails
- `{{ ULP_AUTH_PARAMS }}` — preserved auth params for continuation

### Configuration Per Template
- **Subject** — supports Liquid.
- **From** — must not contain `@auth0.com`.
- **HTML body** — all emails must be HTML (no plain text).
- **Redirect To URL** — where user lands after clicking the link.
- **Enable** — toggle.
- **URL Lifetime** — link/code expiration (default varies; password reset typically 5 days).

### Conditional Templates
Only one template per type, but use Liquid conditionals on `{{ connection.name }}`, `{{ application.name }}`, or `{{ organization.id }}` to vary content per context.

---

## Custom SMTP Configuration

### Native integrations (Dashboard → Branding → Email Provider)
1. **Amazon SES**
2. **Azure Communication Services**
3. **Mailgun**
4. **Mandrill** (Mailchimp Transactional)
5. **Microsoft 365 Exchange Online**
6. **Resend**
7. **SendGrid**
8. **SparkPost**

Each requires the provider's API key/credentials.

### Generic SMTP
Connect any SMTP server with:
- `host`
- `port` (typically 587 for STARTTLS, 465 for SSL/TLS, 25 unencrypted — don't)
- `username`
- `password`
- `from address`

### Auth0 blocks test domains
Don't use `@example.com`, `@test.com` — Auth0 rejects them to prevent misconfig.

### Test SMTP services for local dev
- Debug Mail
- FakeSMTP
- smtp4dev

### Custom email provider via Action
Maximum flexibility: implement an Action (e.g., on `post-user-registration`) that calls any email API (SendGrid, Postmark, custom). Bypasses Auth0's email provider entirely for non-transactional sends.

---

## Enabling Templates
After configuring SMTP and customizing a template, toggle the template's **Status: Enabled**. Templates are off by default after a fresh SMTP config.

## Testing
- Each template has a "Try" button to send a test email.
- Test with realistic Liquid variable values via the template preview.

See [[07_universal_login]] for related branding (logos, colors) and [[18_mfa]] for the MFA enrollment email flow.
