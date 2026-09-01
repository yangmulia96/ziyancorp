# Threads OAuth — Redirect URI & Secret-Leak Remediation (15/8/2026)

## A. "URL Blocked" error (redirect URI not whitelisted)
Error seen on `threads.net/oauth/authorize` after Bos authorize:
```
{"error_message": "URL Blocked: This redirect failed because the redirect URI is not whitelisted in the app's OAuth settings. Make sure Client and Web OAuth Login are on and add all your app domains as Valid OAuth Redirect URIs.", "error_code": 1349168}
```
Root cause: redirect URI `https://localhost:8123/` was NOT added to Meta App Dashboard before generating the auth URL.
Fix (Bos manual, API cannot set this):
1. developers.facebook.com/apps/{APP_ID}/settings/basic/
2. "Valid OAuth Redirect URIs" -> Add `https://localhost:8123/` (exact: https + trailing slash)
3. Sidebar -> Facebook Login -> Settings -> Client OAuth Login = ON, Web OAuth Login = ON
4. Save Changes, THEN generate a fresh auth URL + Bos re-authorizes.

Also: Threads `code` is single-use + very short TTL. After Bos pastes the redirect URL, exchange IMMEDIATELY (within ~1 min). Reused/expired code -> `{"error":{"message":"Invalid verification code","code":1,"error_subcode":36006}}`.

## B. Secret leak to public GitHub bridge (INCIDENT + REMEDIATION)
What happened: raw `threads_app_secret`, `fb_app_secret`, App IDs written into `ZIYAN_BRIDGE/SHARED_MEMORY.md` then `git push` to PUBLIC repo `ziyancorp/ZIYAN_BRIDGE`. Detected via `grep -c <secret> SHARED_MEMORY.md`.

Remediation recipe (run in order):
1. Scrub file: replace every secret with `[VAULT: <key>.gpg]` reference.
2. Verify clean: `grep -c "rawsecret123" SHARED_MEMORY.md` -> must be 0.
3. Commit + push the scrubbed version.
4. Make repo private: `gh repo edit ziyancorp/ZIYAN_BRIDGE --visibility private --accept-visibility-change-consequences`
5. ROTATE exposed secrets at source (Meta Dashboard -> App Settings -> Basic -> Reset next to App secret / Threads app secret). Old values are burned.
6. Store NEW secrets ONLY in vault: `bash bin/token_vault.sh set fb_app_secret "..."` / `set threads_app_secret "..."`.
7. Agent other than Hermes (Manus) reads STATUS + vault location from bridge, never the secret value.

Rule going forward: shared-memory / GitHub files = vault *references* only. Never raw credentials.
