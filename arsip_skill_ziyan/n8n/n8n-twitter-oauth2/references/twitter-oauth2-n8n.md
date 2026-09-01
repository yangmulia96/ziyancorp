# Twitter OAuth2 with PKCE in n8n: Reference

## Twitter API Endpoints

- Authorization: `https://twitter.com/i/oauth2/authorize`
- Token: `https://api.twitter.com/2/oauth2/token`
- Revoke: `https://api.twitter.com/2/oauth2/revoke` (if needed)

## PKCE Parameters

- `code_verifier`: A high-entropy cryptographic random string (43-128 chars).
- `code_challenge`: Base64URL-encoded SHA256 hash of the code verifier.
- `code_challenge_method`: S256 (or plain for testing, but not recommended).

## n8n OAuth2 Node Settings

When setting up a generic OAuth2 credential in n8n for Twitter:

- **Authenticate**: Via GET request to authorization URL.
- **Access Token**: Via POST request to token URL.
- **Scope**: Delimited by spaces (as shown above).
- **PKCE**: Enable and set code challenge method to S256.

## Example Token Request (for manual debugging)

```http
POST https://api.twitter.com/2/oauth2/token
Content-Type: application/x-www-form-urlencoded

client_id=<CLIENT_ID>&
client_secret=<CLIENT_SECRET>&
grant_type=authorization_code&
code=<AUTHORIZATION_CODE>&
code_verifier=<CODE_VERIFIER>&
redirect_uri=<REDIRECT_URI>
```