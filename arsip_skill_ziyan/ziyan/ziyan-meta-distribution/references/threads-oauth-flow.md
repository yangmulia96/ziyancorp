# Threads OAuth & Posting Recipe (verified 15/8/2026)

## Get token (Meta App "User Token Generator" — simplest)
1. Meta App dashboard → Use cases → Threads → Settings
2. Add Redirect Callback URL: `https://localhost:8123/`
3. Scroll to "User Token Generator" → Generate Access... for `@celineaurel99`
4. Copy the long-lived token directly. No OAuth code dance needed.

## Alternative: OAuth code exchange (if generator unavailable)
```
# Step 1: authorize URL (Bos opens in browser/HP, logs in @celineaurel99)
https://threads.net/oauth/authorize?client_id=THREADS_APP_ID&redirect_uri=https%3A%2F%2Flocalhost%3A8123%2F&scope=threads_basic%2Cthreads_content_publish&response_type=code

# Step 2: exchange code -> short-lived (server-side, within ~1 min of code)
curl -X POST https://graph.threads.com/oauth/access_token \
  -d "client_id=THREADS_APP_ID" \
  -d "client_secret=THREADS_APP_SECRET" \
  -d "redirect_uri=https://localhost:8123/" \
  -d "code=CODE_FROM_REDIRECT"

# Step 3: extend short -> long-lived (60d)
curl -X POST https://graph.threads.com/oauth/access_token \
  -d "grant_type=th_exchange_token" \
  -d "client_secret=THREADS_APP_SECRET" \
  -d "access_token=SHORT_TOKEN"
```

## Validate
```
curl "https://graph.threads.com/v1.0/me?fields=id,username&access_token=TOKEN"
# expect: {"id":"...","username":"celineaurel99"}
```

## Post text
```
curl -X POST "https://graph.threads.com/v1.0/me/threads" \
  -d "media_type=TEXT" -d "text=Hello from Celine Aurel" -d "access_token=TOKEN"
# -> {"id":"CREATION_ID"}
curl -X POST "https://graph.threads.com/v1.0/me/threads_publish" \
  -d "creation_id=CREATION_ID" -d "access_token=TOKEN"
# -> {"id":"POST_ID"}
```

## Verify live
```
curl "https://graph.threads.com/v1.0/me/threads?fields=id,text&access_token=TOKEN"
```

## Pitfalls
- Error "Invalid verification code" (subcode 36006) = code already used / expired. Regenerate.
- Error "URL Blocked ... redirect URI not whitelisted" = add `https://localhost:8123/` to
  App Settings → Redirect Callback URLs AND Save.
- Don't mix FB Graph token with Threads token — they are different.
- Threads App ID/Secret are SEPARATE from FB App ID/Secret (same Meta App, different fields).
