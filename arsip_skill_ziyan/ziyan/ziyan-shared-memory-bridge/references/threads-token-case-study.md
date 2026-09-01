# Threads API — Token Case Study (Celine Aurel, 15/8/2026)

## Symptom
`post_threads()` existed in `distributor.py` but always failed:
- `META_USER_TOKEN` (FB Graph token) → error 190 "cannot parse"
- `me/threads` via FB Page token → `{"data":[]}`
- `threads_business_account` field on Page → error 2500 "Unknown path components"

Another agent claimed "100% done / Threads terpasang" — FALSE until verified.

## Root cause (explained by Manus AI)
Threads direct publishing does NOT need a Facebook Page link. It needs a **Threads user access token**, obtained from the **Threads Authorization Window** using **Threads App ID/Secret** (not FB App ID/Secret).

## Correct token flow
1. Meta App must have **Threads use case** added (dashboard → Add Product → Threads).
2. Get **Threads App ID + App Secret** from App Settings → Threads Integration section.
3. Bos authorizes 1x: `https://threads.net/oauth/authorize?client_id=<THREADS_APP_ID>&redirect_uri=https://localhost:8123/&scope=threads_basic,threads_content_publish&response_type=code`
4. Exchange code → short-lived token:
   `POST https://graph.threads.com/oauth/access_token` (client_id, client_secret, redirect_uri, code)
5. Extend to long-lived (~60 days):
   `POST https://graph.threads.com/oauth/access_token` with `grant_type=th_exchange_token`, `client_secret`, `access_token`
6. Validate: `GET https://graph.threads.com/v1.0/me?fields=id,username` → must return `celineaurel99`.
7. Post TEXT: `POST /{threads-user-id}/threads` (media_type=TEXT, text) → `creation_id`; then `POST /{threads-user-id}/threads_publish` with `creation_id`.

## Shortcut that actually worked
Meta App "n8n" had a **User Token Generator** section (Use cases → Customize → Settings → User Token Generator). Bos clicked **"Generate Access..."** next to the @celineaurel99 tester row → got a long-lived token directly. No OAuth redirect dance needed.

## Token lifetimes (Meta)
- Threads short-lived: ~1 hour. Long-lived: ~60 days. Refresh via `/refresh_access_token`.
- FB Page/User Graph token (Graph Explorer): ~6 hours (SHORT-LIVED, not 60 days as often assumed).
- DO NOT mix FB Graph tokens with Threads user tokens.

## Pitfalls
- Redirect URI must be whitelisted in App OAuth settings or you get "URL Blocked" (error 1349168).
- "Form can't be saved" on Threads settings = usually a field rejected (e.g. display name, or redirect URI format). The User Token Generator button still works without saving the form.
- Expired Threads tokens CANNOT be refreshed — require manual re-auth.
