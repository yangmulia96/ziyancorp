# Threads Re-Auth Guide (ZIYAN, verified 16/8/2026)

## Credentials (vault, NEVER chat)
- `threads_app_id` = `1346767533487099`
- `threads_app_secret` = `threads_app_secret.gpg` (rotate if exposed)
- FB App "n8n" = `19946763178947313` (NOT for Threads)

## Flow
1. `python threads_reauth.py` → prints login URL
2. Bos opens on HP, logs in @celineaurel99, authorizes
3. Copy `https://localhost:8123/?code=XXX`
4. `python threads_reauth.py "<URL>"` → exchanges → saves vault `threads_token` + `.env`
5. Validates `GET graph.threads.net/v1.0/me` → must return `celineaurel99`

## Endpoints
- Login: `https://graph.threads.net/oauth/authorize?client_id=1346767533487099&redirect_uri=https%3A//localhost%3A8123/&scope=threads_basic%2Cthreads_content_publish&response_type=code`
- Token: `POST https://graph.threads.com/oauth/access_token` (client_id, client_secret, code)
- Short→Long: `grant_type=th_exchange_token`
- Refresh: `grant_type=th_refresh_token` (replace token in vault BEFORE expiry)

## Errors encountered 16/8
| Error | Cause | Fix |
|-------|-------|-----|
| "No app ID was sent" | Used `threads.net` not `graph.threads.net` | Use `graph.threads.net` |
| "Invalid client_id: 1546767553487099" | Wrong Threads App ID (console screenshot typo) | Use `1346767533487099` (vault) |
| "Error validating client secret" | Used FB secret for Threads app | Use `threads_app_secret` |
| "Invalid verification code" | Code expired OR credential correct (test fake code) | Re-authorize fast; if fake code → credentials OK |
| "Cannot parse access token" | THREADS_USER_TOKEN empty in env | Set via threads_reauth.py |

## Manus rules (16/8)
- Do NOT mix FB/Threads credentials. Separate `threads_reauth.py` from `fb_reauth.py`.
- Threads token NOT eternal. Refresh before expiry, else re-auth.
- If secret exposed in repo → rotate + redact + purge git history.
