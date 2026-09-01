# ZIYAN Distribution Agent — Token & Endpoint Reference (verified 16/8/2026)

Each platform needs its OWN token source + API endpoint. Mixing them causes
"Cannot parse access token" (code 190) or "Insufficient Permission" (403).

## FB Page
- Token: `fb_page_token` in vault (`bash bin/token_vault.sh get fb_page_token`), also in `.env`
- Endpoint: `https://graph.facebook.com/v20.0/{page_id}/feed` (POST)
- Status: WORKS (no re-auth needed)
- Page ID: `975723622288353`

## Threads
- Token: `THREADS_USER_TOKEN` in vault (NOT META_USER_TOKEN, NOT FB_PAGE_TOKEN)
- App: Threads App ID `1346767533487099` + secret `e9cbc6f06bd2470f5d641a4dc3af03ee`
  (separate from FB app — Do NOT use FB app_id/secret for Threads)
- Endpoint: `https://graph.threads.net/v1.0/{user_id}/threads` + `/threads_publish`
- Login URL: `https://graph.threads.net/oauth/authorize?client_id=1346767533487099&redirect_uri=https%3A//localhost%3A8123/&scope=threads_basic%2Cthreads_content_publish&response_type=code`
  (do NOT use `threads.net` or `www.threads.com` — they error "no app ID")
- Token exchange: `https://graph.threads.com/oauth/access_token` (short→long via `th_exchange_token`)
- Posting: TEXT-ONLY works. Image via Drive URL fails (Meta can't fetch Drive).
- Status: WORKS

## Instagram
- Token: `INSTAGRAM_USER_TOKEN` in vault (from Instagram Login / User Token Generator)
- IG Business ID: `17841444876830769` (user `celineaurel99`)
- Endpoint: `https://graph.instagram.com/v20.0/{ig_id}/media` + `/media_publish`
  (do NOT use `graph.facebook.com` for IG Login tokens — "Cannot parse")
- Test validity: `GET graph.instagram.com/v20.0/me` (returns id+username)
- Image: must be a real image URL. Drive `view?usp=drivesdk` / `uc?export=view` = HTML, rejected
  ("image format not supported" code 36001). WORKAROUND: upload photo to FB Page
  (`POST graph.facebook.com/{page_id}/photos`, published:false) → read `.source` CDN URL → use for IG.
- Status: WORKS (after endpoint fix + FB-CDN image)

## YouTube (Celine Aurel Official)
- Token file: `token_celine.json` (channel `UC0h3xyafx6P6J_CjpzhpSeg`, @celineaurelofficial)
- Scope MUST include `https://www.googleapis.com/auth/youtube.upload`
- Failure symp: "Insufficient Permission" 403 → token scope wrong.
  Fix: delete `token_celine.json`, run
  `oauth_channel_check.py --expected-channel UC0h3xyafx6P6J_CjpzhpSeg` (Bos authorizes in browser).
- Upload: `youtube_upload_celine.py --file <mp4> --title T --description D --privacy public
  --expected-channel UC0h3xyafx6P6J_CjpzhpSeg --client client_secret.json --token token_celine.json`
- Status: WORKS

## Vault commands
- List: `bash bin/token_vault.sh list`
- Get:  `bash bin/token_vault.sh get <key>`
- Set:  `bash bin/token_vault.sh set <key> <value>`
- Del:  `bash bin/token_vault.sh del <key>`
- Passphrase: `~/.hermes/.env` VAULT_PASS (never log/commit secrets)

## Cleanup done 16/8
Deleted (expired/sampah): vault `threads_token`, vault `instagram_token`, `.env` META_USER_TOKEN.

## Token validity verification (run BEFORE claiming a platform works)
```python
import subprocess, requests
def vault(k): return subprocess.check_output(['bash','/c/Users/arija/bin/token_vault.sh','get',k]).decode().strip()
tests = {
  'fb_page_token':  ('https://graph.facebook.com/v20.0/me', {'fields':'id'}),
  'threads_user_token': ('https://graph.threads.net/v1.0/me', {'fields':'id,username'}),
  'instagram_user_token': ('https://graph.instagram.com/v20.0/me', {'fields':'id,username'}),
}
for k,(url,params) in tests.items():
    tok=vault(k)
    if not tok: print(k,'EMPTY'); continue
    r=requests.get(url, params={**params,'access_token':tok}, timeout=12)
    print(k, 'OK' if r.status_code==200 else f'ERR {r.status_code}')
```
YouTube: `Credentials.from_authorized_user_file('token_celine.json',[...upload]).valid` must be True AND scope includes youtube.upload.

## Exposed-secret response (16/8 lesson)
If a secret lands in `SHARED_MEMORY.md` / git history:
1. REDACT in the working file immediately (replace with `[REDACTED]`).
2. Commit the redaction.
3. ROTATE the actual secret (reset in Meta/Google console, update vault).
4. Note in SHARED_MEMORY that history purge is recommended (private repo = lower risk, but Manus advised it).
Do NOT keep using an exposed secret silently. The `e9cbc6...ee` Threads secret was rotated by switching to it after `99068c` was exposed.

## App-ID digit trap (16/8)
FB App "n8n" real App ID = `19946763178947313` (9 digits). A typo `1994676317847313` (one digit off) was used for OAuth and produced "client secret invalid" because the secret belonged to the correct app. Always copy App ID from the Meta Console screenshot, never retype. Threads App ID `1346767533487099` is SEPARATE from FB App ID.
