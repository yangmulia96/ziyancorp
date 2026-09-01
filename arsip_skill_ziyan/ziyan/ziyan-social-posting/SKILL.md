---
name: ziyan-social-posting
description: ZIYAN auto-post FB, YouTube, X dari Telegram.
---

# ZIYAN Social Posting Pipeline

## Kapan pakai
- Bos kirim foto/video + deskripsi + link affiliate ke Telegram (Hermes DM)
- Mau auto-post ke FB Page, YouTube Shorts, X dengan caption affiliate
- Setup / perpanjang token FB Page, X, atau YouTube

## Arsitektur (terbukti jalan, 8 Agt 2026)
```
Bos kirim file+teks ke chat Telegram (Hermes DM)
  → Orion simpan file ke ziyan_intake/files/
  → generate caption via 9router (model openrouter/auto)
  → enqueue ke ziyan_intake/queue.json
  → scheduler.py loop: tiap 77 menit post 1 item ke FB (+YT kalau video) + X
  → arsip 1 row ke ziyan_intake/arsip.csv
```

**JANGAN pakai n8n webhook untuk intake lokal.** n8n 2.33 gagal register webhook dari DB insert manual ("webhook not registered" / "0 published workflows"). Pakai Python scheduler sebagai otak; n8n skip.

## Format Caption (WAJIB — preferensi Bos)
Ada link affiliate:
```
[LINK AFFILIATE di BARIS 1]
[caption dari deskripsi, 2 kalimat casual+persuasive, Bahasa Indonesia]
#[hashtag platform, 3-5 buah]
```
Contoh FB:
```
https://s.shopee.co.id/6L3SphnQcZ
Crop top HUT RI ini adem dipakai harian, pas buat gaya merah putih yang santai tapi stylish. Cuma Rp23.170!
#cropop #hutri #bajumerahputih
```
Gak ada link → caption casual (persona influencer), tetap bisa lewat AI.

## Auth Setup (detail: references/auth.md)
- **FB Page**: user token pendek → `GET /me/accounts?fields=id,name,access_token` → ambil PAGE token → exchange pakai `FB_APP_ID`+`FB_APP_SECRET` (`grant_type=fb_exchange_token`) → **60 hari**. Selalu TEST POST lalu DELETE untuk verifikasi.
- **X/Twitter**: BEARER / App-only → **403 Forbidden** (free tier read-only untuk v2 write). Pakai **OAuth1a User Context** (`requests_oauthlib.OAuth1Session` dengan CONSUMER_KEY/SECRET + ACCESS_TOKEN/SECRET). Free bisa posting teks + media.
- **YouTube**: `access_token` di file `ziyan_youtube_token.json`; kalau expired, refresh pakai `refresh_token` via `https://oauth2.googleapis.com/token`. Upload `privacyStatus=public`.

## Batch & Scheduling
- Bos kirim banyak sekaligus → jadwalkan **per 77 menit** (bukan langsung semua).
- X ikut dipost (Bos setuju, cara gratis OAuth1a jalan — bukan paid $100/bln).

## Pitfalls (DILARANG — dari koreksi Bos)
- **JANGAN biarkan test post jadi spam di page.** Tiap TEST POST wajib di-DELETE. Bos marah lihat spam test ("Siapa yang posting? Hapus semua"). Verifikasi lewat curl DELETE, bukan biarkan.
- **JANGAN hardcode token** di script — baca dari file (`OneDrive/ziyan_pending/fb_page_token.txt`, `~/.x_credentials`).
- **JANGAN print token** ke chat — simpan ke file, baca lewat script.
- Token FB = **60 hari**, gak perlu ganti tiap hari. Bos sempat mengira "harus ganti terus" — salah, sudah di-extend.
- **TELEGRAM CHANNEL POST (PENTING — temuan 15 Agt 2026)**: Bot post ke channel HARUS pakai `context.bot.send_message(chat_id=CHANNEL_ID, text=...)` dari dalam handler python-telegram-bot (PTB 22.6). **JANGAN pakai raw `curl`/requests ke `sendMessage`** — akan return 404 "Not Found" meski bot sudah jadi admin channel. Ini bug/limitation: PTB library pakai auth context berbeda dari curl. Fakta: curl 404 berulang 12x, tapi `context.bot.send_message` sukses (terbukti log). Gunakan bot object, bukan curl, untuk semua write ke Telegram.
- **PTB 22.6 forward detection**: atribut bukan `message.forward_from_chat` (error AttributeError) tapi `message.forward_origin` (type `MessageOriginChannel`, punya `.chat.id`).
- **Channel admin check**: bot di-list admin ≠ bot bisa write via curl. Validasi lewat `context.bot.send_message` dari handler, bukan `getChat` via curl.
- **Google SA vs OAuth untuk Drive upload**: Service Account (`hggh-568@ziyancorp`) GAGAL upload ke Drive personal (quota 0, error `storageQuotaExceeded`). Solusi: pakai **OAuth user** (`token.json` dari `client_secret.json` Desktop app) — quota user, bukan SA. Bot `google_workspace.py` auto-prioritize `token.json` kalau ada.
- **Celine Aurel arsip channel**: chat_id `-1004373452633`, bot `@Zynarsipbot` admin. Command `/distribusi PROD-ID all` → generate caption AI (format Celine, tanpa harga) → post ke channel via bot object. FB Page Celine: `975723622288353` (token di `OneDrive/ziyan_pending/fb_page_token.txt`). YT Celine: `youtube_token_celineaurel.json` (channel `UC8Lzhi5_SvJZcecD79xIiog`). IG/Threads: token TIDAK ADA di disk (hanya `.gpg` encrypted, butuh passphrase).

## Arsip
- Tiap post → 1 row CSV `ziyan_intake/arsip.csv`: `enqueued_at, file_path, deskripsi, link_aff, caption, fb_id, yt_id, x_id, posted_at`.
- Google Sheet ditunda (token expired + client_secret hilang di disk) → pakai CSV lokal dulu.

## Support files
- `references/auth.md` — resep token exchange FB + snippet OAuth1a X + YT refresh
- `references/fb_ig_threads_token_reauth.md` — vault decrypt/set, FB Page re-auth, IG "sudah link di HP tapi API bilang belum" diagnosis, Threads endpoint
- `templates/scheduler.py` — scheduler lengkap (enqueue / run_once / loop + FB/YT/X + arsip CSV)
- `templates/post_tweet.py` — X poster OAuth1a (teks + media)
