# Threads Token — Direct API Publishing (condensed)

Source: Meta official Threads docs + Manus AI correction (15/8/2026). Hermes previously
MIXED Facebook Page token with Threads — that is wrong. Threads needs its OWN user token.

## Credentials (vault: threads_app_id / threads_app_secret)
- Threads App ID: `1346767533487099`
- Threads App Secret: `bbdc0cb1895636`
- FB App (reuse for dashboard): `fb_app_id=1994676378747313`, `fb_app_secret=18bd7af50624616`
- Target Threads account: `@celineaurel99`

## Authorize URL (Bos opens, logs in @celineaurel99, copies redirect)
```
https://threads.net/oauth/authorize?client_id=1346767533487099&redirect_uri=https%3A%2F%2Flocalhost%3A8123%2F&scope=threads_basic%2Cthreads_content_publish&response_type=code
```

## Step-by-step (server-side only, secret never to browser/repo/log/Telegram)
1. Exchange code → short-lived (1h):
   POST https://graph.threads.com/oauth/access_token
   form: client_id, client_secret=ThreadsSecret, code, redirect_uri, grant_type=authorization_code
2. Exchange → long-lived (~60d):
   POST https://graph.threads.com/oauth/access_token
   grant_type=th_exchange_token, client_secret=ThreadsSecret, access_token=<short>
3. VALIDATE GATE (mandatory before posting):
   GET https://graph.threads.com/v1.0/me?fields=id,username
   → username MUST be `celineaurel99`. If not, stop.
4. Save: threads_user_id, token (encrypted vault), expires_at, last_refresh_at.
5. Post text:
   POST /{threads-user-id}/threads  body: media_type=TEXT, text=...
   → {id: creation_id}
   POST /{threads-user-id}/threads_publish  body: creation_id=...
6. Post image/video: media URL must be PUBLIC (not C:\... local path).

## Refresh
GET https://graph.threads.com/refresh_access_token?grant_type=th_refresh_token&client_secret=...&access_token=...
Do BEFORE expiry. Expired token CANNOT be exchanged — needs manual re-auth.

## Gotchas
- FB Graph token (META_USER_TOKEN) at graph.threads.com → error 190 "cannot parse". Wrong token type.
- /{page-id}/threads_business_account field on graph.facebook.com = Business Suite cross-post, NOT needed for direct API.
- Linking Threads to FB Page in the app is NOT the blocker for direct publishing.
- App secret server-side only.
