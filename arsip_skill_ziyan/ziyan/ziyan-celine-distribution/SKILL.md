---
name: ziyan-celine-distribution
description: Celine Aurel multi-platform distribution bot and scheduler.
---

# ZIYAN Celine Aurel Distribution

## Scope
Bot `@Zynarsipbot` → arsip file ke Drive+Sheet → auto-post ke 5 platform dengan prime-time scheduler. Code: `C:\Users\arija\ziyancorp\ziyan_archive_bot\`

## 5 Platforms (all LIVE, verified 15/8)
| Platform | Credential | Endpoint |
|---------|-----------|----------|
| Telegram Channel `-1004373452633` | `TELEGRAM_BOT_TOKEN` (bot object, NOT curl) | sendMessage |
| FB Page `975723622288353` | `fb_page_token.gpg` vault | graph.facebook.com |
| Instagram `@celineaurel99` (IG_BIZ_ID `17841444876830769`) | `META_USER_TOKEN` / fb_page_token | graph.facebook.com |
| YouTube `UC0h3xyafx6P6J_CjpzhpSeg` | `token_celine.json` (oauth_channel_check.py preflight) | youtube_upload_celine.py |
| Threads `@celineaurel99` | `threads_user_token.gpg` vault | **graph.threads.com** |

## CRITICAL: Threads needs its OWN user token
- Threads API uses **Threads user access token**, NOT Facebook Page token. Mismatch = error 190.
- Get via Meta App "n8n" → Use cases → Threads → **User Token Generator** → @celineaurel99 (long-lived).
- Endpoints: `graph.threads.com/v1.0/me/threads` + `/threads_publish`. FB `/threads_business_account` field does NOT exist unless linked via Business Suite.
- Validation gate: `GET graph.threads.com/v1.0/me` → username must be `celineaurel99` before posting.

## Meta token lifetime lesson (burned us this session)
- FB Page/User tokens from Graph Explorer = **SHORT-LIVED (~6h)**, not 60 days.
- Threads user token ≈ 60 days (long-lived), refresh via `/refresh_access_token`.
- Always re-auth via `fb_reauth.py` before use; store in vault, never .env plaintext on GitHub.

## CURRENT KNOWN-GOOD BASELINE = "15 Agustus setup" (Bos reverted to this 16/8)
After I added a channel handler + retry logic + prime-time scheduler on 16/8, Bos said "kembalikan setup bot itu seperti tanggal 15 Agustus" because the additions made it ribet and broke the flow he already trusted. The reverted baseline is:
- `on_media`: caption taken from `if message.caption and session.mode == "new":` (no `and session.draft is None`).
- `finalize_batch`: if no draft → **immediately return** with "kirim metadata lalu /simpan" (no reschedule/retry).
- Handlers: **PM-only** (`filters.PHOTO | VIDEO | DOCUMENT | CAPTION` + `TEXT & ~COMMAND`). NO channel handler.
- **NO prime-time scheduler.** Distribution is manual: Bos runs `/distribusi PROD-ID all`.
- No `retry` field on `UploadSession`.

⚠️ **PITFALL — "revert to known-good" means STRIP added features, not layer on top.**
When Bos says "kembalikan seperti [date]", delete the features I added since then (channel handler, retry, scheduler, extra fields) until the code matches the trusted state. Do NOT keep them "just in case" — that's what made it ribet. After reverting, restart and confirm the bot polls + archives a test product as it did before.

⚠️ **PITFALL — never claim a capability is supported without checking the code.**
I told Bos "bot bisa baca channel" based on a dashboard assumption, but `reject_if_unauthorized` only permitted channel type while NO `filters.ChatType.CHANNEL` handler existed — so channel messages were silently dropped. Bos: "kemarin kau bilang bisa malah kau suruh buat channel.. ribet kali kau buat." Rule: before asserting "X works / bot supports Y", grep the handler list + the relevant function. If the handler/filter isn't there, say "belum didukung, mau saya tambah?" — don't assert.

## Anti-bot prime-time scheduler (REVISI 16/8 — FINAL)
Bos merevisi jadwal + mekanisme:
- **4 jam FIX**: `08:57, 12:34, 16:08, 20:13` WIB (bukan 8/77 menit, bukan 13:03/16:24/20:29)
- **1 konten diupload SEKALIGUS ke SEMUA platform** di jam tersebut (bukan stagger)
- Platform: **YT, FB, IG, Threads** (TG Channel DIKELUARKAN per revisi 16/8)
- Scheduler: `application.job_queue.run_daily()` di `bot.py main()` atau cron terpisah

## Caption format (FIX 16/8 — TANPA HARGA)
```
<Link Shopee>

<Deskripsi natural: tema produk, ukuran, kegunaan — TANPA HARGA>

<Link Affiliate selain Shopee — kalau ada>
<4 hashtag>
```
- ❌ JANGAN sebut harga (revisi dari SOP lama yang ada harga)
- ✅ Link Shopee baris PALING ATAS
- ✅ 4 hashtag PERSIS (bukan 5)
- Sumber: `AFFILIATE.json` di folder Drive (baca `other` links) atau Sheet kolom F
- Generate via 9Router (`kr/claude-sonnet-4.5`), system instruction: "JANGAN sebut harga, 4 hashtag"

## Distribution Agent (16/8)
File: `distribute_agent.py` (di repo, GitHub `ziyancorp/ziyancorp`)
- Baca produk TERBARU (baris terakhir Sheet, bukan pertama)
- Baca `AFFILIATE.json` dari Drive → download aset ASLI (foto/video)
- `build_caption()` → format Bos (tanpa harga, 4 hashtag)
- Post YT/FB/IG/Threads PUBLIK
- Mark PUBLISHED kolom I/J
- FB jalan (vault token), Threads/IG expired (re-auth via `threads_reauth.py`), YT error `next_chunk` (debug separately)

## Bot lifecycle (restart discipline)
- **ONLY ONE instance may poll** a bot token. Starting a 2nd instance → `telegram.error.Conflict: terminated by other getUpdates request`. Always kill old instance first:
  `powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'\" | ForEach-Object { taskkill /PID $_.ProcessId /F }"`
- `.env` `TELEGRAM_BOT_TOKEN` loads via `dotenv` in `config.py`, BUT if the value is stale/invalid the server returns `InvalidToken 8173479633:***`. When restarting after a token change, the new token must be in `.env` (not just env var). Test before restart: `curl -s https://api.telegram.org/bot<TOKEN>/getMe`.
- Launch background via `terminal(background=true)` with all env vars exported (`TELEGRAM_BOT_TOKEN`, `FB_PAGE_TOKEN` from vault, `CHANNEL_CELINE`, `GOOGLE_CREDENTIALS_FILE`, `HERMES_CUSTOM_9ROUTER_API_KEY`), `env -u PYTHONPATH` to avoid venv collision.

## Sheet structure
- Tab `PRODUCT_MASTER!A2:K`. Col J (index 9) = status (PENDING/PUBLISHED). Col I = publish timestamp. `get_pending_products()` filters PENDING.

## Verification discipline (Bos rule #2)
- Another agent claimed "100% selesai" — was false (Threads token invalid). Always `curl`/`python` test API before reporting success.
- TG Channel posts via `context.bot.send_message` (curl → 404, but bot object works).

## Pitfalls
- Don't trust `curl 404` on TG sendMessage — use bot object.
- **FB App ID typo costs hours**: Screenshot console showed `19946763178947313` but I used `1994676317847313` (1 digit off) → all token exchanges failed. Always copy App ID exactly, verify via `grep` not eyeball.
- **Threads ≠ FB credentials**: Threads App ID `1346767533487099` (vault `threads_app_id`), NOT FB App `19946763178947313`. Mixing → "Error validating client secret". Use `threads_reauth.py` (separate from `fb_reauth.py`).
- Threads redirect URI must be whitelisted in Meta App or "URL Blocked" error.
- IG App "n8n" Unpublished + no IG product → IG posting DOWN until product added or separate Business app.
- YT upload `next_chunk` error = quota/network, not auth (refresh token present).
