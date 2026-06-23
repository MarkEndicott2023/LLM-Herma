# Passwordless Authentication

**Auth0 docs:** https://auth0.com/docs/authenticate/passwordless

Authentication without a traditional password. Auth0 supports several channels.

## Available Channels

### Email — Magic Link
- User enters email → receives email with a time-limited link → click logs them in.
- **Magic links work only in Classic Login**, not New Universal Login.

### Email — One-Time Password (OTP / code)
- User enters email → receives email with a numeric code → enters the code.
- Works in both Classic and New Universal Login.

### SMS — One-Time Password
- User enters phone number → receives SMS code → enters the code.
- Works in Universal Login, Classic, and Embedded.

### Passkeys (FIDO WebAuthn)
- Public-key credentials synced across devices via the platform (iCloud Keychain, Google Password Manager).
- Phishing-resistant.

### Social Login & Biometrics
- Social (Google, Facebook, etc.) is technically a form of passwordless authentication.
- WebAuthn-based biometrics (Touch ID, Face ID, Windows Hello, security keys) — see [[18_mfa]].

## Passwordless Connections

Passwordless email and SMS each have their own **connection type**, distinct from database, social, and enterprise connections.

- The user is authenticated through Auth0 (Auth0 is the IdP).
- If the same user logs in with different identifiers (email vs phone), **multiple separate user profiles are created**.
- Use [[11_users_profile]] account linking to consolidate.

## Endpoints (for Embedded Login)

### Start passwordless authentication
```
POST /passwordless/start
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "...",          // confidential apps only
  "connection": "email" | "sms",
  "email": "user@example.com",     // for email
  "phone_number": "+15551234567",  // for SMS
  "send": "link" | "code",         // email only; "code" for OTP, "link" for magic link
  "authParams": { "scope": "openid profile email" }
}
```

### Verify the OTP
```
POST /passwordless/verify   (legacy) — prefer /oauth/token with grant_type=passwordless
POST /oauth/token
grant_type=http://auth0.com/oauth/grant-type/passwordless/otp
&client_id=YOUR_CLIENT_ID
&username=email_or_phone
&otp=THE_CODE
&realm=email | sms
&scope=openid profile email
```

## Limitations

- Cannot create passwordless users via the Dashboard UI — use the Management API (`POST /users` with `connection: "email"` or `"sms"`).
- Magic links are Classic-Login-only.
- Each identifier (email, phone) creates a separate profile by default.

## Security Considerations

- Reduces password breach risk.
- OTP codes are short-lived (typically 3 minutes).
- Phishing risk remains for SMS/email OTP — use passkeys/WebAuthn for phishing resistance.

See [[07_universal_login]] for Universal Login passwordless setup and [[18_mfa]] for WebAuthn details.
