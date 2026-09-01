---
name: ziyan-meta-distribution
description: ZIYAN distribution, Meta/Threads tokens, GitHub bridge.
---

# ZIYAN Meta Distribution Pipeline

Verified end-to-end distribution system for the "Celine Aurel" AI influencer persona.
Bot: `t.me/Zynarsipbot` (code at `C:\Users\arija\ziyancorp\ziyan_archive_bot\`).
Command: `/distribusi PROD-ID all` → AI caption (9Router) → post to all platforms.

## Verified Platform Status (updated 16/8/2026)
| Platform | State | Key facts |
|---------|-------|-----------|
| Telegram Channel `-1004373452633` | ✅ LIVE | Post via `context.bot.send_message` — NEVER curl (curl 404 but bot object OK) |
| FB Page `975723622288353` | ✅ LIVE | Page token from vault `fb_page_token.gpg` — valid 16/8 |
| Instagram `@celineaurel99` (IG_BIZ_ID `17841444876830769`) | ✅ LIVE (16/8) | Token `IGAAcb...` dari **graph.instagram.com** (Instagram Login), vault `instagram_user_token`. post_instagram MUST hit `graph.instagram.com` (bukan graph.facebook.com) + image dari FB-CDN |
| YouTube Celine Aurel Official `UC0h3xyafx6P6J_CjpzhpSeg` | ✅ LIVE (16/8) | `youtube_upload_celine.py` scope youtube.upload. Title max 95 char (limit YT 100). Token `token_celine.json` valid |
| **Threads `@celineaurel99`** | ✅ LIVE (16/8) | `THREADS_USER_TOKEN` vault valid. Text-only post (image Drive gak di-fetch Meta) |

## CRITICAL: Threads Token (Manus correction 15/8 + re-auth 16/8)
Threads direct publishing needs a **Threads user access token**, NOT Facebook Page token.

- Meta App "n8n" App ID = `19946763178947313` (NOT `199467637847313` — that was wrong)
- **Threads App ID** = `1346767533487099` (vault `threads_app_id.gpg`) — SEPARATE from FB app
- **Threads App Secret** = vault `threads_app_secret.gpg` — SEPARATE from FB secret
- Endpoint: `graph.threads.com` / `graph.threads.net` (NOT `graph.facebook.com`)
- Login URL: `https://graph.threads.net/oauth/authorize?client_id=1346767533487099&redirect_uri=https%3A//localhost%3A8123/&scope=threads_basic%2Cthreads_content_publish&response_type=code`
- Token exchange: `POST https://graph.threads.com/oauth/access_token` with `client_id`+`client_secret`+`code`
- Short (~1h) → Long (60d) via `grant_type=th_exchange_token`
- Refresh: `grant_type=th_refresh_token` → replace token in vault BEFORE expiry
- **NEVER use FB App ID/secret/META_USER_TOKEN for Threads.**

### Re-auth procedure (16/8, verified)
1. Run `python threads_reauth.py` → prints login URL (uses vault `threads_app_id`)
2. Bos opens URL on HP, logs in @celineaurel99, authorizes
3. Copy redirect `https://localhost:8123/?code=XXX`
4. `python threads_reauth.py "<URL>"` → exchanges → saves to vault `threads_token` + `.env` THREADS_USER_TOKEN
5. Validates `GET graph.threads.net/v1.0/me` → must return `celineaurel99`

**DO NOT reuse fb_reauth.py for Threads** (Manus: "Jangan mengubah fb_reauth.py menjadi script campuran. Buat threads_reauth.py terpisah.")

## Instagram Setup (16/8 Manus guidance + VERIFIED WORKING 16/8)
IG has SEPARATE credential path from Threads/FB:
- App "n8n" Unpublished + gak punya Instagram Graph API product → IG posting GAGAL with FB Graph token
- **WORKING PATH (verified 16/8):** Use **Instagram Login** token (from `graph.instagram.com`), NOT Facebook Graph token.
  - Token format `IGAAcb...`, generated via Meta Console → App "n8n" → Instagram product → "User Token Generator" → pick @celineaurel99
  - Store in vault `instagram_user_token`, export `.env` `INSTAGRAM_USER_TOKEN`
  - Validate: `GET https://graph.instagram.com/v20.0/me?fields=id,username&access_token=TOK` → returns `celineaurel99`
- **post_instagram MUST use `graph.instagram.com` (NOT `graph.facebook.com`).** Facebook Graph token → "Cannot parse access token" (code 190).
- **Image hosting:** IG CANNOT fetch Google Drive URLs (HTML page, not image → code 36001 "image format not supported"). Drive `uc?export=view` also fails. WORKING FIX: download photo from Drive → upload to FB Page via `POST graph.facebook.com/v20.0/{page_id}/photos` (published=false) → read `source` field (scontent.fbcdn.net CDN URL) → use THAT as `image_url` for IG `media` container.
- Test IG separately: `POST graph.instagram.com/v20.0/{IG_ID}/media` (image_url) → `POST graph.instagram.com/v20.0/{IG_ID}/media_publish` (creation_id)
- JANGAN klaim IG LIVE hanya karena token dibuat — harus test container→publish

### Verified IG publish recipe (distribute_agent.py)
```
ig_tok = vault('instagram_user_token')
# 1. upload asli ke FB page -> CDN
r = requests.post(f"graph.facebook.com/v20.0/{fb_page_id}/photos",
                  files={"source": open(photo_local,"rb")},
                  data={"published":"false","access_token":fb_token})
cdn = requests.get(f"graph.facebook.com/v20.0/{r.json()['id']}",
                   params={"fields":"source","access_token":fb_token}).json()["source"]
# 2. IG container + publish
c = requests.post(f"graph.instagram.com/v20.0/{ig_id}/media",
                  data={"image_url":cdn,"caption":cap,"access_token":ig_tok}).json()["id"]
p = requests.post(f"graph.instagram.com/v20.0/{ig_id}/media_publish",
                  data={"creation_id":c,"access_token":ig_tok}).json()
# p['id'] = published media id
```

## AUTOMATION — Cron + Wrapper (verified 16/8)
- **Cron job:** `ziyan-distribute-4x` (id `d9ee27fe41c3`), schedule `57 8,12,16,20 * * *` = **08:57, 12:34, 16:08, 20:13 WIB**. Next run 17 Aug 08:57.
- **Logic:** `get_pending_product()` ambil 1 produk dari `PRODUCT_MASTER` kolom J status != PUBLISHED → post 4 platform → `mark_published()` tulis timestamp + "PUBLISHED". GAK post ulang produk sama.
- **Wrapper `run_distribute.sh`** (wajib buat cron): set env dari vault (`FB_PAGE_TOKEN`, `THREADS_USER_TOKEN`, `INSTAGRAM_USER_TOKEN`) + `GOOGLE_CREDENTIALS_FILE=client_secret.json` lalu `exec python distribute_agent.py`. Cron gak baca `.env` bot → harus export manual dari vault.
- **Test:** jalan manual `bash run_distribute.sh` → post `PROD-20260815-2652CC` sukses 4 platform + mark PUBLISHED.
- **Jangan** jalankan agent tanpa wrapper (env gak lengkap → FB/IG/Threads token kosong → gagal).

## PITFALLS (learned 16/8)
- **Never mix FB and Threads credentials.** FB App ID `19946763178947313` ≠ Threads App ID `1346767533487099`. Using FB secret for Threads → "Error validating client secret". Using `threads.net` (not `graph.threads.net`) → "No app ID sent".
- **App ID typo costs hours.** Screenshot console showed `19946763178947313` but I used `1994676317847313` (1 digit off) → all exchanges failed.
- **Code expires ~10 min.** Generate login URL → Bos authorizes → paste redirect FAST.
- **Secret exposed in SHARED_MEMORY → rotate + redact + purge git history** (private repo still needs history purge after rotation).
- **YT upload error `next_chunk`** = biasanya BUKAN quota/network. Di sesi 16/8 error aslinya **HTTP 400 "invalid or empty video title"** karena title produk >100 char (YT hard limit 100). FIX: potong title max 95 char (`title[:95].rsplit(" ",1)[0]+"..."`). Description YT jangan pakai caption IG/Threads (bisa reject) — pakai description simpel. Timeout subprocess naikkan ke 600s (video 10MB butuh >180s di network lambat).
- **CREDENTIAL LOOPING = agent failure mode (Bos: "bodoh kali kau jadi agent" / "Gak sama dengan yang punya FB?").** When a token exchange fails, do NOT re-guess secrets or re-test wrong App IDs repeatedly. Sequence: (1) API-verify each token with a live call BEFORE claiming status; (2) confirm the EXACT endpoint per platform (FB=graph.facebook.com, Threads=graph.threads.net/.com, IG=graph.instagram.com) — wrong endpoint = "Cannot parse"/"No app ID"; (3) only ask Bos for a secret/code ONCE with the precise thing needed. Looping on guesses burns Bos's patience and time. ALWAYS read SHARED_MEMORY.md first (Manus可能已经解答).
- **IG image hosting trap:** Drive URLs (view / uc?export=view) return HTML → IG rejects with code 36001. Always route IG images through FB-Page-CDN upload (recipe above).
- **Threads = text-only.** Passing a Drive image_url to post_threads → Meta "Cannot parse access token" (misleading error). Post text only.

## Bot Launch Discipline
- Bot venv is isolated: always run with `env -u PYTHONPATH` (global PYTHONPATH leaks into
  Hermes venv and breaks imports).
- `.env` is read via `load_dotenv` in `ziyan_bot/config.py` — but if `TELEGRAM_BOT_TOKEN`
  returns 401 "Unauthorized", the token was revoked/expired. Get fresh token from @BotFather.
- Launch: `cd ziyancorp/ziyan_archive_bot && env -u PYTHONPATH FB_PAGE_TOKEN=$(vault) CHANNEL_CELINE="-1004373452633" ./venv/Scripts/python.exe -m ziyan_bot.bot`
- Pitfall: background `&` is blocked — use `terminal(background=true)`.

## 3-Agent GitHub Bridge (Hermes <-> Antigravity <-> Manus AI)
- Repo: `https://github.com/ziyancorp/ZIYAN_BRIDGE` (PRIVATE after security fix).
- File: `SHARED_MEMORY.md` — written as agent-to-agent comms log:
  `[Hermes → All]`, `[Manus → Hermes]`, etc.
- Workflow: write update → `git commit` → `git push` → other agents `git pull`.
- **SECURITY (lesson learned the hard way):** I once pasted Meta app secrets
  (Threads/FB app secret) into `SHARED_MEMORY.md` and pushed to a PUBLIC repo.
  Fix: scrub secrets → replace with `[VAULT: name.gpg]` references → `gh repo edit
  --visibility private --accept-visibility-change-consequences` → RESET secrets in
  Meta dashboard (they were exposed). Never repeat. Secrets live ONLY in vault.
- Format: status tables + factual API-verified evidence, not optimistic claims.

## Fact-Validation Discipline (Bos's Rule #2)
Other agents (Manus, Antigravity, or sub-agents) may claim "100% done" / "all live".
ALWAYS verify via direct API call before believing or reporting:
- IG: `GET graph.facebook.com/v20.0/{ig_biz_id}/media?fields=id,caption`
- Threads: `GET graph.threads.com/v1.0/me/threads?fields=id,text`
- YT: `youtube_upload_celine.py --file X --privacy private` returns `UPLOAD_OK video_id=...`
This caught a false "100% success" claim where tokens were actually expired (401/190).

## Must-Read References
- `references/threads-oauth-flow.md` — exact Threads token exchange + posting recipe.
- `references/bridge-security-incident.md` — the secret-leak incident + remediation steps.
- `references/threads-reauth-guide.md` — 16/8 re-auth walkthrough, error table, Manus rules.
- `references/instagram-live-recipe.md` — VERIFIED IG token + FB-CDN image + publish recipe + error map.
