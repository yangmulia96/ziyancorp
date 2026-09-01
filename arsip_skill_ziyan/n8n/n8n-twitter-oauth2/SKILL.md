---
name: n8n-twitter-oauth2
description: Enable Twitter API access in n8n via OAuth 2.0 PKCE.
category: n8n
---

# n8n Twitter OAuth2 with PKCE

This skill describes how to configure Twitter (X) OAuth 2.0 with PKCE in n8n to enable automated tweeting without browser flows.

## Prerequisites

- A Twitter Developer account and approved project.
- n8n instance (self-hosted or cloud) with internet access to Twitter API.

## Twitter App Registration

1. Go to [Twitter Developer Portal](https://developer.twitter.com/).
2. Create a new Project and App.
3. Note the **Client ID** and **Client Secret**.
4. Set the **Redirect URI** to your n8n instance's OAuth callback URL (e.g., `https://your-n8n-domain.com/oauth2-callback`).
5. Under "OAuth 2.0", enable **PKCE**.
6. Specify the following scopes: `tweet.read`, `tweet.write`, `users.read`, `offline.access`.

## n8n OAuth2 Credentials Setup (with PKCE)

1. In n8n, go to **Credentials** > **New Credential**.
2. Select **OAuth2** (or **Twitter/X** if available and updated).
3. If using the generic OAuth2 credential:
   - **Grant Type**: Authorization Code (PKCE)
   - **Authorization URL**: `https://twitter.com/i/oauth2/authorize`
   - **Access Token URL**: `https://api.twitter.com/2/oauth2/token`
   - **Client ID**: [Your Twitter Client ID]
   - **Client Secret**: [Your Twitter Client Secret]
   - **Scope**: `tweet.read tweet.write users.read offline.access`
   - **Redirect URI**: [Must match the one set in Twitter App]
   - **PKCE Code Challenge Method**: S256 (recommended)
4. Save and connect the credential to test the connection.

## Example Workflow: Post a Tweet

1. Use a **Trigger** node (e.g., Cron, Webhook).
2. Add an **HTTP Request** node (or Twitter node if available and configured) to post a tweet.
   - If using HTTP Request:
     - Method: POST
     - URL: `https://api.twitter.com/2/tweets`
     - Headers:
        - Authorization: Bearer {{$json["access_token"]}} (from OAuth2 credential)
        - Content-Type: application/json
     - Body: JSON with `{"text": "Your tweet here"}`
3. Connect the OAuth2 credential to the HTTP Request node.

## Pitfalls and Troubleshooting

- **404 on n8n Twitter Node Documentation**: If the built-in Twitter node documentation returns a 404, use the generic OAuth2 credential and HTTP Request node as described above.
- **Token Expiry**: The `offline.access` scope allows refresh tokens. Ensure your workflow handles token refresh automatically (n8n does this for OAuth2 credentials).
- **Scope Mismatch**: Double-check that the scopes in your n8n credential match those approved in the Twitter App.

## References

- See `references/twitter-oauth2-n8n.md` for detailed API notes.
- See `templates/n8n-twitter-post-tweet.json` for a workflow example.