---
name: ziyan-token-lifecycle
description: Refresh FB/X/YT/Google tokens and fix n8n webhook for ZIYAN.
---

# ZIYAN Token Lifecycle & Publishing Automation

## When to use
- Bos asks to fix/refresh FB, X, YT, or Google tokens.
- Posting to FB/YT/X fails with auth errors (403/401/expired).
- n8n webhook won't register (v2.33 manual DB insert bug) → need a scheduler.
- Building Job Hunter or affiliate posting automation (Telegram → FB+YT+X → Sheet).

## Core techniques (proven this session)

### 1. Facebook — token lifetime (FACTUAL, verified 2026-08-15)
- **MYTH BUSTED**: dokumentasi bilang `fb_exchange_token` → 60 hari. **DI PRAKTEK TIDAK.** Sesi 15/8: token dari Graph Explorer app "n8n"/"nibs" DAN dari `fb_reauth.py` (setelah `fb_exchange_token` POST form) = **SHORT-LIVED ~6 JAM** (token jam 11:00, expired jam 17:00 same day, error 190 subcode 463 "Session has expired").
- `debug_token` tidak menampilkan `expires_at` untuk page token → jangan pakai itu sebagai bukti "long-lived".
- **REALITAS**: Meta token untuk akun pribadi Bos (Celine Aurel) = short-lived. Harus **re-auth sebelum tiap sesi pakai** (jalankan `fb_reauth.py`, Bos authorize di HP, ambil page token dari `me/accounts`).
- Flow yang WORK (verified 15/8):
  1. `python fb_reauth.py` → print login URL (app `1994676317847313`)
  2. Bos buka URL di HP → authorize → paste redirect URL (`https://localhost:8123/?code=...`) ke agent
  3. Script exchange code → user token → `me/accounts` → **PAGE token** (`975723622288353`)
  4. Simpan: `bash bin/token_vault.sh set fb_page_token "$PTOK"` + `set fb_user_token "$UTOK"`
  5. VALIDATE segera: `curl .../975723622288353?fields=id,name&access_token=$PTOK` → harus return `{"id":"975723622288353"}`
- App ID/Secret: `OneDrive/ziyan_pending/fb_app_id.txt` + `fb_app_secret.txt`.
- Posting requires **PAGE** token (user token → 403). FB page target: `Celine Aurel` (`975723622288353`).
- **JANGAN asumsi token "60 hari"**: selalu validate sebelum pakai, re-auth kalau 190.

### 2. X/Twitter — OAuth1a NOT Bearer
- Free tier: Bearer (App-only) → **403 Forbidden** on `POST /2/tweets`.
- Use **OAuth 1.0a User Context**: CONSUMER_KEY/SECRET + ACCESS_TOKEN/SECRET from `~/.x_credentials`.
- Post: `OAuth1Session(...).post("https://api.twitter.com/2/tweets", json={"text":...})` → 201 = success.
- Media: upload via `upload.twitter.com/1.1/media/upload.json` first → reference `media_ids` in the tweet.
- Credentials: `~/.x_credentials` (the `.bak` holds real values; copy to active).

### 2a. X API 403/401 ROOT CAUSE — client-not-enrolled
- Error 403 client-not-enrolled / must use keys from app attached to a Project = app NOT connected to a Project.
- Fix: console.x.com → klik app → card Project Access (kuning, Not connected) → klik Manage → pilih Default project → Connect. Status jadi hijau Connected, API v2 jalan.
- Jika 401 Unauthorized → tab Keys & Tokens → Revoke + Regenerate Bearer Token & Access Token (OAuth1a).
- Username di cred (TWITTER_USERNAME) harus sama dengan akun posting. Kalau Bos ganti akun (AgenticsID → celineaurel99), regenerate token untuk akun baru.

### 2a-XTRA — TOKEN DARI APP YANG DIHAPUS = MATI SELAMANYA
- **JANGAN hapus app X di console kalau masih butuh tokennya.** Menghapus app membuat SELURUH token (Consumer/Access/Bearer/OAuth2) dari app itu INVALID → 401/403 permanen.
- Gejala sesi 08-09: Bos hapus app `shopeeaffiliatee` + `2082093644111073280AgenticsID` → semua token di `.x_credentials` mati, test OAuth1a/Bearer gagal terus. Regenerate di app lain TIDAK menolong karena Consumer Key beda app.
- **HANYA JALAN jika Bos buat app BARU** di console.x.com (+ Create App), connect ke Project, lalu regenerate 4 token (Consumer Key/Secret + Access Token/Secret) dari app baru itu.
- Urutan wajib: (1) Create App → (2) permission Read+Write+DM, type Web App/Bot, callback `http://127.0.0.1:3000` → (3) Manage → connect Default project → (4) BARU regenerate Access Token (harus SETELAH connect) → (5) kirim 4 token ke agent.
- OAuth2 tokens (Client ID / Access Token / Refresh Token dari tab OAuth 2.0 Keys) juga mati kalau app dihapus — perlakukan sama.
- Simpan token ke `~/.x_credentials` (format `KEY=value` per baris, BUKAN JSON). Jangan print literal ke chat; redact di summary.
- Detail + recovery step-by-step: `references/x-app-deleted-tokens.md`

### 2c. STYLE BOS — JANGAN NEBEK LOKASI TOMBOL DI CONSOLE/WEB  [TERBUKTI 2026-08-09]
- Bos marah "salah terus arahan mu" karena saya nebak lokasi tombol Delete App di X Developer Console (bilang "scroll di Authentication settings" padahal tombol ada di tab Settings).
- FIX: kalau Bos suruh cari/menuju tombol di UI web/console → **RISK dulu via web-search** (cari dokumentasi resmi X/n8n) atau **minta Bos screenshot** langkah aktual. JANGAN nebak urutan klik.
- Bos mau respons **SINGKAT & PADAT** — jangan jelaskan panjang lebar. Format: fakta + action + hasil.

### 2d. X API: APP YANG MASIH HIDUP vs DIHAPUS  [TERBUKTI 2026-08-09]
- Sesi 08-09: Bos hapus app `shopeeaffiliatee` + `2082093644111073280AgenticsID` → token dari app itu MATI (401/403).
- TAPI app **`shopeeaffiliate`** (tanpa 'e' di akhir) MASIH HIDUP → token dari app ini yang akhirnya jalan (test 200, akun celineaurel99).
- Lesson: jangan asumsi "app dihapus" kalau Bos bilang "connect sudah ok". Cek screenshot mana app yang status "Connected" (hijau). App berbeda = Consumer Key beda = token gak cocok walau format sama.
- Saat Bos kirim token, PASTIKAN Consumer Key di `.x_credentials` cocok dengan app yang sedang Connected di console.
- Tombol Delete App TIDAK ADA di tab Keys & Tokens atau sub-page Authentication settings.
- Lokasi BENAR: buka app → tab Settings (icon gear, sebelah Keys & Tokens) → SCROLL KE PALING BAWAH → tombol merah Delete App → ketik nama app persis → konfirmasi.
- Apps list (sidebar kiri → Apps) tidak menampilkan tombol delete langsung; harus masuk detail app dulu.
- JANGAN hapus app produksi (misal shopeeaffiliatee). App sampah numerik boleh dihapus kalau Bos yakin.
- Detail navigasi console: `references/x-console-nav.md`

### 3. YouTube — refresh_token
- Token in `AppData/Local/hermes/ziyan_youtube_token.json` (account Celine Aurel).
- If `access_token` expired: POST `https://oauth2.googleapis.com/token` with `client_id/secret/refresh_token/grant_type=refresh_token`, write new `access_token` back.
- Upload Shorts: multipart `metadata=<file;type=application/json` + `file=@video;type=video/mp4` to `youtube/v3/videos?part=snippet,status&uploadType=multipart`. Set `status.privacyStatus: public`.

### 4. Google Sheets — curl bypass (broken lib)
- `google-api` Python lib may fail on this Windows venv (`_cffi_backend` missing). Use **curl to Sheets API v4** directly.
- Client secret in `AppData/Local/hermes/google_client_secret.json` (key `installed`). Same Google project = `ZiyanCorp`.
- Refresh: same oauth2 endpoint as YT.
- Append row:
  `POST https://sheets.googleapis.com/v4/spreadsheets/{ID}/values/{TAB}!A:I:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS`
  with `-H "Authorization: Bearer {token}" --data-binary @{row.json}`.

### 5. n8n webhook broken → Python scheduler
- n8n v2.33: manual DB insert of a workflow does NOT register its webhook → "Cannot POST /webhook".
- Replace with a Python scheduler: `queue.json` (pending items) + `loop()` that posts 1 item every N minutes to FB+YT+X, then writes an arsip row.
- Working example: `C:\Users\arija\ziyan_intake\scheduler.py` (batch every 77 min; arsip to CSV + Google Sheet tab `Arsip`).

### 6. Vault decrypt (.gpg tokens) — PASSPHRASE IN ~/.hermes/.env
- Encrypted tokens live in `.hermes/vault/*.gpg` (fb_page_token.gpg, fb_user_token.gpg, threads_token.gpg).
- Decrypt WITHOUT manual passphrase prompt via the helper:
  `bash bin/token_vault.sh get <name>`  (e.g. `bash bin/token_vault.sh get threads_token`)
- Passphrase sourced automatically from `~/.hermes/.env` (`VAULT_PASS=...`). Script: `bin/token_vault.sh` (set/get/del/list, AES256 GPG symmetric).
- Raw `gpg --decrypt file.gpg` without `-passphrase` will hang 25s waiting for stdin — ALWAYS use the vault script or pass `--batch --yes --passphrase "$VAULT_PASS"`.
- After decrypt, VALIDATE before use: a decrypted token may be EXPIRED (error 190). Sesi 2026-08-15: threads_token + fb_page_token + fb_user_token all decrypted OK but returned "Session has expired" on API call. Expiry date in error = 10-Jul-26, current = 14-Aug-26.
- To re-auth expired Meta tokens: app ID/secret in `OneDrive/ziyan_pending/fb_app_id.txt` + `fb_app_secret.txt`; see Section 1 for exchange flow.

> PITFALL: don't waste turns hunting for "lost" IG/YouTube tokens. Sesi 2026-08-15 deep search (disk + GitHub yangmulia96 + Antigravity logs + Hermes history) found: YouTube Celine Aurel token VALID (`ziyancorp/youtube_token_celineaurel.json`); IG token NEVER existed plain-text; Threads only in expired `.gpg`. Conclusion: re-auth, don't search.

### 7. Threads — OWN token, NOT Facebook (KOREKSI MANUS AI, 15/8/2026)
**MYTH BUSTED by Manus:** Threads publishing does NOT use Facebook Page token. It needs a **Threads user access token** obtained from the **Threads Authorization Window** using **Threads App ID/Secret** (separate from FB App ID). Endpoint `GET /{page-id}/threads_business_account` is for Business Suite cross-posting, NOT direct API publishing.

- Threads App credentials (tersimpan vault, dari screenshot dashboard Meta app "n8n" 20:40 15/8):
  - `threads_app_id = 1346767533487099`
  - `threads_app_secret = bbdc0cb1895636`
  - FB App (reuse): `fb_app_id = 1994676378747313`, `fb_app_secret = 18bd7af50624616`
- **Token lifetime**: short-lived ~**1 jam** → tukar ke long-lived ~**60 hari** via `grant_type=th_exchange_token` (Threads secret, server-side ONLY via `graph.threads.com`, NEVER browser/repo/log/Telegram).
- **PREREQ WAJIB (pelajaran 15/8: Bos error "URL Blocked" 3×):** SEBELUM generate auth URL, **whitelist redirect URI di Meta App Dashboard DULU**:
  - App Dashboard → Settings → Basic → **"Valid OAuth Redirect URIs"** → Add `https://localhost:8123/` (persis, https + trailing slash).
  - Pastikan **Client OAuth Login = ON** & **Web OAuth Login = ON** (sidebar → Facebook Login → Settings).
  - Kalau dilewatkan → error: `{"error_message":"URL Blocked: This redirect failed because the redirect URI is not whitelisted..."}`. App token (appid|appsecret) GAK bisa set redirect via API → Bos harus klik manual di dashboard.
- **JANGAN pakai ID lama dari disk** — kalau Bos kirim screenshot Meta dashboard, AMBIL App ID/secret dari screenshot itu LANGSUNG (15/8: saya mutar cari `yangmulia96` padahal Bos sudah screenshot `ziyancorp`/`1994676378747313` → Bos marah "Pantek lah.. lama kali"). Pakai nilai screenshot sebagai sumber kebenaran.
- **Flow (verified design, belum live-test 15/8 karena Bos belum authorize):**
  1. Bos buka URL authorize → `https://threads.net/oauth/authorize?client_id={threads_app_id}&redirect_uri=https%3A%2F%2Flocalhost%3A8123%2F&scope=threads_basic%2Cthreads_content_publish&response_type=code`
  2. Bos authorize login `@celineaurel99` → copy URL redirect `https://localhost:8123/?code=...`
  3. Tukar code → short-lived: `POST https://graph.threads.com/oauth/access_token` (form: client_id, client_secret=Threads secret, code, redirect_uri, grant_type=authorization_code)
  4. Tukar → long-lived: `POST https://graph.threads.com/oauth/access_token` grant_type=`th_exchange_token`, client_secret=Threads secret
  5. **VALIDATE GATE**: `GET https://graph.threads.com/v1.0/me?fields=id,username` → username HARUS `celineaurel99` sebelum `post_threads()` lanjut.
  6. Text post: `POST /{threads-user-id}/threads` (media_type=TEXT, text) → dapat `creation_id` → `POST /{threads-user-id}/threads_publish` (creation_id). Image/video: media URL harus publik (bukan path lokal `C:\...`).
  7. Simpan: Threads user ID, token terenkripsi, `expires_at`, `last_refresh_at`. Refresh via `/refresh_access_token` sebelum expiry. Token expired TIDAK bisa ditukar → butuh authorize ulang.
- **JANGAN** campur FB Graph token dengan Threads user token. `META_USER_TOKEN` (FB) error 190 di `graph.threads.com` = token salah jenis.
- Referensi resmi: developers.facebook.com/documentation/threads (get-started, get-access-tokens, long-lived-tokens, publishing, create-posts).
- Detail + endpoint exact: `references/threads-token.md`

## Pitfalls
- FB: never trust `/me/accounts` token as long-lived without the explicit exchange call.
- FB: **Meta token untuk akun Celine Aurel = SHORT-LIVED ~6 JAM** (verified 15/8), BUKAN 60 hari. Selalu re-auth via `fb_reauth.py` sebelum pakai, validate dengan curl `me/accounts` atau `975723622288353?fields=id`.
- X: Bearer ≠ OAuth1a; free tier needs OAuth1a for writes.
- X: tokens die permanently when their app is deleted — create a new app, don't try to revive old tokens.
- Sheets: google-api lib unreliable here → use curl.
- Never print literal tokens in chat; save to OneDrive/AppData, redact in summaries.
- **SHARED MEMORY / GITHUB BRIDGE = JANGAN TULIS RAW SECRET.** Sesi 15/8: saya tulis `threads_app_secret` + `fb_app_secret` mentah ke `SHARED_MEMORY.md` lalu `git push` ke repo **PUBLIC** (`ziyancorp/ZIYAN_BRIDGE`) → bocor. FIX: di file shared memory/GitHub TULIS `[VAULT: <key>.gpg]` (reference), nilai asli HANYA di vault lokal (`bin/token_vault.sh set`). Setelah push, `gh repo edit <repo> --visibility private --accept-visibility-change-consequences`. Kalau secret sudah ke-push public → ROTATE di dashboard Meta (Reset secret) + ganti di vault. Agent lain (Manus/Antigravity) baca STATUS + LOKASI vault, bukan nilai secret.
- Verify every posting op by reading the API response (post ID), don't assume success.

## References
- `references/fb-60day-exchange.md` — exact curl sequence + verification.
- `references/fb-short-lived-reauth.md` — FACTUAL: Meta token Celine Aurel SHORT-LIVED ~6 jam (bukan 60 hari), flow fb_reauth.py verified.
- `references/x-oauth1a.md` — post_tweet.py OAuth1a pattern.
- `references/google-sheets-curl.md` — append-row recipe + token refresh.
- `references/n8n-webhook-bypass.md` — scheduler.py structure & batch loop.
- `references/x-app-deleted-tokens.md` — deleting an app kills all tokens; new-app recovery steps.
- `references/x-console-nav.md` — X Developer Console button locations (verified, not guessed).
- `references/vault-decrypt.md` — decrypt `.gpg` tokens via `bin/token_vault.sh` + validation.
- `references/threads-token.md` — Threads OAuth flow (Threads App ID/secret, exchange, long-lived, publish endpoint, validate gate).
- `references/threads-oauth-redirect-leak.md` — "URL Blocked" fix (whitelist redirect URI first) + GitHub secret-leak remediation recipe.