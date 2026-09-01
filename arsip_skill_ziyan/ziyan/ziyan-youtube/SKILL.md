---
name: ziyan-youtube
description: Setup OAuth & otomasi upload YouTube ZIYAN Compound Daily.
---

# ZIYAN YouTube — Channel "Compound Daily"

## Fakta Channel (terverifikasi 1 Aug 2026)
- Akun: `mziyan266@gmail.com` (akun ZIYAN) — punya BANYAK channel (brand accounts): Ziyan Malik, Compound Daily, ClayCaper, Arijal Meutuwah, 4K Scenic Wildlife, Compound Daily, TinyRealm Builds, Se Ruang Konspirasi, The Visually Satisfying
- **Target resmi (REVISI 1 Aug 2026): "Ziyan Malik"** (`UCend05oI081uEVPTNa934Bg`, 61 subs, 57K views) — dipilih Bos setelah konfirmasi "semua itu milikku" & token `youtube_token.json` terikat channel ini (HTTP 200 terverifikasi via `channels?mine=true`).
- **Compound Daily** (@CompoundDaily-v7c, `UCzWib2-2CPkWo315fzucaUw`, 0 subs) TIDAK dipakai — hanya disebut di sesi awal sebelum Bos pilih Ziyan Malik.
- Niche: **Tech / AI / Business / Finance** (4-in-1, rotasi topik harian), bahasa **Inggris**, target internasional

## Multi-Channel dalam 1 Akun (PELAJARAN KRITIS — 1 Aug 2026)
- `channels?mine=true` HANYA mengembalikan **1 primary channel** (yang aktif saat ini), BUKAN semua channel di akun.
- **Token terikat ke channel yang AKTIF saat consent OAuth**, bukan ke seluruh akun.
- Maka: **tiap channel tujuan butuh token TERPISAH**, di-generate saat channel itu yang aktif di layar consent.
- Verifikasi WAJIB setelah tukar token: panggil `mine=true` & cek `BOUND CHANNEL` = target. Kalau salah (misal dapet Ziyan Malik padahal mau Compound Daily) → ulang OAuth dari session di mana channel target aktif.
- Tidak bisa ganti channel token tanpa ulang OAuth (token sudah terikat). Atau di YouTube Studio jadikan target sebagai primary lalu re-auth.

### File token per channel (ziyan_credentials/)
- `youtube_token.json` → **Ziyan Malik** (`UCend05oI081uEVPTNa934Bg`) ✅ BOUND & terverifikasi HTTP 200 (1 Aug 2026). INI token utama operasional.
- `youtube_token_compound.json` → Compound Daily (`UCzWib2-2CPkWo315fzucaUw`) — ada di disk tapi channel itu TIDAK dipakai. Jangan kirrau dengan token utama.
- Tambah `youtube_token_<nama>.json` untuk channel lain bila perlu.

## Jadwal (perintah Bos)
- **Shorts**: 3x/hari — prime time US: 18:00 / 00:00 / 06:00 WIB (EST 06:00/12:00/18:00)
- **Long-form**: 3x/minggu (Selasa/Kamis/Sabtu), prime time US
- Bahasa: Inggris. Sumber utama: **NotebookLM** (video), cadangan mass: 9router + edge-tts + ffmpeg

## Pipeline Produksi — Jalur A: NotebookLM (UTAMA, wajib)
Alur (SESUAI KOREKSI BOSS 2026-08-04 — agen yang cari topik, BUKAN Boss):
1. **AGEN riset topik trending** di X/Twitter + perkembangan AI terbaru (delegate RISA, sumber reliable: Hacker News, Ars Technica, The Verge, HF papers — JANGAN Trends24 Indonesia yang tidak relevan). Pilih 1 topik paling hot & relevan niche ZIYAN.
2. **AGEN cari 10 sumber terpercaya** (URL valid 200, beragam sudut pandang: official, tech news, GitHub, Reddit, YouTube, comparison). VERIFIKASI tiap URL via `curl -o /dev/null -w "%{http_code}"` — JANGAN terima URL `...` terpotong (halu).
3. **AGEN inject 10 URL** ke NotebookLM via CLI.
4. **AGEN generate 8 artefak** (video explainer 16:9 LONG only, audio, slide-deck, infographic, report, data-table, mind-map, quiz).
5. Download ke `ziyan_artifacts/<nama>/`. Video LONG saja (Boss bikin Short di HP).
6. Upload YouTube (Long) + Blogger + distribusi Telegram/X/LinkedIn.
NOTE: Boss TIDAK kasih keyword — agen yang inisiatif cari trending. Tapi tugas system-heavy (generate video/quota) tetap butuh persetujuan strategis Bos sebelum eksekusi.

### Jalur Mandiri (agent 100% tanpa Bos pegang browser) — `notebooklm-py`
- `notebooklm-py` (v0.7.3, PyPI, MIT) = unofficial API via RPC `batchexecute`. **TERVERIFIKASI** ada & CLI jalan (cek 1 Aug 2026).
- **VERIFIED COMMANDS (2026-08-04, venv `C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m notebooklm`)**: `notebooklm create "Nama"` (ambil ID dari `notebooklm list`; TIDAK ada subcmd `notebooklm notebook create`); `notebooklm source add --type url -n <ID> <URL>` (ulangi per URL, `sleep 2` antar inject — too fast = rate-limit); `notebooklm generate video|audio|slide-deck|infographic|report -n <ID> "prompt"` (returns task ID); `notebooklm generate data-table -n <ID> "DESC"` (positional, BUKAN `--description`); `notebooklm generate mind-map -n <ID> --kind interactive` (TIDAK terima prompt positional); `notebooklm artifact wait <TASK> -n <ID> --timeout 100`; `notebooklm download <type> -n <ID> <OUT_PATH>` (positional, bukan `--output`); `notebooklm source list -n <ID> --no-truncate`. **TIDAK ADA** `notebooklm source add-research`, `notebooklm download video --latest`, `--title`.
- **VIDEO FORMAT VERIFIED 8/3**: CLI `--format` HANYA `explainer`(16:9) / `brief` / `cinematic`(Veo3). **TIDAK ada `short`** — argumen `short` ditolak ("'short' is not one of 'explainer','brief','cinematic'"). Format vertikal 9:16 "Short" ADA di **MOBILE APP NotebookLM** (generate di HP), bukan CLI. Format vertikal 9:16 "Short" ADA di **MOBILE APP NotebookLM** (generate di HP), bukan CLI. **SHORTS — ATURAN BOSS (2026-08-04, OVERRIDE crop)**: **JANGAN crop** explainer jadi 9:16. Agent HANYA download video LONG (16:9). Boss yang generate native Short di HP lalu kasih balik ke agent. Ffmpeg crop DINYATAKAN DEPRECATED untuk ZIYAN.
- **FREE TIER LIMIT (FAKTA Bos 8/3)**: MAX **3 Video + 3 Audio Overview PER HARI**. Scale butuh Google AI Ultra/Workspace. JANGAN percaya estimasi "20-30/hari".
- **JANGAN computer_use klik UI NotebookLM** — Google blokir ("browser not secure"). Semua via CLI.
- **Login 1x (Bos manual, Windows)**: `notebooklm login --fresh` (launch Chromium, Bos login `mziyan266@gmail.com`, tutup jendela). Cookie tersimpan `~/.notebooklm/profiles/default/storage_state.json`.
  - **JANGAN pakai `--browser-cookies brave|chrome`** → gagal "Could not decrypt ... cookies" (rookiepy tdk bisa DPAPI Brave/Chrome Windows). Pakai `--fresh`.
  - **JANGAN tutup jendela sebelum login selesai** → "browser window was closed during login" → ulang `--fresh`.
- **Install (WAJIB ke venv Hermes, bukan Python sistem)**:
  `set VIRTUAL_ENV=C:\Users\arija\AppData\Local\hermes\hermes-agent\venv` lalu `uv pip install "notebooklm-py[browser]"` + `python -m playwright install chromium`.
  - `uv pip install --python <path-exe> <pkg>` GAGAL di Windows (uv tdk kenali venv dari path exe). Pakai env var `VIRTUAL_ENV`.
- **Caveat**: unofficial = risiko ToS/rate-limit; cookie = kredensial sensitif (simpan di disk lokal, jangan ke chat). Pin versi `notebooklm-py==0.7.3`. Kalau RPC patah → fallback Playwright / Veo Vertex.
- Detail + recipe: `references/notebooklm_py_automation.md`.

## Pipeline Produksi — Jalur B: Lokal cadangan (mass/gratis, TIDAK utama)
- edge-tts **GAGAL** di proxy ini (SSL error); 9router TTS **502** (model invalid). Jalur B sedang rusak — jangan andalkan.
- Bila jalan: Script → TTS → Gambar (`gen_img.py` → `ag/gemini-3.1-flash-image`) → ffmpeg gabung.
- `gen_img.py` di `C:\Users\arija\gen_img.py` (butuh `HERMES_CUSTOM_9ROUTER_API_KEY`).

## Upload ke YouTube (WAJIB via Data API, BUKAN yt-dlp)
- yt-dlp **TIDAK punya flag `--upload`** (error "no such option: --upload"). Pakai **YouTube Data API resumable**:
  `POST /upload/youtube/v3/videos?uploadType=resumable&part=snippet,status` → PUT bytes ke `Location`.
- Token: `upload_pipeline.py` (skrip operasional batch) HARDCODE membaca
  `ziyan_credentials/youtube_token.json` — BUKAN `youtube_token_compound.json`.
  Maka re-auth/upload APA PUN channel target harus regenerate file **`youtube_token.json`**
  (dengan `refresh_token` + scope `youtube.upload`), agar `upload_pipeline.py` bisa jalan.
  Catatan lama yg rujuk `youtube_token_compound.json` sudah usang & tidak cocok dgn skrip.
  SELALU verifikasi `BOUND CHANNEL` via `channels?mine=true` sesudah tukar token.
- Privacy: `private` dulu (Bos review), lalu publish.
- **Jadwal terjadwal (bukan serentak)**: `status.privacyStatus="private"` +
  `status.publishAt` RFC3339 UTC (`%Y-%m-%dT%H:%M:%SZ`). Acak jamnya & simpan
  `last_scheduled` di state file supaya batch tidak rilis bersamaan.
- **Guard channel WAJIB** sebelum upload: `channels?part=snippet&mine=true`,
  abort kalau judul channel bukan target. Akun ini multi-channel — tanpa guard,
  video bisa nyasar.
- **Pipeline batch siap pakai**: `C:\Users\arija\ziyan_drive_learn\upload_pipeline.py`
  (scan → compress 48k mono → upload → jadwal random, default DRY-RUN).
  Detail & cara tes: `references/upload_pipeline.md`.
  Pola off-window cron (riset+staging saat jendela tutup): `references/compound-daily-pipeline-state.md`.
- **KOREKSI binding token (verifikasi 2026-08-02)**: `youtube_token.json` sekarang
  balik `Compound Daily` dari `mine=true` (bukan Ziyan Malik seperti catatan
  1 Aug). Binding token BISA berubah setelah re-auth — SELALU cek `mine=true`
  saat itu juga, jangan percaya catatan lama.

## Setup OAuth — PITFALL KRITIS (baca references/youtube_oauth.md + references/youtube_oauth_403.md)
- **JANGAN pakai client tipe WEB** untuk script upload — `urn:ietf:wg:oauth:2.0:oob` DITOLAK ("must contain a domain")
- **Pakai client tipe DESKTOP/Installed app** → redirect `http://localhost` (sudah valid)
- File client Desktop ZIYAN: `C:\Users\arija\ziyan_credentials\youtube_desktop_client.json` (project `lofty-layout-504106-n4`)
- Flow: generate URL → Bos buka & login `mziyan266` → Allow → copy `code=` dari address bar → tukar jadi refresh_token (simpan lokal, TIDAK lewat chat)
- **Error 403 `access_denied`** — DUA penyebab, bedakan dari status consent screen:
  - **(A) App External + TESTING** + email BELUM masuk Test Users → FIX: OAuth consent → Test users → + ADD `mziyan266@gmail.com` → SAVE, lalu re-auth. Token Testing expire **7 hari**.
  - **(B) App External + PRODUCTION** (status Benar!) tapi scope `youtube.upload` = **RESTRICTED** → Google TETAP tolak HARD 403 kecuali lewat tombol "unverified". FIX: di layar error/consent, klik **Advanced** (kiri bawah) → **Go to agent youtube (unsafe)** → Allow. Setelah itu redirect & dapet `code=`. Production = refresh_token TIDAK expire 7 hari. INI yang terjadi 1 Aug 2026 — bot salah diagnosis sebagai Test User padahal sudah Production.

## Monetisasi (baca references/youtube_monetization.md)
- YPP butuh 1000 subs + 4000 jam TAYANG (atau 1000 subs + 10jt Shorts views). Shorts watch-time di feed TIDAK hitung ke 4000 jam.
- Jalur <30 hari: (1) Affiliate (hari-1), (2) Patreon/Ko-fi (mgg-1), (3) Funnel ke AI Service Agency (mgg-2)
- Wajib disclosure affiliate & penggunaan AI. JANGAN reuse-content / AI-spam (reused/inauthentic = no monetization)

## Prinsip Keamanan
- refresh_token & client_secret → hanya di `ziyan_credentials/` lokal. JANGAN tempel ke chat.
- Bos ambil auth code lewat browser sendiri; agent tukar code → token (token tidak pernah di-print ke chat)

## Blog ZYN AI co (Blogger autopost — hasil 1 Aug 2026)
- Blog: **ZYN AI co** → `https://ziyancorp.blogspot.com/` (Bos buat via UI Blogger.com; **TIDAK bisa via API** — `blogs.insert` tidak ada di Blogger API v3).
- OAuth: scope `blogger` DITAMBAHKAN ke URL consent bersama `youtube.upload`+`youtube.readonly` → 1 token gabungan (`youtube_token.json` sudah punya scope blogger, terverifikasi).
- **Blogger API v3 WAJIB di-enable manual** di GCP Console (`blogger.googleapis.com`) — tidak bisa via API tanpa scope `cloud-platform`. Link enable: `https://console.developers.google.com/apis/api/blogger.googleapis.com/overview?project=789747689443`
- Blog ID diambil via `GET users/self/blogs` (butuh token blogger) — jangan panggil `byurl` tanpa API key (403).
- Posting: `POST /blogger/v3/blogs/{blogId}/posts` (body: `kind, title, content`). Draft dulu (`isDraft:true`) lalu `posts.publish`.
- **JADWAL autopost**: ≤1 artikel/hari (aman dari AdSense scaled-content-abuse/NOV per riset `ziyan_blogspot_adsense_riski.md`).
- **ANTI-NOV**: artikel HARUS pakai data orisinal ZIYAN (`ZIYAN_COMPANY_LOG.md`, `ziyan_riset_*.md`, `ziyan_audit_nbproof.md`) — JANGAN rekap info umum/web. Wajib AI disclosure.
- Draft contoh: `ziyan_blog_draft_01.md` (angle: "We tested 15 free AI image models — only 1 worked", semua angka dari tes nyata).

## CHANNEL CELINE AUREL — STATUS FINAL (2026-08-07, AKHIR SESI)
- **Channel BARU dibuat**: `UC8Lzhi5_SvJZcecD79xIiog` ("Celine Aurel") = channel utama akun `mziyan266@gmail.com` (Bos pilih "buat channel baru aja" setelah lihat tidak ada opsi Owner di channel lama `UCzY1VDdRBSpDDHzBn_NcSLg`).
- **TOKEN BENAR**: OAuth diulang (Incognito, akun manager) → `channels?mine=true` balik `('Celine Aurel','UC8Lzhi5_SvJZcecD79xIiog')` ✅. Token `ziyan_youtube_token.json` field `channel_id=UC8Lzhi5_SvJZcecD79xIiog`, refresh token tersimpan (tidak expired).
- **UPLOAD TEST SUKSES**: lewat OAuth user token → video masuk ke channel Celine Aurel (`youtube.com/shorts/<id>`).
- **SA TIDAK DIPAKAI** upload (401 youtubeSignupRequired ke channel biasa). SA `ziyancorp` file `ziyan_google_service_account.json` = cadangan dokumentasi saja.
- **NODE YOUTUBE di n8n**: belum dipasang (workflow batal import karena connection mismatch — lihat `ziyan-n8n-workflow-builder` FIX). Setelah import ulang: tambah node HTTP POST video ke Data API pakai token `ziyan_youtube_token.json` + `channel_id=UC8Lzhi5_SvJZcecD79xIiog` + `privacyStatus: public` (atau private dulu).
- **URL AUTHORIZE** (installed client `3131524149-2ek5m9fg8o60p78bl8b1a546m7aj5o19`): `https://accounts.google.com/o/oauth2/v2/auth?client_id=3131524149-2ek5m9fg8o60p78bl8b1a546m7aj5o19.apps.googleusercontent.com&redirect_uri=http://localhost&response_type=code&scope=https://www.googleapis.com/auth/youtube.upload%20https://www.googleapis.com/auth/youtube&access_type=offline&prompt=consent`

## PITFALL KRITIS — UPLOAD SELALU KE DEFAULT CHANNEL AKUN
- Upload via OAuth user token SELALU ke channel UTAMA/aktif akun saat consent, bukan channel yang kita mau kecuali itu default.
- `channels?mine=true` HANYA balik 1 primary channel (yang aktif). Tidak bisa pilih channel saat `videos.insert`.
- MAKA: sebelum upload, PASTIKAN `mine=true` balik channel TUJUAN. Kalau salah → DELETE video (`videos().delete`) + ulang OAuth dari session di mana channel target = default/aktif.
- JANGAN paksa SA upload (401). JANGAN transfer ownership (tidak ada opsi di channel pribadi).

## Channel Manager via SERVICE ACCOUNT — GAGAL UPLOAD (KOREKSI 2026-08-07)
- Channel CELINE AUREL (lama `UCzY1VDdRBSpDDHzBn_NcSLg`, BARU `UC8Lzhi5_SvJZcecD79xIiog`) BUKAN akun utama ZIYAN — Bos di-invite sebagai manager.
- **SA TIDAK BISA UPLOAD**: `videos().insert` pakai SA `apikey@ziyancorp.iam.gserviceaccount.com` → `401 youtubeSignupRequired`. YouTube hanya izinkan SA via CMS/Brand Account terverifikasi. SA tidak dipakai untuk upload (enable API + invite Manager sudah dilakukan, tetap 401).
- **SOLUSI JALAN = OAuth User Token** dari akun manager. Token `ziyan_youtube_token.json` (channel_id=`UC8Lzhi5_SvJZcecD79xIiog`), upload test SUKSES. Refresh token tersimpan.
- SA file `ziyan_google_service_account.json` simpan cadangan dokumentasi saja, JANGAN pakai upload.
- **NOTE GRATIS**: SA ziyancorp = GRATIS buat YouTube upload (quota 10rb unit/hari). TAPI TIDAK bisa ke channel biasa (cuma CMS). Jangan pasang ke Vertex AI (bayar setelah $300 credit habis).

## Pitfalls (TAMBAHAN 1 Aug 2026)
- **YT TITLE LIMIT = 100 char.** Di sesi 16/8, upload gagal HTTP 400 "invalid or empty video title" karena title produk 185 char. FIX di `youtube_upload_celine.py` / `distribute_agent.py`: `title = title[:95].rsplit(" ",1)[0]+"..."`. Description jangan pakai caption IG/Threads (bisa reject) — pakai description simpel. Timeout subprocess naikkan 600s (video 10MB butuh >180s di network lambat).
- **HALUSINASI ASET (KOREKSI BOS)**: JANGAN klaim aset di disk ("channel terhubung", "token milik kita") tanpa (a) bukti tool nyata (HTTP 200, `mine=true`) DAN (b) konfirmasi asal ke Bos. Token/channel bisa berasal dari setup Bos di Hermes Desktop instance lain — agent Discord TIDAK berbagi memory dgn instance lain, hanya berbagi file disk. SELALU sebut batas kejelasan ("saya tidak tahu milik akun mana") sebelum simpulkan. Cross-ref `ZIYAN_COMPANY_LOG.md`.
- **Vision gagal** (vision_analyze 404 di model free/tencent-hy3): JANGAN minta Bos kirim screenshot berulang. Verifikasi via API/terminal (channels?mine=true, users/self/blogs, os.path.exists). Lihat skill `image-verification-fallback`.
- **Multi-channel trap**: `mine=true` cuma return 1 channel (primary aktif). Token terikat channel saat consent. Untuk Compound Daily butuh token terpisah (`youtube_token_compound.json`), bukan reuse token Ziyan Malik. SELALU verifikasi `BOUND CHANNEL` setelah tukar token.
- Error `redirect_uri_mismatch` = URI belum terdaftar di GCP Console ATAU salah tipe client (web vs desktop)
- 9router `gemini/*` channel MATI (401 key invalid di proxy) — pakai `ag/gemini-3.1-flash-image`
- Vision service (vision_analyze) sering 404 di sesi ini — fallback ke terminal/python untuk cek file (lihat skill `image-verification-fallback`)
- **URL SUMBER HALU (2026-08-04)**: Sub-agent RISA sering return URL `...` terpotong (YouTube `watch?v=...`, Ars `arstechnica.com/ai/...`) = TIDAK valid. SELALU verifikasi dengan `curl -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" <URL>` (200/301=oke, 404/000=buat). Cari 10 sumber valid via DuckDuckGo HTML (sering kosong/block → fetch langsung domain: HF, GitHub API `api.github.com/search/repositories`, minimaxi.com/news). Jangan lanjut inject sumber sampah.
- **9ROUTER LAUNCHER (2026-08-04)**: binary di `C:\Users\arija\AppData\Roaming\npm\9router`. Jalankan `9router -p 20128 -H 127.0.0.1 -t --skip-update` (tray mode, background). Cek `netstat -an | grep :20128` = LISTENING. Models: channel-researcher, openrouter, claude-gratsi. Provider untuk SUB-AGENT (bukan Parent/nous). Secret bocor ke Windows User Env Var (shell eksekusi isi env sebagai command) — simpan di `ziyan_keys.env` saja.
- **BLOGGER TOKEN (2026-08-04)**: `youtube_token_ziyanmalik.json` SUDAH punya scope `blogger` + refresh_token. Refresh pakai `youtube_desktop_client.json` (client_id `789747689443-qk9ns...`). Blog `ZYN AI corp` ID `598320500315317650` (ziyancorp.blogspot.com). Upload `POST /blogger/v3/blogs/{id}/posts`. JANGAN embed base64 image >~1MB (400 error) — pakai URL eksternal (YouTube thumbnail) sebagai cover sementara.
