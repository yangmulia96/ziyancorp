---
name: ziyan-google-archive
description: Build and run ZIYAN's Telegram→Drive+Sheets archive bot.
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
---

# ZIYAN Google Archive Bot

## When to use
- Bos wants to archive generated content + affiliate links into Google Drive with a searchable Sheets catalog.
- Building/operating the `@Ziyanclipperbot` archive pipeline (Telegram intake → Drive + Sheets → Telegram confirmation).
- Any task where Hermes must read/write the archive (search products, add links, export catalog) without Bos in the loop.

## BOSS STYLE — EMBED (durable, dari sesi 16/8)

**1. AUTONOMY: "Kau yang tau mekanismenya, jangan tanya aku."** Bos benci diberi pilihan kecil yang agent bisa putuskan sendiri. Kalau butuh keputusan teknis (format caption, mekanisme orphan-kill, mana folder, struktur cron), **AMBIL KEPUTUSAN + JELASKAN + EKSEKUSI**, jangan `clarify`/`tanya`. Hanya eskalasi: anggaran besar, strategi major, risiko reputasi, atau butuh Bos login manual (OAuth/browser). Kalau Bos kasih 2 opsi lalu bilang "kau yang tau" → artinya "pilih yang terbaik, jalanin".

**2. VALIDASI MENYELURUH sebelum lapor "beres".** Bos bilang "Validasi dulu betul betul. Memory, history, skill, log dan sebagainya." Maksudnya: jangan claim sukses dari log doang. Verifikasi rantai penuh:
- **Token**: tes via API (`graph.facebook.com/v20.0/me?access_token=...` → 200?) bukan cuma baca `.env`.
- **Post live**: cek `graph.facebook.com/<post_id>` / `graph.threads.net/v1.0/<id>` balik → match caption + timestamp.
- **Sheet/Drive**: `gw.sheets...values().get` + `gw.drive.files().list` langsung, bukan asumsi.
- **Memory/skill/history**: baca file aktual (grep), jangan ingat-ingat. `search_files` sering gagal di Windows path style (`C:/...` vs `C:\`) → pakai `terminal` + `grep`/`cat` lewat bash.
- **Fakta vs klaim**: tiap "bot jalan/sukses" harus punya bukti API/log, bukan tebakan.

**3. JANGAN dramatisasi banyak failure jadi masalah terpisah.** Bos komplain "kok jadi banyak lagi masalahnya" padahal akar cuma 1 (token expired). Gabungkan ke 1 akar + sebutin apa yang SUDAH beres. Sama spirit ANTI-LOOP: cari akar tunggal, jangan list tiap gejala sebagai bug baru.

**4. HAPUS postingan test yg asetnya gak cocok = tugas validasi.** Bos minta "hapus semua postingan yang salah" → yang asetnya random (picsum/dune) bukan asli. Hapus via API: FB `DELETE graph.facebook.com/v20.0/<post_id>?access_token=...` (sukses). **Threads GAGAL hapus via API** (`code:10 Application does not have permission` / kadang `Cannot parse access token`) → Bos harus hapus MANUAL di HP (3-dot → Delete). Jangan janjikan hapus Threads otomatis.

## Architecture (proven 2026-08-15, RESTRUCTURED 2026-08-16)
```
Telegram Bot (@Zynarsipbot, python-telegram-bot)
  → Intake Handler (batch window 60s after last file — Bos spec "1 menit", BATCH_WINDOW_SECONDS=60)
  → Google Drive: Celine Arsip/YYYY-MM/PROD-YYYYMMDD-XXXXXX/
        ├── 01_VIDEO/  02_FOTO/  03_OTHER/
        ├── AFFILIATE.json
        └── PRODUCT_INFO.txt
  → Google Sheets ARSIP_MASTER tabs: PRODUCT_MASTER / CONTENT_ASSETS / PROCESS_LOG
  → confirm back to Telegram
```
- 1 product = many photo/video assets + 1..N affiliate links (Shopee, TikTok Shop, other).
- Product ID auto: `PROD-YYYYMMDD-XXXXXX`; Asset ID: `AST-YYYYMMDD-XXXXXX`.
- Restrict to Telegram user ID(s) via `TELEGRAM_ALLOWED_USER_IDS`.
- Local SQLite (`archive.db`) for dedupe + fast search; Sheets is the human+AI-readable catalog.
- Commands: /start /new /cari /lihat /edit /tambah /hapus_asset /batal. /hapus_asset uses inline-keyboard confirm then Drive Trash (never permanent delete).

### "Celine Arsip" folder restructure (2026-08-16)
Bos wanted BOTH the archive Drive folder AND the Sheet inside ONE folder "Celine Arsip" (previously the Drive archive lived under `ZIYAN_ARCHIVE/YYYY-MM/` and the Sheet lived elsewhere).
**Procedure (idempotent, reversible):**
1. Create folder "Celine Arsip" at the old root (`GOOGLE_ROOT_FOLDER_ID` before change).
2. `drive.files().update(fileId=<2026-08 folder>, addParents=<celine_id>, removeParents=<old_root>)` → moves archive folder in.
3. `drive.files().update(fileId=<ARSIP_MASTER sheet>, addParents=<celine_id>, removeParents=<old_parent>)` → moves Sheet in.
4. Update `.env`: `GOOGLE_ROOT_FOLDER_ID=<celine_id>` so NEW archives auto-land in `Celine Arsip/2026-08/PROD-*`.
- Both archive + Sheet now visible together in one Drive folder = Bos's single source of truth.
- Agent readability unchanged: Sheets API + `AFFILIATE.json` still the AI entry points.

## CRITICAL: Service Account quota = 0 (GOTCHA)
A free GCP project's SA (`*.iam.gserviceaccount.com`) has **Drive storage limit = 0 bytes**. SA CANNOT create files in its own Drive → `403 storageQuotaExceeded`.
**FIX (proven):** create `ZIYAN_ARCHIVE` folder + `ARSIP_MASTER` Sheet in **Bos's personal Drive**, then **share both to the SA email as Editor**. SA then writes into Bos's Drive (quota belongs to Bos). Verify: `files().get(fileId, fields='capabilities(canEdit)')` → `True`.
See `references/sa_quota_workaround.md`.

## CRITICAL: venv isolation + PYTHONPATH pollution (GOTCHA)
This machine has a global `PYTHONPATH` pointing at Hermes venv (`.../hermes-agent/venv/Lib/site-packages`). Running a project venv WITHOUT unsetting it makes Python import Hermes's (often broken/outdated) packages → `ModuleNotFoundError: _cffi_backend`, `cryptography`, `requests`, `google.api_core`, etc. `pip install` also leaks into Hermes venv.
**FIX (proven):** create a dedicated venv per project and ALWAYS run with `env -u PYTHONPATH`:
```
env -u PYTHONPATH ./venv/Scripts/python.exe -m pip install -r requirements.txt
env -u PYTHONPATH ./venv/Scripts/python.exe -m ziyan_bot.bot
```
See `references/venv_isolation.md`. Windows process inspection (count/kill real bots, verify before kill, 9router recovery) → `references/deploy_debugging.md`. OAuth Desktop setup + SA-upload blocker → see Auth path section above.

## Auth path: SA vs OAuth
`google_workspace.py` auto-detects credential type: if `credentials.json` has `"type": "service_account"`, use it directly (no browser consent, no-expiry, AI-callable). OAuth (`token.json`) only needed for personal-Drive ops without an SA share.
**REALITY 2026-08-15: SA CANNOT upload to personal Drive (quota 0)** even when folder shared as Editor → `403 storageQuotaExceeded`. So for the archive bot that WRITES files, **OAuth user token is the working path** (`client_secret.json` + `token.json`). SA is fine only for READS. Bot runs with `GOOGLE_CREDENTIALS_FILE=client_secret.json` (OAuth) + `token.json` present.
**NEVER** echo the SA private key or Telegram token in chat/README. Store in `.env` (gitignored).

### SA CANNOT upload to personal Drive (the real upload blocker)
Even when the `ZIYAN_ARCHIVE` folder is shared to the SA as Editor (`canEdit=True`), Google still bills the **SA's own** storage quota (=0 on free tier) on every `files().create()` → `403 storageQuotaExceeded: Service Accounts do not have storage quota`.
- **Working fix = OAuth user token (free, personal Drive).** Create an **OAuth Desktop client** (NOT SA) at Google Cloud → APIs & Services → Credentials → Create OAuth client ID → Desktop app. Download `client_secret.json` to project root. Then:
  `env -u PYTHONPATH GOOGLE_CREDENTIALS_FILE=client_secret.json ./venv/Scripts/python.exe scripts/google_auth.py`
  → opens browser → Bos logs in (same machine as bot, because redirect_uri=http://localhost:PORT) → Allow → `token.json` written. Browser "site can't be reached" after Allow = normal.
- **OAuth consent test-user gotcha:** new OAuth clients are "restricted to test users" — add Bos's Google email as a **Test User** at OAuth consent screen, else login is rejected ("not a test user").
- After `token.json` exists, bot uploads using **Bos's** Drive quota (not SA's) → no 403. Keep `credentials.json` (SA) for reads if desired; `google_auth.py` honors `GOOGLE_CREDENTIALS_FILE` override so SA and OAuth creds coexist.
- `google_auth.py` flow uses `InstalledAppFlow.run_local_server(port=0)` — run it with `env -u PYTHONPATH` and the override above; do NOT run it inside the already-running bot process.

## GOOGLE TOKEN EXPIRY & SOLUSI PERMANENT (NEW 2026-08-16)
Bot arsip pakai OAuth `token.json` (Desktop client). Token sering EXPIRED → bot "collapse" tiba-tiba (arsip gagal upload). Telegram bot token & FB_PAGE_TOKEN = **gak expired** (cuma invalid kalau revoke). Yang bikin bot mati = **cuma Google token.json**.

**Opsi biar gak expired (dari Hermes, butuh konfirmasi Manus):**
1. **Set OAuth app ke "Production"** di Google Cloud Console → refresh_token gak dicabut otomatis → token auto-renew selamanya (butuh verify domain/PR). Paling gampang tapi butuh Bos login Google Cloud.
2. **Service Account (JSON key)** → gak pernah expired, paling stabil. TAPI lihat GOTCHA di atas: SA quota=0 → **SA gak bisa UPLOAD ke personal Drive** (403). Jadi SA hanya aman kalau folder arsip dibuat di SA Drive sendiri (bukan Bos Drive) — atau semua arsip pindah ke SA Drive. Untuk arsip saat ini (Bos Drive), **OAuth Production = lebih praktis**.

**Mitigasi sementara (sudah jalan):** Cron harian 08:00 (`cronjob` job `5df26507ece9` "ZiyanBot Health Check") cek process bot + Google token valid + FB token. Kalau expired → alert Bos (bukan auto-fix, butuh Bos re-auth via browser). Bos mau solusi permanent → tanya Manus di `SHARED_MEMORY.md` (`ziyancorp/ZIYAN_BRIDGE`, section "TANYA: Google Token Bot Arsip Gak Expired?").

## Deploy checklist
1. `.env`: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USER_IDS`, `GOOGLE_CREDENTIALS_FILE=client_secret.json`, `GOOGLE_ROOT_FOLDER_ID` (= "Celine Arsip" folder id sejak 2026-08-16), `GOOGLE_SPREADSHEET_ID` (= ARSIP_MASTER, lives INSIDE Celine Arsip), `BATCH_WINDOW_SECONDS=60`, `TIMEZONE=Asia/Jakarta`.
2. Place SA key as `credentials.json` in project root.
3. `env -u PYTHONPATH ./venv/Scripts/python.exe -m ziyan_bot.bot` (background).
4. Verify log: `Application started` + `getUpdates 200 OK`.
5. Test from phone: send caption + files → bot replies Product ID + folder URL.

## AI-accessibility (why this design)
Sheets = single source of truth readable by both Bos (browser) and Hermes (API). Hermes can search/add/export without Bos. This satisfies Bos's rule: "once you can access it, don't keep asking me."

## Distribution layer (tahap 2, OUTPUT side)
The bot is the **input/storage** layer. The **distributor** reads `ARSIP_MASTER` and pushes to
platforms with AI-generated captions. See `references/distributor.md` (Sheets → 9Router natural
caption → Telegram channel; FB/IG/Threads/YT pending Bos tokens). Python 9Router call pattern
(Bearer key + SSE parse) → `references/9router_python.md`.
- **Caption style Bos (Celine Aurel):** format `[link Shopee]` blank `[deskripsi 1-2 kalimat]`
  blank `[link lain]` blank `[4 hashtag PERSIS]`, **DILARANG sebut harga** (aturan keras, FINAL 16/8). Generate
  natural via 9Router (bukan robotik). `distributor.gen_caption()` sudah pakai prompt ini.

### DEDICATED DISTRIBUTION AGENT (KEPUTUSAN + FINAL RULE 2026-08-16)
Bos minta **1 agent khusus distribusi konten** (terpisah dari bot arsip & Hermes).

**FINAL DISTRIBUSI RULE (Bos revisi 16/8 — OVERRIDE aturan 8/77 menit & 6h-spacing SEBELUMNYA):**
- **Jadwal UPLOAD: 4x sehari, FIX** → `08:57`, `12:34`, `16:08`, `20:13` (WIB, Asia/Jakarta).
- **Mekanisme:** 1 konten diupload **SEKALIGUS ke SEMUA platform** (TG Channel, FB Page, IG @celineaurel99, YouTube Celine Aurel, Threads @celineaurel99) di jam tersebut. BUKAN stagger/6h — SEMUA platform di 1 waktu. (Ini lampi dari `ziyan-autonomous-orchestration` "Anti-Spam 1 post/6h" — Bos FINAL pilih simultan 4 jam fix. Bos wins.)
- **Caption (FIX):** `[Link Shopee]` + blank + `[deskripsi natural TANPA HARGA]` + blank + `[link affiliate selain Shopee, kalau ada]` + `[PERSIS 4 hashtag]`.
  - Contoh: `https://s.shopee.co.id/AUtAt2Lpuw\n\nKaos Oblong Cowok lengan pendek tema Kemerdekaan 17 Agustus ke-80, tersedia ukuran S-XXL...\n\n<other link>\n#h1 #h2 #h3 #h4`
  - ❌ JANGAN sebut harga. ✅ Link Shopee BARIS PALING ATAS. ✅ PERSIS 4 hashtag.
- **Sumber arsip:** `ARSIP_MASTER` Sheet (tab PRODUCT_MASTER) atau `AFFILIATE.json` di `Celine Arsip/2026-08/PROD-*`. Agent baca → generate caption → post ke 5 platform.

**Desain agent:**
- **Trigger:** cron di 4 jam fix (`cronjob` schedule `57 8,12,16,20 * * *`) → ambil produk berstatus PENDING/terbaru → distribusikan. (Bukan cuma perintah Bos; Bos mau otomatis di 4 jam itu.)
- **Flow:** (1) baca `AFFILIATE.json` produk → link + aset; (2) generate caption natural via 9Router (format di atas); (3) panggil `distributor.py` per platform; (4) mark status di Sheet (anti-double); (5) lapor hasil.
- **Platform aktif (REVISI 16/8 — HAPUS Telegram Channel):** Bos bilang platform CUMA **YT, FB, IG, Threads**. TG Channel TIDAK dipakai distribusi. FB/IG/YT/Threads = auto-skip kalau token expired, lapor ke Bos.
- **YouTube PRIVACY = PUBLIC** (bukan private). `post_youtube` di `distributor.py` hardcode `privacy=private` → agent harus override ke `public` (lihat `distribute_agent.py` `post_youtube_public()`).
- **Caption:** generate AI natural (9Router, gak ada harga, 4 hashtag, style Celine Aurel) — BUKAN title mentah. `distributor.gen_caption()` bikin 5 hashtag + bisa leak harga dari title → agent PAKAI `build_caption()` sendiri (buang pola `dengan harga RpXX.XXX` + `Dapatkan di Shopee sekarang`).
- **JANGAN buat agent ini manual/blocking.** Pakai `delegate_task` (lihat `ziyan-autonomous-orchestration` → DELEGASI WAJIB). Hermes hanya desain + sintesis, sub-agent yang eksekusi `distributor.py`.

**DISTRIBUTION AGENT — IMPLEMENTASI + EKSEKUSI PERDANA (2026-08-16, TERBUKTI):**
- File: `distribute_agent.py` (di repo `ziyancorp/ziyan_archive_bot`).
- **Cron job distribution BELUM dibuat** (baru rule + script). Bos setuju build dulu, revisi kalau kurang.
- **Bug yang ditemukan & fixed saat eksekusi perdana:**
  1. `from datetime import ZoneInfo` → SALAH (Python 3.13 WindowsApps). Benar: `from zoneinfo import ZoneInfo`. (`mark_published` pakai `ZoneInfo("Asia/Jakarta")`.)
  2. `get_products(limit=1)` ambil **baris PERTAMA** (produk 15 Aug lama), BUKAN terbaru. Agent pakai `get_products_latest()` (reverse rows → ambil terakhir = `PROD-20260816-260F26`).
  3. YT `video_path` diisi dari `r[6]` (folder_url Drive) BUKAN path lokal → selalu skip. Fix: agent cari video dari folder Drive via `AFFILIATE.json` assets, download lokal, baru upload. Atau simpan path lokal di Sheet kolom benar.
  4. `FB_PAGE_TOKEN=$(bash ...)` di 1 line bash git-bash → expanded jadi command aneh (`zcej: command not found`). FIX: `export FB_PAGE_TOKEN="$(bash /c/Users/arija/bin/token_vault.sh get fb_page_token 2>/dev/null | tr -d '\n')"` di line terpisah, lalu `env -u PYTHONPATH ./venv/Scripts/python.exe distribute_agent.py`.
- **Hasil eksekusi perdana** (`PROD-20260816-260F26`, Kaos Kemerdekaan):
  - ✅ **Facebook**: post ID `975723622288353_122141892801223725` (public)
  - ✅ **Threads**: post ID `18135665863607524` (public)
  - ❌ **Instagram**: token expired (`Session has expired on Saturday, 15-Aug-26`) → butuh re-auth `fb_reauth.py`
  - ⏭️ **YouTube**: skip (produk foto-only, `video_path` kosong di Sheet)
  - Caption (format Bos, tanpa harga, 4 hashtag) → terbukti jalan.
- **Laporan wajib**: agent return JSON `{status, product_id, caption, results}` → Hermes forward ke Bos + copy ke diri sendiri. Bos minta "laporan langsung ke aku, copy-an dikirim ke kamu".

**MANUS JAWAB TOKEN (merged ke SHARED_MEMORY.md 16/8):**
- OAuth "Production" ≠ abadi, tapi paling awet. Bot tetap wajib handle `invalid_grant`.
- **Service Account TIDAK support YouTube Data API** → YT tetap OAuth user. Drive/Sheets bisa SA (folder dibagikan ke email SA).
- Cron/autostart harus diverifikasi via `schtasks`/Task Scheduler, bukan cuma klaim agent.
- Rekomendasi: migrasi Drive/Sheets ke SA terpisah, YT pertahankan OAuth.

**Verified di SHARED_MEMORY.md** (`ziyancorp/ZIYAN_BRIDGE`, section "REVISI DISTRIBUSI KONTEN — 16/8 (FINAL)"). Full spec + Manus token answer → `references/distribution_schedule_16aug.md`.

## PITFALL (2026-08-16 — distribusi eksekusi perdana, SECOND RUN)
SETELAH fix pertama, `distribute_agent.py` dijalankan lagi (foreground). Hasil:
- ✅ **FB sukses** (post baru — `FB_PAGE_TOKEN` dari vault MASIH VALID)
- ❌ **IG**: `META_USER_TOKEN` expired (`Session has expired on Saturday, 15-Aug-26 05:00 PDT`)
- ⚠️ **Threads**: awal dilaporkan expired, tapi SETELAH validasi API ulang (`graph.threads.net/v1.0/me` return 200) = **MASIH VALID** — post perdana sukses. JANGAN asumsikan Threads expired kalau META expired; cek masing-masing via API.
- ❌ **YT**: `next_chunk()` gagal (`token_celine.json` punya refresh_token, tapi upload error — kemungkinan YT Data API quota/network, **BELUM resolved**)
- ✅ **mark PUBLISHED di Sheet FIXED** (ZoneInfo benar)
- ✅ **aset ASLI dari AFFILIATE.json** (download dari Drive) FIXED — gak lagi picsum fallback

**FAKTA PENTING — "banyak masalah" itu cuma 1 AKAR:** Bos komplain "kok jadi banyak lagi masalahnya". Jujur: gak ada bug baru. SEMUA failure = **TOKEN EXPIRED**.
- `FB_PAGE_TOKEN` (vault) = PERSISTEN, jalan terus
- `META_USER_TOKEN` + `THREADS_USER_TOKEN` = EXPIRE ~harian (session 15 Aug mati 16 Aug)
- `Google token.json` = masih valid (Drive/Sheets jalan)

**LESSON KOMUNIKASI (Bos style — EMBED):** kalau lapor status distribusi, **JANGAN** list tiap platform sebagai "masalah terpisah". Gabungkan jadi 1 akar: *"1 akar = Meta/Threads token expired, butuh re-auth Bos. FB jalan. YT pending debug. Agent + caption + mark status SUDAH beres."* Bos benci laporan yang bikin kayak sistem hancur padahal cuma token mati. Ini sama spiritnya dgn ANTI-LOOP: jangan dramatisasi, cari akar tunggal.

**RE-AUTH Meta/Threads (Bos harus login browser) — DIPERBARUI 16/8:**
- **Threads**: pakai `threads_reauth.py` (TERPISAH dari `fb_reauth.py`, per Manus 16/8). JANGAN campur FB credential. Threads App ID `1346767533487099` (vault `threads_app_id`), secret `threads_app_secret`. Endpoint `graph.threads.com`/`graph.threads.net` (bukan `graph.facebook.com`). Flow: `python threads_reauth.py` → Bos authorize HP → copy `https://localhost:8123/?code=XXX` → `python threads_reauth.py "<URL>"` → saves vault `threads_token` + `.env`.
- **Instagram**: App "n8n" status Unpublished + gak punya Instagram Graph API product → IG posting DOWN. Butuh: (a) add "Instagram Graph API" product di app, atau (b) app Business terpisah. IG token via `META_USER_TOKEN` (expired 15 Aug). Re-auth IG = `fb_reauth.py` (FB app) tapi app harus punya IG product dulu.
- **FB**: jalan terus (`FB_PAGE_TOKEN` vault, page token long-lived).
- **JANGAN asumsikan Threads expired kalau META expired** — cek masing-masing via API (`graph.threads.net/v1.0/me` vs `graph.facebook.com/v20.0/me`). Sesi 16/8: META expired tapi THREADS masih valid.
- **Secret exposed di SHARED_MEMORY?** → rotate + redact + purge git history (private repo tetap perlu purge setelah rotate). Jangan kirim secret ke chat.

**DELETE POSTINGAN (penting — beda platform beda bisa):** FB = `DELETE graph.facebook.com/v20.0/<post_id>?access_token=<FB_PAGE_TOKEN>` → `{"success":true}`. Threads = **GAGAL via API** (`code:10 Application does not have permission for this action`, kadang `Cannot parse access token` walau token valid). Tidak ada endpoint delete Threads yg bisa dipanggil agent → **Bos hapus manual di HP** (3-dot → Delete). IG = hapus via Graph (`DELETE graph.facebook.com/v20.0/<ig_media_id>`) kalau token valid. JANGAN janjikan "hapus semua postingan otomatis" kalau ada Threads — sebutkan Threads butuh manual.

**TODO (belum done per 16/8):** cron distribusi di 4 jam fix (`57 8,12,16,20 * * *`) BELUM dibuat — baru rule + script `distribute_agent.py`. YT upload `next_chunk` error perlu debug (enable YT Data API? cek quota/hari).

**LAUNCH PATTERN (terbukti, jangan salah):** jangan `FB_PAGE_TOKEN=$(bash ...)` di 1 line (git-bash expand jadi command aneh `zcej: command not found`). Pakai:
```bash
export FB_PAGE_TOKEN="$(bash /c/Users/arija/bin/token_vault.sh get fb_page_token 2>/dev/null | tr -d '\n')"
export CHANNEL_CELINE="-1004373452633"
export GOOGLE_CREDENTIALS_FILE="client_secret.json"
export HERMES_CUSTOM_9ROUTER_API_KEY="$HERMES_CUSTOM_9ROUTER_API_KEY"
env -u PYTHONPATH ./venv/Scripts/python.exe distribute_agent.py
```

## Auto-start on laptop login
- **Startup folder shortcut WORKS** (no admin): create `.lnk` in
  `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\` pointing to a `.bat` that does
  `set PYTHONPATH=` + `env -u PYTHONPATH GOOGLE_CREDENTIALS_FILE=client_secret.json ./venv/Scripts/python.exe -m ziyan_bot.bot`.
- **Task Scheduler FAILS** with `Register-ScheduledTask : Access is denied` (needs admin). Don't
  rely on it unless Bos runs as admin. Startup folder is enough for "run on login".
- Crash-auto-restart needs admin (Task Scheduler `RestartCount`) — optional, skip if not admin.
- **`wmic` DEPRECATED di Windows 11** — jangan pakai di `.bat` autostart (error `'wmic' is not recognized`, bot gak jalan). Untuk anti-orphan di `.bat`, pakai `tasklist` + `taskkill` langsung:
  ```bat
  for /f "tokens=2" %%p in ('tasklist /fi "imagename eq python.exe" /fo list ^| findstr /i "PID:"') do (
      for /f "tokens=*" %%c in ('tasklist /fi "pid eq %%p" /fo list ^| findstr /i "Command Line:"') do (
          echo %%c | findstr /i "ziyan_bot.bot" >nul && taskkill /pid %%p /f >nul 2>&1
      )
  )
  ```
  (Terjadi 16/8: `.bat` pakai `wmic` → gagal → bot gak start sampai diganti `tasklist`.)

## Pitfalls
- SA quota 0 → must share Bos's folder to SA (above). Creating folder via SA fails with 403.
- PYTHONPATH leak → `env -u PYTHONPATH` (above). Forgetting this wastes ~10 install cycles.
- Token/key in chat = security violation.
- Pure Python daemon > n8n for this (simpler, Hermes-friendly — see ziyan-agent-patterns).
- Background process dies on laptop restart — add Task Scheduler / Startup shortcut for persistence.
- **"Akses ditolak." berulang = user ID pengirim tidak ada di whitelist.** DEBUG: patch `reject_if_unauthorized` di `bot.py` untuk `logger.warning("REJECTED user_id=%s (allowed=%s)", uid, sorted(...))`, restart bot, Bos kirim 1 pesan dari HP, baca log `proc_*` → dapat user ID asli → tambahkan ke `TELEGRAM_ALLOWED_USER_IDS` di `.env`. Jangan nebak ID. (Terjadi 2026-08-15: Bos kirim dari HP dgn user ID beda dari token, bot nolak 4x.)
  - **GOTCHA kritis:** `TELEGRAM_ALLOWED_USER_IDS` = **sender user ID** (`message.from.id`), BUKAN token prefix. Token `8684088993:...` → `8684088993` adalah **BOT ID**, bukan ID Bos. Jangan masukkan angka dari token ke whitelist (ini penyebab "Akses ditolak" 4x).
  - **Multi-instance conflict:** jangan jalankan >1 bot. Bos sering double-click `run_bot.bat` berkali-kali + Hermes spawn background → numpuk instance → Telegram error `Conflict: terminated by other getUpdates request`. Pastikan cuma 1 process `python.exe -m ziyan_bot.bot` sebelum start (cek: `Get-CimInstance Win32_Process -Filter "Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'"`).
  - **False-positive process detection:** cek bot jalan pakai `CommandLine LIKE '%ziyan_bot.bot%'` saja → shell/bash yg mengetik perintah itu ikut match (kelihatan 4 bot padahal 0). Filter benar: `Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'`.
  - **JANGAN kill PID dengan nebak.** Kejadian 2026-08-15: agent nebak PID 4180 = "bot manual" (karena RAM 252MB + window title Unknown) lalu `taskkill /F` → ternyata itu **9router** → Hermes gateway + vision + model proxy mati. SELALU verifikasi `CommandLine` via `Get-CimInstance Win32_Process -Filter "ProcessId=<pid>"` SEBELUM kill. Jangan sentuh PID yang CommandLine mengandung `hermes_cli.main serve`, `gateway run`, atau `9router` — itu Hermes gateway / 9router, bukan bot. Recovery kalau 9router ke-kill: `9router --tray --no-browser` lalu `curl -s -m5 http://127.0.0.1:20128/health`.
  - Lihat `references/bot_ops_debugging.md` untuk command set PowerShell lengkap (hitung/kill bot asli, verify sebelum kill, recovery 9router).
  - **Test end-to-end tanpa HP Bos** (simulasi incoming + bukti ke Sheet): `references/bot_end_to_end_test.md`.
  - **`vision_analyze` 404 = empty `auxiliary.vision.model`.** Fix dari agent terminal (NOT a Bos-only step): `hermes config set auxiliary.vision.model kr/claude-sonnet-4.5` (model sudah terbukti ada di 9router). Jangan asumsikan agent gak bisa edit config — coba command dulu.
  - **Channel admin 404 (MAHAL) — FINAL RESOLUTION 2026-08-15:** Bot tampil di list admin + hak post ON, tapi `getChat`/`sendMessage` via **curl 404**. Penyebab sebenarnya: bot bisa **receive** update dari channel (log `CHAT_DEBUG type=channel id=-1004373452633` muncul saat pesan masuk), tapi **curl `requests.post` ke sendMessage 404** karena raw curl gak bawa auth context yang sama dengan bot object. **FIX: distribusi channel HARUS pakai `context.bot.send_message(chat_id=..., text=...)` (python-telegram-bot object), BUKAN `requests.post` curl.** Di handler `/distribusi`, gunakan `await context.bot.send_message(...)` — ini sukses meski curl 404. Jangan buang waktu tes curl `sendMessage` ke channel (akan selalu 404 walau bot bisa post).
  - **Bypass auth untuk channel:** di `reject_if_unauthorized`, izinkan `if chat and chat.type == "channel": return False` (pesan di channel gak bawa user_id, jadi `effective_user=None` → selalu kena reject "Akses ditolak" kalau gak di-bypass). Tanpa ini bot reply "Akses ditolak" ke tiap pesan di channel.
  - **ID channel akurat:** dapatkan dari `forward_origin.chat.id` (PTB 22.6) saat Bos forward pesan channel ke PM bot, atau dari `CHAT_DEBUG id=` di log saat pesan masuk channel. JANGAN nebak ID.
  - **JANGAN suruh Bos mutar UI berulang-ulang.** Bos benci agent yang suruh user klik save/admin berkali-kali padahal sudah done. Kalau screenshot nunjukin bot sudah admin, PERCAYA screenshot → cari penyebab teknis lain (bypass auth, pakai bot object bukan curl).
- **Gmail IMAP cleanup `\\\\Trash` escape gotcha** (tidak terkait bot tapi di sesi yang sama): `STORE +X-GM-LABELS '(\\\\Trash)'` — di Python string harus `'(\\\\Trash)'` salah (terlalu banyak backslash → "Could not parse command"); yang benar pakai `BS=chr(92); lbl=f"({BS}Trash)"` (satu backslash literal). Tanpa ini move gagal total tapi log klaim sukses.

## Pitfalls (2026-08-16 — bot mati setelah restart, debug end-to-end)
Sesi ini bot tiba-tiba gak arsip foto (15 Agustus jalan, 16 Agustus mati). Root causes + fix:

1. **`filters.Caption` (class) crash dispatcher → bot gak process UPDATE APA PUN.** Di PTB 22.x, `filters.Caption` adalah class (bukan instance filter yang valid). Dipakai di `MessageHandler(filters.PHOTO | ... | filters.Caption, ...)` → `TypeError: MessageFilter.check_update() missing 1 required positional argument` saat PTB register/dispatch → entire dispatcher mati → `getUpdates` 200 OK tapi handler gak ke-trigger (gak ada log `ON_MEDIA`). **FIX:** pakai `filters.CAPTION` (constant). Verifikasi: `hasattr(filters,'CAPTION')` → True, `filters.CAPTION` valid. Setelah fix, test `app.process_update(Update.de_json({...}, app.bot))` jalan.
2. **`archive.py` `upload_file` butuh `Path`, dikasih string → crash → produk gak kesimpan.** Line ~93: `self.google.upload_file(local_file.path, ...)` dikirim `local_file.path` (string) padahal `google_workspace.upload_file(self, path: Path, ...)` expect `Path` (pakai `path.name`/`str(path)`). **FIX:** wrap `Path(local_file.path)`. Symptom: `archive_new_product` raise `'str' object has no attribute 'name'`, session files gak pernah ditulis ke Sheet.
3. **`googleapiclient` `drive.files().create(..., timeout=300)` → `TypeError: unexpected keyword argument timeout`.** `timeout=` adalah kwarg httpx/PTB, BUKAN googleapiclient. **FIX:** hapus `timeout=` dari `.execute()`. Untuk upload lambat di koneksi buruk, lebih reliable pakai `MediaFileUpload(resumable=False)` (non-resumable, aman <25MB) daripada naikkan timeout yang gak didukung.
4. **Orphan process numpuk dari restart background berulang.** Tiap launch `terminal(background=true)` spawn process baru; kalau gak kill yang lama dulu → numpuk 8-10 instance bot → berebut `getUpdates` → `Conflict: terminated by other getUpdates request` / `return []` (bot gak dapet update). **FIX sebelum launch:** kill ALL dulu:
   ```powershell
   Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*ziyan_bot.bot*' } | ForEach-Object { taskkill /PID $_.ProcessId /F }
   sleep 3
   # verify cuma 0 sisa:
   Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*ziyan_bot.bot*' } | Select-Object ProcessId
   ```
   Lalu launch 1 instance. Jangan percaya "cuma 1" dari kilasan — cek `CommandLine` sungguhan.
5. **Test simulasi salah arah (pelajaran):** `bot{BT}/sendPhoto` = **bot kirim KE Bos (outgoing)**, BUKAN Bos kirim KE bot (incoming). Bot gak receive itu → `getUpdates` return `[]`. Buat test incoming beneran, pakai `app.process_update(Update.de_json(foto_update_json, app.bot))` dengan mock `telegram.ext.ExtBot.get_file` + `telegram.File.download_to_drive` (copy file lokal), lalu `await app.initialize(); await app.start(); await asyncio.sleep(batch_window+5); await app.stop()`. Pattern test lengkap ada di `references/bot_end_to_end_test.md`.
6. **Verifikasi end-to-end tanpa HP Bos:** jalankan script yang `app.initialize()` + `app.start()` (biar `job_queue`/`finalize_batch` jalan) lalu `process_update` → tunggu > `BATCH_WINDOW_SECONDS` → cek Sheet via `gw.sheets...values().get(...)`. Ini membuktikan chain `on_media → finalize_batch → archive_new_product → Sheet` tanpa intervensi Bos. (Bukti sesi ini: `PROD-20260816-65BAE4` masuk Sheet.)
7. **BOS SPEC test (4 file + 1 link):** `references/bot_end_to_end_test.md` punya function `test_bos_spec()` — kirim 4 update (caption cuma di file #1) → finalize → cek `db.list_assets(pid)` harus 4 aset, 1 link di Sheet. Ini membuktikan aturan "simpan selalu, link hanya jika ada" + batch 1 menit. Run: `env -u PYTHONPATH ./venv/Scripts/python.exe test_bos_spec.py` (set `BATCH_WINDOW_SECONDS=5` di dalam script untuk cepat).

## PITFALL (2026-08-16) — `send_chat_action` ReadError membatalkan finalize
GEJALA: Bos kirim 8 file, bot receive normal (`ON_MEDIA` ✅, download ✅, job `finalize` scheduled), tapi **arsip gak masuk Drive/Sheet sama sekali**. Log: `DISPATCH ERROR: httpx.ReadError` + `telegram.error.NetworkError: httpx.ReadError` di awal `finalize_batch`.
ROOT CAUSE: `finalize_batch` memanggil `await context.bot.send_chat_action(chat_id, ChatAction.UPLOAD_DOCUMENT)` SEBELUM `archive_new_product`. Saat koneksi ke Telegram putus (ReadError), exception naik ke `except` block → `archive_new_product` TIDAK pernah dijalankan → file gak tersimpan. Koneksi putus ini sering terjadi karena `apscheduler` job "missed by 5:33" (event loop lag) lalu neken saat network flaky.
FIX (terbukti):
- **HAPUS `send_chat_action`** dari `finalize_batch` (itu bukan prasyarat arsip).
- Bungkus `send_message` balasan ke user jadi **best-effort** — arsip tetap jalan walau Telegram error:
  ```python
  try:
      result = await asyncio.to_thread(self.archive.archive_new_product, session.draft, session.files)
      message = f"Produk berhasil diarsipkan.\nProduct ID: {result['product_id']} ..."
      try:
          await context.bot.send_message(chat_id, message)
      except Exception:
          logger.warning("gagal balas ke user, tapi arsip sukses")
  except Exception as exc:
      logger.exception("archive failed")
      try:
          await context.bot.send_message(chat_id, f"Pengarsipan gagal: {exc}")
      except Exception:
          pass
  ```
- Verifikasi: setelah fix, kirim file → 60dtk → cek Drive `Celine Arsip/2026-08/` ada folder PROD-* baru. JANGAN cuma lihat reply bot — reply bisa gagal tapi arsip sukses.

## DIAGNOSA "GATEWAY OFFLINE" (2026-08-16)
Bos bilang "gateway offline" — cek urutan:
1. `Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*ziyan_bot.bot*' }` → hitung instance. **>1 instance = orphan conflict** → Telegram `Conflict: terminated by other getUpdates request` / `getUpdates` return `[]` → bot gak receive = "offline" di mata Telegram. Kill all, launch 1.
2. `curl -s -m5 http://localhost:20128/health` (9Router) → `200` = online. 9Router mati bikin model/vision gagal, tapi BUKAN penyebab bot offline.
3. `curl -s -o /dev/null -w "%{http_code}" http://localhost:5678/` → `000` = n8n mati (expected, jangan start).
4. Jangan salah diagnosis: bot "offline" hampir selalu = orphan instance, bukan token mati (token sudah divalidasi 15 Agust). Kill orphan dulu SEBELUM cek token.

## BOS SPEC 2026-08-16: SIMPAN FILE SELALU, LINK HANYA JIKA ADA
Aturan keras Bos (final, setelah debug bot mati):
- **Bot SELALU simpan file yang dikirim** — jangan tolak walau gak ada caption/link.
- **Link/deskripsi HANYA dicatat kalau ada** di caption. Kalau gak ada → produk dibuat dengan `title="Tanpa judul"`, link kosong.
- **Skenario 4 file + 1 link (dalam 1 menit):** ke-4 file dikumpulkan jadi 1 produk, dicatat berdasarkan 1 link itu. Caption cukup ada di 1 file saja (sisanya tanpa caption), parser tetap pakai draft dari caption pertama yang muncul di batch.
- **Implementasi (`bot.py` `finalize_batch`):** HAPUS penolakan `if session.mode=="new" and not session.draft: return`. Ganti dengan auto-draft default:
  ```python
  if session.mode == "new" and not session.draft:
      session.draft = ProductDraft(title="Tanpa judul", description="", shopee_url=None, tiktok_url=None, other_links=[])
  ```
- **Batch window = 60 dtk** (`BATCH_WINDOW_SECONDS=60` di `.env`) — "1 menit" Bos.
- Bukti E2E (test script): 4 file (1 caption link + 3 tanpa caption) → Sheet `PROD-...` dengan 4 aset, 1 link Shopee tertulis. Lihat `references/bot_end_to_end_test.md` (function `test_bos_spec`).

## CLEANUP GHOST/TEST DATA (NEW 2026-08-16)
E2E test scripts (test_full_chain.py, test_bos_spec.py) write **REAL data** into Bos's Drive + Sheets. After debugging, 6 ghost folders (`PROD-20260816-*`) accumulated → Bos noticed and asked to purge. **Prevention = discipline, not luck:**
- Every test script that archives MUST clean up its own output (delete test folders from Drive trash + strip Sheet rows) at end, OR point at a dedicated test folder ID + test spreadsheet (set `GOOGLE_ROOT_FOLDER_ID` / `GOOGLE_SPREADSHEET_ID` override inside the script).
- Bos monitors his Drive personally — leftover test artifacts erode trust.

**Identify ghost vs real (procedure in `references/cleanup_test_data.md`):**
- List `2026-08` folder. Test data = today's date prefix (`PROD-20260816-*`); real = earlier (`PROD-20260815-*`).
- Confirm by contents: REAL folders have actual `telegram_XX.jpg/.mp4` from Bos's phone + `PRODUCT_INFO.txt` + `AFFILIATE.json`. TEST folders have dummy PNGs / captions like `KAOS TEST`, `FULL CHAIN TEST`.
- Purge: `drive.files().delete(fileId)` → goes to **trash (reversible 30d)**. Then strip Sheet rows matching `^PROD-20260816-` from PRODUCT_MASTER + CONTENT_ASSETS (clear range, rewrite keep-rows).
- NEVER permanently delete Bos's real 15-Aug products.

## ANTI-LOOP PROTOCOL (CORE DIRECTIVE BOS, 2026-08-15)
Bos keluar dari loop debugging dengan marah ("bodoh", "mutar-mutar", "cari tutorialnya anjing"). Embed sebagai rule wajib:
1. **Anti-Loop & Self-Critique:** Jika error SAMA (misal 404) muncul >2x berturut-turut → HENTIKAN asumsi awal. Jangan langsung simpulkan API corrupt. Cek ulang: (a) ID benar & sinkron? (b) env vars sesuai? (c) filter internal bot yg blokir?
2. **Chain of Thought runut:** Verifikasi input → alur eksekusi → hasil. JANGAN lompat ke kesimpulan kompleks (channel corrupt, ghost admin) sebelum hal dasar (salah ID, salah format) tervalidasi.
3. **Context Saturation:** Kalau log penuh error berulang & stuck → STOP debat. Minta Bos reset riwayat / kirim 1 log bersih dari nol. Jangan nebak terus.
4. **Bos-benci-suruh-manual:** "kau atur lah" = delegasi penuh. Jangan suruh Bos klik UI/setting berulang. Cari jalan teknis (bypass, bot object, auto-detect) sehingga Bos gak perlu mutar.

## Distribusi end-to-end (proven 2026-08-15)
- `distributor.gen_caption()` → 9Router (Bearer `HERMES_CUSTOM_9ROUTER_API_KEY`, SSE parse) → caption natural Celine Aurel tanpa harga.
- Command: Bos kirim PM ke bot `/distribusi PROD-XXXXXX all` → bot generate → `context.bot.send_message(chat_id=CHANNEL_CELINE, text=caption)` → post ke channel.
- `CHANNEL_CELINE=-1004373452633` di env bot. FB Page token valid (`FB_PAGE_TOKEN` dari `OneDrive/ziyan_pending/fb_page_token.txt`, page "Celine Aurel" id 975723622288353).
- YouTube Celine = proyek terpisah (token `youtube_token_celineaurel.json` valid, channel `UC8Lzhi5_SvJZcecD79xIiog`). Compound Daily = proyek lain lagi (token hilang = blocker).
