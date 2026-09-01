---
name: ziyan-social-publisher
description: "ZIYAN FB Page + YT Shorts affiliate posting pipeline."
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
platforms: [windows]
---

# ZIYAN Social Publisher — FB Page + YouTube Shorts

Alur utama ZIYAN affiliate/influencer: **Bos kirim file+teks di Telegram → Orion (Hermes) simpan, generate caption, post ke FB Page + YT Shorts + X/Twitter**. X **AKTIF** sejak 2026-08-08 (OAuth1a free, lihat section X/Twitter).

## Arsitektur (verified 2026-08-08)
- **Bukan n8n.** Workflow n8n kita bermasalah di v2.33 (manual SQLite insert TIDAK mendaftarkan webhook → 404 "Cannot POST"). Pengganti: **`C:\Users\arija\ziyan_intake\scheduler.py`** (loop 77 menit, baca `queue.json`). Lihat `references/why_not_n8n.md`.
- Orion menerima file/teks di chat Telegram (Hermes DM), lalu:
  1. Simpan file ke `ziyan_intake/files/`
  2. Generate caption via 9router (`openrouter/auto`) — lihat "Caption Spec" bawah
  3. `enqueue()` ke `ziyan_intake/queue.json`
  4. `scheduler.py` loop mem-post 1 item / 77 menit ke FB (+YT kalau video)

## Caption Spec (ATURAN BOS — jangan ubah format)
- **Ada `link_aff`** → mode JUALAN:
  ```
  [LINK AFFILIATE di BARIS 1]
  [Caption dari deskripsi produk, 1-2 kalimat, casual+persuasive, Bahasa Indonesia]
  #[3-5 hashtag relevan platform]
  ```
- **Gak ada link** → mode CASUAL (persona influencer harian, tanpa jualan).
- AI prompt template (9router `openrouter/auto`):
  - Jualan: "Kamu AI copywriter affiliate ZIYAN. FORMAT WAJIB: BARIS1: {link} | BARIS2: caption dari {deskripsi} | BARIS3: 3-5 hashtag platform {platform}. Maks 2 kalimat, casual tapi persuasive, Bahasa Indonesia."
  - Casual: "Kamu AI influencer ZIYAN. Caption CASUAL 1-2 kalimat ala posting harian (tanpa jualan) + 3 hashtag platform {platform}."
- Verified output (test crop top Shopee): link di atas + "Crop top HUT RI ini adem dipakai harian..." + `#cropop #hutri #bajumerahputih` ✅

## FB Token Storage — VAULT GPG (WAJIB, updated 2026-08-15)
- **Token TIDAK lagi di plaintext.** Sekarang di `.hermes/vault/*.gpg` (AES256, passphrase di `~/.hermes/.env` → `VAULT_PASS`).
- **DEKRIPSI (jangan `gpg --decrypt` langsung — timeout, minta passphrase interactive):**
  ```bash
  cd /c/Users/arija
  PAGE_TOK=$(bash bin/token_vault.sh get fb_page_token 2>/dev/null | tr -d '\n')
  USER_TOK=$(bash bin/token_vault.sh get fb_user_token 2>/dev/null | tr -d '\n')
  ```
- **SIMPAN token baru:**
  ```bash
  bash bin/token_vault.sh set fb_page_token "$PAGE_TOK"
  bash bin/token_vault.sh set fb_user_token "$USER_TOK"
  ```
- **PITFALL:** `OneDrive/ziyan_pending/fb_page_token.txt` sudah **EXPIRED** (10-Jul-26). Jangan pakai. Cek `references/token_vault.md` untuk recipe lengkap + cara Bos kasih token `EAA...` (user token) → re-auth via `fb_reauth.py` (token SHORT-LIVED ~6 jam, BUKAN 60 hari — re-auth tiap sesi).
- **PITFALL:** `gpg --decrypt file.gpg` TANPA passphrase = hang 25s (interactive prompt gak muncul di non-tty). Selalu lewat `token_vault.sh`.

## FB Page Publishing (Graph API v19.0)
- **Page tujuan: Celine Aurel** (`975723622288353`).
- Token: ambil dari vault (lihat section VAULT GPG di atas) = **PAGE access token** (SHORT-LIVED ~6 jam untuk akun ini — re-auth via `fb_reauth.py` tiap sesi, validate sebelum pakai).
- **Video:** `POST https://graph.facebook.com/v19.0/975723622288353/videos` dengan `-F source=@file;type=video/mp4 -F description={caption} -F access_token={PTOK}`.
- **Photo/Text:** `POST .../975723622288353/feed` dengan `-F message={caption} -F access_token={PTOK}`.
- **Hapus post:** `DELETE https://graph.facebook.com/v19.0/{post_id}?access_token={PTOK}` → `{"success":true}`.
- Daftar post: `GET .../975723622288353/posts?fields=id,message,created_time&limit=50`.

## FB Token — Re-auth (RECIPE, verified 2026-08-15)
- **MYTH BUSTED**: dokumentasi bilang `fb_exchange_token` → 60 hari. **DI PRAKTEK TIDAK** untuk akun Celine Aurel. Sesi 15/8: token dari `fb_reauth.py` = **SHORT-LIVED ~6 JAM** (jam 11 expired jam 17 same day, error 190 subcode 463).
- **REALITA**: Meta token Bos = short-lived. **Re-auth via `fb_reauth.py` SEBELUM TIAP SESI PAKAI.**
- Flow work (verified 15/8):
```bash
cd /c/Users/arija/ziyancorp/ziyan_archive_bot
# 1. print login URL
env -u PYTHONPATH ./venv/Scripts/python.exe fb_reauth.py
# 2. Bos buka URL di HP -> authorize -> paste redirect URL ke agent
env -u PYTHONPATH ./venv/Scripts/python.exe fb_reauth.py "https://localhost:8123/?code=XXXX"
# 3. script -> user token -> me/accounts -> PAGE token 975723622288353
# 4. simpan ke vault
bash bin/token_vault.sh set fb_page_token "$PTOK"
bash bin/token_vault.sh set fb_user_token "$UTOK"
# 5. VALIDATE
curl -s "https://graph.facebook.com/v20.0/975723622288353?fields=id,name&access_token=$PTOK"
```
- **PITFALL:** USER token pendek kadaluarsa ~1 jam. PAGE token hasil exchange **TETAP SHORT-LIVED ~6 jam** untuk akun ini (bukan 60 hari). Selalu validate sebelum pakai.
- **PITFALL:** Jangan pakai USER token langsung buat posting → error `(#200) requires app installed in group`. Harus lewat PAGE token dari `/me/accounts`.
- Simpan `FB_APP_ID`+`FB_APP_SECRET`+`FB_PAGE_TOKEN`+`FB_PAGE_ID`+`FB_PAGE_NAME` ke `AppData/Local/hermes/ziyan_fb_credentials.env`.

## YouTube Shorts (Celine Aurel Official — `UC0h3xyafx6P6J_CjpzhpSeg`) — TERVERIFIKASI LIVE 2026-08-15
- **Channel BENAR: `UC0h3xyafx6P6J_CjpzhpSeg` (Celine Aurel Official, @celineaurelofficial).** JANGAN pakai `UC8Lzhi5_SvJZcecD79xIiog` (itu Compound Daily, BEDA channel).
- **Token: `token_celine.json`** (folder bot `ziyancorp/ziyan_archive_bot/`), hasil `oauth_channel_check.py` (fail-closed preflight `channels.list(mine=true)` → cocok target baru upload).
- **RE-AUTH saat expired (401):** jalankan `oauth_channel_check.py --client client_secret.json --token token_celine.json --expected-channel UC0h3xyafx6P6J_CjpzhpSeg` → buka URL consent di browser Bos → pilih Google Account owner Celine → authorize → script auto-save token baru. `client_secret.json` = Desktop app (`project_id: ziyancorp`, redirect `http://localhost`). Token status Testing → refresh expired 7 hari → re-consent periodik WAJIB.
- **PITFALL:** `ziyan_credentials/youtube_token_celineaurel.json` (lama) = **EXPIRED (401)**. Jangan pakai. Pakai `token_celine.json` hasil re-auth.
- **Upload (API resmi, BUKAN Playwright-primary):** `youtube_upload_celine.py --file X.mp4 --title T --description D --privacy private --client client_secret.json --token token_celine.json --expected-channel UC0h3xyafx6P6J_CjpzhpSeg`. Resumable + retry 5xx + SAFETY_STOP kalau response channelId ≠ target. Test privat dulu, cek video ID, baru publish manual.
- **Integrasi `distributor.py`:** `post_youtube()` panggil `youtube_upload_celine.py` via subprocess (bukan `yt_automator` Playwright). Target `"youtube"`/`"all"` → upload privat ke Celine Official.
- **Fallback Playwright:** `youtube_studio_upload.py` (profile `profiles/youtube-celine`, headed bootstrap, owner login manual, fail-closed kalau login/MFA/Service unavailable). HANYA kalau API gagal.
- **PITFALL Brand Account:** error "Service unavailable" saat pilih Brand Account = masalah channel-switching Google. Fix: set Celine **default channel** (YouTube → Advanced → Default Channel), hapus token, consent ulang. Jangan bypass/cookie automation.

## Telegram Channel — PITFALL CURL 404 VS BOT OBJECT (TERBUKTI 2026-08-15)
- Bot bisa **baca** pesan channel (`CHAT_DEBUG type=channel id=-1004373452633`) tapi **raw `curl` `sendMessage`/`getChat` ke channel ID selalu 404**.
- **ROOT CAUSE:** `python-telegram-bot` library punya auth context berbeda dari raw `curl` shell → `context.bot.send_message(chat_id=..., text=...)` **JALAN**, `curl .../sendMessage` **404**.
- **FIX:** POST ke channel PAKAI **bot object** (`await context.bot.send_message(...)`), BUKAN `requests.post` curl. Jangan diagnosis "bot gak punya akses" dari curl 404 — tes via bot object dulu.
- Channel Celine Aurel arsip = `-1004373452633` (terverifikasi dari `forward_origin.chat.id`, PTB 22.6).

## Instagram (Celine Aurel) — VIA FB GRAPH API [TERBUKTI 2026-08-10, VERIFIED LIVE 2026-08-15]
- **IG Business ID: `17841444876830769`** (username `@celineaurel99`). Terverifikasi posting live (media `17885900343655280` muncul di IG).
- **Butuh Instagram Business Account linked ke FB Page "Celine Aurel"**. Jika belum linked → auto-skip dengan warning.
- Token: **Sama dengan FB Page token** (dari vault, lihat section VAULT GPG).
- **VERIFY LINK (jalankan sebelum post):**
  ```bash
  PAGE_TOK=$(bash bin/token_vault.sh get fb_page_token 2>/dev/null | tr -d '\n')
  curl -s "https://graph.facebook.com/v20.0/975723622288353?fields=instagram_business_account{id,username}&access_token=$PAGE_TOK"
  ```
  - Response punya `instagram_business_account` → LINKED ✅, ambil `id` = `ig_user_id`.
  - Error `(#100) Tried accessing nonexisting field` → **BELUM LINKED** ❌ (IG gak terhubung ke Page, atau IG bukan Business/Creator account).
- **PITFALL (2026-08-15):** `threads_business_account` field **TIDAK VALID** di v20.0 Page request (error 100). Jangan gabung IG+Threads dalam 1 query. Threads pakai endpoint terpisah (lihat section Threads).
- **Photo**: `POST /{ig_user_id}/media` (create container: `image_url` atau `source` file) → `POST /{ig_user_id}/media_publish` (publish: `creation_id`).
- **Video/Reels**: `POST /{ig_user_id}/media` dengan `media_type=REELS` + `video_url`/`source` → polling `GET /{creation_id}?fields=status_code` sampai `FINISHED` → `POST /{ig_user_id}/media_publish`.
- Caption: sama format (link di baris 1, caption, hashtag). Max 2200 char.
- **PITFALL:** Video processing butuh waktu (30-300 detik). Polling timeout 5 menit.
- **PITFALL:** IG Celine Aurel HARUS Professional/Business account + ter-link ke FB Page yang benar (`975723622288353`). Kalau Bos bilang "sudah link di HP" tapi API bilang field gak ada → cek IG account type + pastikan link ke Page ini, bukan Page lain.
- **Graceful fallback**: Jika `ig_user_id` kosong → log warning "Instagram not available (no IG Business Account linked to FB Page)" → jalankan FB only.

## Threads (Celine Aurel) — VIA FB GRAPH API [2026-08-15]
- **Butuh Threads account linked ke FB Page "Celine Aurel"** (sama syarat IG: Professional + ter-link).
- **ENDPOINT TERPISAH** (bukan field di Page request):
  ```bash
  PAGE_TOK=$(bash bin/token_vault.sh get fb_page_token 2>/dev/null | tr -d '\n')
  # ambil Threads Business ID
  curl -s "https://graph.threads.net/v1.0/me?fields=id,username,threads_business_account&access_token=$PAGE_TOK"
  ```
  - Threads API base = `https://graph.threads.net/v1.0/` (BUKAN graph.facebook.com).
  - `threads_business_account` field di **Threads API `/me`**, bukan di FB Page API.
- **Post Threads:** `POST https://graph.threads.net/v1.0/{threads_user_id}/threads` (text) → `POST .../{creation_id}/publish`.
- **PITFALL:** Threads token = **SAMA dengan FB Page token** kalau sudah ter-link. Tidak perlu token terpisah.
- **PITFALL (2026-08-15):** `threads_token.gpg` di vault = **EXPIRED** (error 190 saat decrypt+validate). Jangan pakai. Ambil dari Page token setelah link sukses.

## Agent Handoff — Uraian Masalah (untuk delegasi ke agent lain)
Bila Bos minta serahkan ke agent lain, berikan ringkasan faktual (BUKAN mutar sendiri):
- Sebutkan status tiap platform (VALID / EXPIRED / NOT LINKED) + bukti (response API / error code).
- Sertakan app_id, page_id, user_id, vault path + cara decrypt (`bin/token_vault.sh get <name>`).
- Jangan minta Bos klik UI berulang tanpa konfirmasi error code spesifik.

## Debug Recipes
- `references/social_publisher_debug.md` — Telegram curl-404-vs-bot-object, YouTube Celine re-auth (`oauth_channel_check.py` → `token_celine.json`), IG verified live IDs.

## X/Twitter (OAuth1a, FREE — AKTIF 2026-08-08)
- Account: `@AgenticsID`. Credential: `~/.x_credentials` (CONSUMER_KEY/SECRET, ACCESS_TOKEN/SECRET).
- **JANGAN pakai Bearer/App-only** → 403 Forbidden ("Unsupported Authentication"). WAJIB **OAuth1a User Context**:
  ```python
  from requests_oauthlib import OAuth1Session
  o = OAuth1Session(CK, client_secret=CS, resource_owner_key=AT, resource_owner_secret=ATS)
  r = o.post("https://api.twitter.com/2/tweets", json={"text": caption})  # 201=OK
  # media: upload dulu ke upload.twitter.com/1.1/media/upload.json lalu masukkan media_ids
  ```
- Script: `post_tweet.py` (CLI) + `ziyan_intake/post_tweet_helpers.py` (dipanggil `scheduler._post_x`).
- Hapus: `o.delete(f"https://api.twitter.com/2/tweets/{id}")`.
- PITFALL: `.x_credentials` di disk SERING kosong (template). Isi asli ada di `.x_credentials.bak` → `cp .x_credentials.bak .x_credentials` kalau `len==0`.

## Google Sheet Arsip (tab "Arsip")
- Tiap post → 1 row (enqueued_at, file_path, deskripsi, link_aff, caption, fb_id, yt_id, x_id, posted_at) ke Sheet `1wLqdaYcjd...` tab `Arsip`.
- Pakai **curl ke Sheets API v4 append** (bypass lib `google-api` rusak: `_cffi_backend` missing di venv). Client secret: `AppData/Local/hermes/google_client_secret.json` (`installed` key).
- Fallback lokal: `ziyan_intake/arsip.csv`.

## Batch & Scheduler (aturan Bos 8/8)
- Bos kirim BANYAK file/link sekaligus → **JADWALKAN per 77 menit**, bukan langsung semua.
- **FB + YT Shorts + X/Twitter SEMUA AKTIF.** YT public. X via OAuth1a.
- Tiap post → arsip ke Google Sheet tab `Arsip` + `ziyan_intake/arsip.csv`.
- Loop: `uv run python3 ziyan_intake/scheduler.py loop` (background). `once` = post 1 item. `enqueue()` via Python import.

## Keamanan
- Token FB/YT TIDAK di-print ke chat. Simpan di disk (`OneDrive/ziyan_pending/`, `AppData/Local/hermes/`).
- Bos kirim token mentah ke chat → terima, simpan ke file, langsung colok (jangan echo/print balik).
