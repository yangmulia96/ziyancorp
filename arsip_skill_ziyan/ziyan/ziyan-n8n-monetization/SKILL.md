---
name: ziyan-n8n-monetization
description: "ZIYAN cuan via n8n: template + jasa workflow."
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
platforms: [windows, linux, macos]
---

# Monetisasi n8n untuk ZIYAN

n8n = workflow builder no-code (node visual, trigger eksternal). Berbeda dengan Hermes (LLM-agent
yang mikir). ZIYAN pakai **n8n = OTOT** (mesin produksi/eksekusi), **Hermes = OTAK** (riset,
naskah, strategy, QC).

## Kapan pakai
- Bos: "cari cara cuan", "template n8n", "jual workflow", "faceless channel otomatis".
- Butuh alur deterministik berulang (upload massal, generate video dari sheet, lead-gen).

## TEMUAN PASAR (riset 2026-08-02, `ziyan_riset_n8n_cuan.md`)
Uang terbesar = **JASA**, bukan konten:
| Model | Pendapatan |
|---|---|
| Workflow n8n (freelance/agency) | $150-2.000/proyek, retainer $200-1.500/klien/bln (margin 85-95%) |
| Faceless YouTube (n8n) | $6-15/bln (gratis) s.d $150-250/bln (premium API) |
| Lead-gen B2B | $0.20-2/lead, sistem $1.500-5.000, retainer $1.000-3.000/bln |
| AI CS UMKM (ID) | Rp 3-10jt setup + Rp 500k-2jt/bln |
| Content-as-a-Service | langganan buat klien punya channel faceless |

## TEMPLATE n8n PALING DICARI (prioritas ZIYAN)
1. **AI agent auto-reply WhatsApp/IG** (UMKM) — node: webhook → LLM → send
2. **YouTube faceless pipeline** — Google Sheets → script (OpenAI) → TTS (ElevenLabs) → BGM
   (Suno) → render (JSON2Video) → upload YouTube API
3. **Lead gen LinkedIn/Upwork** — scrape → filter → draft proposal → notify

## TEMPAT JUAL
- Gumroad, n8n.io community templates, ProductHunt, grup FB, X/Twitter
- Template gratis = lead magnet ke jasa (upsell retainer)
- Harga: template $5-50, jasa $150-2.000

## CARA BUAT
- n8n self-host **GRATIS** (Community edition, `n8n start` via Docker/`npx n8n`)
- Butuh: drag-drop node, HTTP node, JS/Python code node, API integration
- 1 template = beberapa jam (bergantung kompleksitas)
- Jalur gratis TETAP cuan: n8n self-host + Gemini free + Edge-TTS + Pexels/Pixabay + FFmpeg + YT API

## INSTALL n8n DI LAPTOP (WINDOWS, TANPA DOCKER)
- **Tidak butuh Docker.** Docker cuma opsional (production/isolasi). Untuk RAM 8GB, npm langsung LEBIH BAIK.
- Prasyarat: Node.js v18+ (Bos v24 ��� **INKOMPATIBEL** — n8n 2.33 crash senyap). Cek: `node --version`
- **FIX NO-ADMIN (terbukti 2026-08-10)**: Download **Node 22.22 LTS portable ZIP** side-by-side:
  ```bash
  curl -L -o node22b.zip "https://nodejs.org/dist/v22.22.0/node-v22.22.0-win-x64.zip" && unzip -q node22b.zip -d node22b
  ```
  Path node: `C:\\Users\\arija\\node22b\\node-v22.22.0-win-x64\\node.exe`
- Install n8n global: `npm install -g n8n` (pakai Node 22)
- Jalankan: `n8n start` (background) → buka `http://localhost:5678`
- Port default 5678. Cek: `curl localhost:5678/healthz` → `{"status":"ok"}`
- **VERIFIKASI WAJIB**: `netstat -ano | findstr 5678` HARUS ada LISTENING. `curl -s -o /dev/null -w '%{http_code}' localhost:5678/healthz` HARUS 200.
- **DISIPLIN**: Agent TIDAK start n8n. Bos buka **cmd.exe Windows asli** → `n8n start` → biarkan jalan. Agent cek `curl localhost:5678/healthz` dari terminal sendiri. Setelah Bos bilang "sudah nyala", agent langsung API import/activate/test.
- Jika agent TERPAKSA start: pakai `N8N_PORT=5679` untuk hindari conflict dengan instance Bos.
- Simpan `start-n8n.bat` di Startup folder + copy di Desktop untuk akses cepat Bos.

## IMPORT WORKFLOW (hindari klik UI)
**PENTING (2.33.4): REST `/api/v1/workflows` TIDAK enable default** — balas `Cannot POST /api/v1/workflows` walau API key benar. CLI `n8n import:workflow` juga FAIL (`SQLITE_CONSTRAINT id NOT NULL` karena node string id).
**Jalur andal = insert langsung ke SQLite** `~/.n8n/database.sqlite` tabel `workflow_entity` (id=UUID, versionId=UUID, nodes/connections=JSON string, STRIP field `id` tiap node). Detail + perintah: `references/n8n-shopee-deployment.md`.
- API key (kalau perlu): insert `user_api_keys` (apiKey=sha256(raw)), restart n8n.
- Env var workflow `{{ $env.X }}`: tabel `settings` key=`env` (JSON), restart n8n.
- Workflow import `active:false` → set `active=1` di DB atau aktifkan manual di UI.
- Setelah insert/manipulasi DB: **restart n8n** (`cmd.exe /c "taskkill /F /PID <pid>"` lalu `n8n start`) agar kebaca.

## AUTOMATION INSTAGRAM (IG Auto-Post via n8n)
- Node: Schedule → Set Data → HTTP Request (Graph create media) → HTTP Request (publish)
- Endpoint: `POST graph.facebook.com/v19.0/{IG_USER_ID}/media` (body: image_url+caption)
  lalu `POST .../{IG_USER_ID}/media_publish` (body: creation_id)
- Credential: env `IG_ACCESS_TOKEN` + `IG_USER_ID` (atau n8n Credentials "Facebook Graph API")
- Template: `ziyan_n8n_templates/ig_auto_post.json` (sudah diimport n8n id `8l9YDltPLU9GOD7R`)
- Panduan token: `ziyan_n8n_templates/IG_TOKEN_GUIDE.md`
- Syarat: IG Business/Creator + terhubung Facebook Page
- Token: short-lived (1j) → exchange long-lived (60h) via OAuth endpoint (app_id+secret)

## BIAYA OPERASIONAL (faceless channel, per bulan)
- Gratis: ~$0 (stack di atas)
- Standar: $55-80 (ElevenLabs $5 + Suno + JSON2Video $17 + API lain)
- Premium: $150-250 (Veo/FAL video gen)
- JSON2Video: free 600 kredit (watermark) · $16.95/bln=3.000 kredit (1 kredit=1 detik video)
- ElevenLabs: $5 Starter / $22 Creator / $99 Pro

## RISIKO (hubungkan ke riset Inauthentic Content Policy)
- YouTube cabut YPP (Jul 2025) untuk pola template generik / overposting / slideshow statis
- Wajib: nilai tambah di level naskah + QC (Judge agent) + upload random (bukan serentak)
- TTS berisiko demonetisasi (ElevenLabs) → pakai Google TTS / voice asli

## REKOMENDASI ZIYAN
Prioritas monetisasi (dari riset):
1. **AI CS UMKM** (Jalur 1, paling cepat cuan, Rp jutaan/bln)
2. **Jasa workflow n8n + retainer**
3. **Content-as-a-Service** (bikin channel buat klien)
4. **Channel sendiri** = lead magnet, BUKAN pusat laba

## PITFALL
- Jangan buru-buru harap cuan dari YouTube (Adsense 3-6 bln, RPM rendah $1.5).
- n8n bukan pengganti Hermes untuk reasoning — pakai bersama.
- Template gratis boleh, tapi jangan jadi konten spam (kena Inauthentic Policy).
- **JANGAN auto-post ke platform berbayar tanpa approval Bos.** Kasus nyata: Twitter/X ngabisin saldo API tapi postingan tidak jelas → Bos suruh hapus (`~/.x_credentials` dikosongkan, token dihapus dari `ziyan_keys.env`). Setelah itu tidak ada tweet otomatis tanpa perintah eksplisit. Terapkan ke X, IG (Meta Graph API token 60-hari habis → butuh refresh manual), semua channel berbayar.
- **Skill/konten yang cuma "generate teks" = redundant.** Bos sudah punya Hermes + 9router + Gemini Spark untuk teks. Jangan tawarkan skill generator kalau tidak ada aksi nyata (koneksi app, publish, workflow). Bos: "cuma buat teks udah punya".
- **Bedakan atribusi tool.** Hermes (orkestrator), Gemini Spark (skill-based Workspace agent: Gmail/Drive/YouTube/TikTok UGC). Salah sebut = Bos marah ("bukan... itu dari Gemini Spark").
- **Antigravity BUKAN app terpisah yang tidak bisa saya pakai.** Model Antigravity (`ag/*`) muncul di 9Router Proxy dashboard (sidebar Providers → Antigravity, akun `mziyan266@gmail.com`) dan **BISA dipanggil langsung** via `POST http://127.0.0.1:20128/v1/chat/completions` dengan `model: ag/...` (sudah tested: `ag/gemini-3.6-flash-medium` buat vision jalan). Jangan ulang kesalahan "Google Antigravity aplikasi terpisah di laptop, saya tidak bisa akses" — itu SALAH. 9Router proxy = jembatan ke semua model itu. Katalog lengkap + kehebatan tiap model: `references/9router_antigravity_models.md`.
- **STYLE: jangan terlalu teknis ke Bos.** Sinyal nyata: Bos bilang "aku gak paham itu" saat dijelaskan node chain / endpoint detail. Strategi: beri ringkas "apa yang sudah jalan + apa yang harus Bos lakukan" (tabel/bullet), sembunyikan detail node ke skill reference. Bos mau eksekusi, bukan arsitektur.
- **Sub-agent QC tidak bisa diandalkan** — selalu verifikasi hasil sub-agent sendiri (kasus nyata: QC nyasar baca `.gemini/antigravity`, workflow builder salah URL + salah bahasa kode). Orkestrator rebuild manual kalau perlu.
- **Hermes `vision_analyze` 404 = buta baca screenshot Bos.** Causa: `auxiliary.vision.model` di config.yaml salah (`gemini/gemini-3-flash-preview` tidak ada di proxy 9Router → 404 "Couldn't find that"). FIX: `hermes config set auxiliary.vision.model ag/gemini-3.6-flash-medium` (model vision asli di 9Router Proxy, tested jalan). Bos frustrasi berat ("sakit kali otakku") karena vision gagal berulang → tiap session baru, jika `vision_analyze` error 404, langsung cek `grep -A2 "auxiliary:" config.yaml` dan pastikan model = `ag/gemini-3.6-flash-medium` (bukan gemini/* yang tidak ada di proxy).

## AFFILIATE SHOPEE — CHANNEL & TOOL ALTERNATIF (riset 2026-08)
Referensi video ID (transkrip disabled, diambil dari judul + landscape):
- Hendra Setyo — "2 JUTA PER HARI TANPA BIKIN VIDEO THREADS + SHOPEE AFFILIATE": distribusi via **Threads** (Meta), konten teks/carousel TANPA video, reach organik tinggi.
- afree adi — "Tutorial konten affiliate Shopee pake Ai Agent – Alternatif n8n Gratis": **AI Agent** (bukan n8n) bisa generate konten affiliate gratis.

Implikasi ZIYAN:
- Channel prioritas affiliate = **Threads + FB Page** (bukan cuma FB Page).
- Tool: bisa pakai **AI Agent gratis** (Hermes + 9router) sebagai alternatif n8n untuk generate caption/carousel dari Sheet link affiliate.
- Tanpa video = lebih cepat & murah, selaras etik (foto asli produk, AI hanya bikin lifestyle bg/card promo).
- Pitfall: Threads API posting terbatas (butuh approval Meta); auto-post ke profil pribadi tidak didukung API — hanya Page.

## AFFILIATE SHOPEE — PIPELINE TEKNIS (2026-08, praktik langsung)
Bos punya FB App "n8n" (ID `1994676317847313`) + Threads app (`1346767533487099`) + Page + Shopee Affiliate aktif.

### FB Page auto-post (jalan hari ini)
- App ID/Secret **TIDAK CUKUP** untuk posting. Butuh **Page Access Token**.
- Alur: Graph Explorer → Generate User Token (scope: `pages_manage_posts`, `pages_read_engagement`, `pages_show_list`) → tukar long-lived:
  `GET graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=1994676317847313&client_secret=APP_SECRET&fb_exchange_token=USER_TOKEN`
  lalu ambil Page ID + Page token: `GET graph.facebook.com/v19.0/me/accounts?access_token=USER_TOKEN`.
- **SECURITY**: Bos sering paste App Secret/Token ke chat. Orkestrator WAJIB pindah ke file `.env` lokal (misal `ziyan_fb_credentials.env`) + sarankan rotate. Jangan biarkan secret melayang di chat history.
- Post **SINGLE PHOTO** (terbukti jalan): `POST graph.facebook.com/v19.0/{PAGE_ID}/photos` dengan **multipart form-data** (`source=@file`, `message`, `access_token`) — BUKAN JSON body `url:data:image/png;base64,...` (FB tolak: "url should represent a valid URL"). Di n8n: HTTP Request node `contentType=multipartFormData`, `binaryProperty=data`.
- **VIDEO POST** (terbukti jalan, tes 2026-08-07): `POST graph.facebook.com/v19.0/{PAGE_ID}/videos` dengan multipart form-data (`description`, `access_token`, file video via `source`). URL/9router tidak dipakai — video diupload langsung dari file lokal. Di workflow: node `FB: Upload Video` paralel dengan `FB: Post Photo` (pilih berdasar ekstensi file: `.mp4/.mov/.webm` = video).
- **CAROUSEL GAGAL** di Page Bos: `POST /{PAGE_ID}/media` balas `(#100) subcode 33 = Unsupported post request` (fitur media/unpublished-photo belum di-aktifkan di app, butuh **Meta app review**). Jangan buang waktu ke carousel sampai app Live+review. Pakai single-photo (langsung jalan, compliant).

### Threads (BELUM bisa auto-post)
- Threads Graph API wajib **app review** (Live + `business_use_case` + akun business/creator). Tanpa review hanya read.
- Strategi: FB Page jalan dulu; Threads generate caption di n8n, Bos copy-paste manual sampai app lolos review.

### Hybrid image (COMPLIANT, jangan produk palsu)
- Shopee Affiliate melarang tampilkan produk tidak sesuai asli → komisi batal + akun ban + langgar etik Bos.
- Cara: screenshot foto ASLI produk → upload Sheet/Storage → `9router-image` generate **lifestyle background** (elektronik=meja kerja, fashion=ootd abstrak) → composite foto asli di atasnya via **PIL lokal** (resize 1080x1080, 4 slide carousel).
- 9router-image: OpenAI-compatible `POST http://127.0.0.1:20128/v1/images/generations`, header `Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY`.
- **MODEL YANG JALAN (2026-08-07, tested)**:
  - ✅ `cf/@cf/black-forest-labs/flux-1-schnell` — GRATIS, return `b64_json` (base64 PNG). PALING ANDAL utk composite lokal.
  - ⚠️ `nb/nanobanana-flash` — jalan tapi sering "credits insufficient, reset 20s". Return `url`.
  - ❌ `gemini/gemini-3-pro-image-preview` — 429 quota. ❌ `flux` (model salah, tidak ada di lista).
  - Cek model available: `GET http://127.0.0.1:20128/v1/models/image`.

### Caption otomatis via 9router chat (9Router Proxy)
- Node n8n `HTTP Request` → `POST http://127.0.0.1:20128/v1/chat/completions`, header `Authorization: Bearer {{ $env.HERMES_CUSTOM_9ROUTER_API_KEY }}`.
- Body: `{"model":"openrouter/auto","messages":[{"role":"user","content":"<prompt caption>"}],"max_tokens":200}`.
- Response: `choices[0].message.content` = caption. Di n8n: `{{ $json.choices[0].message.content }}`.
- Ini pakai combo `openrouter` (fallback) di 9Router Proxy dashboard. Buat caption/naskah tanpa ketik manual di sumber data.
- Pitfall: jangan campur dengan `/v1/images/generations` (itu gambar, beda endpoint).

### INPUT DARI HP — TELEGRAM BOT (pilihan Bos, 2026-08-07)
- Bos mau **ganti Form dengan Telegram bot** (kirim link + foto/video langsung dari HP → agent simpan Sheet → upload sosmed).
- Bot `CelineaureBot` (token di `ziyan_telegram.env`) sudah CONNECT ke Hermes gateway (polling mode: `hermes gateway restart` → log "✓ telegram connected").
- **SETUP**: token di `.env` Hermes baris `TELEGRAM_BOT_TOKEN=` (uncomment `#` + isi literal, jangan biarkan `#`). Lalu `hermes gateway restart`. Biarkan `TELEGRAM_ALLOWED_USERS=` kosong (atau isi chat_id Bos) untuk izinkan siapa saja.
- **Alur rencana**: Telegram (link + media) → Hermes tanya detail (harga/diskon/kategori) → simpan row ke Sheet `1wLqdaYcjdaxXD1nEXPIv9PHObFhQPCi80cSiUHqEG8w` → n8n schedule tiap **87 menit** ambil `posted=false` → Foto=composite PIL→FB / Video=upload FB → mark `posted=true`.
- **PITFALL**: Bos harus kirim 1 pesan dulu ke bot (@CelineaureBot) supaya gateway tahu chat_id Bos sebelum bisa balas otomatis.
- **TARGET SOSMED (2026-08-07 malam, tested): FB Page = JALAN. Threads = BLOKIR review Meta (subcode 33) → skip. X/Twitter = APP+BEARER ADA tapi POSTING GAGAL via bearer.**
- **X/Twitter — SEKARANG JALAN (terbukti 2026-08-07, tweet id `2085701683632644177`):** app `shopeeaffiliateee`, akun `@AgenticsID` (id `2079132337502359552`). **Consumer Key BENAR = `vVXNsMZEZ2k2EhyiHRA3a8YQt`** (GANTI `GXkFwJzQvMj1Iem2g8d3wguH` yang 401 — itu dari app salah). Access Token `2079132337502359552-5RyHsdhfTOtCwZMqKj1pKVfHs9TgnO` + Secret `IxFS7LXBHjluCmFmKWy1m5xXE04QYMST32UBM8Z1hTRwG` (OAuth 1.0a User Context, dari X Dev Console → "Access Token and Secret"). **BEARER App-Only TETAP GAGAL POST** (403) → jangan pakai. **Cara post yang JALAN (Python `requests_oauthlib`, SUDAH TESTED):**
  ```python
  from requests_oauthlib import OAuth1Session
  o=OAuth1Session(CK, client_secret=CS, resource_owner_key=AT, resource_owner_secret=ATS)
  r=o.post('https://api.twitter.com/2/tweets', json={'text':'caption link'})  # 201=sukses
  ```
  **n8n**: node `executeCommand` panggil `python3 -c "..."` dengan env `X_CK/X_CS/X_AT/X_ATS` (set di n8n `settings` key=`env`, restart n8n). **Node X SUDAH AKTIF di workflow** (bukan disabled). **PITFALL**: `executeCommand` di n8n v2.33 BELUM terverifikasi jalan di dalam n8n (hanya pola Python di atas yang tested langsung). Kalau executeCommand gagal, ganti Code node (Python) atau HTTP Request + signing manual. **Free tier = 17 tweet/24 jam** (akun baru). Etika: jangan auto-post X tanpa izin Bos. Detail: `references/x_twitter_oauth_setup.md`.

### FASHION ASSET INGESTION (mass content dari zip, 2026-08-07)
- Bos kirim `download.zip` (149MB, 176 file) → extract → **150 foto fashion** (street style/OOTD/mirror selfie/hijab).
- **FILTER WATERMARK**: `vision_analyze` sample 5 → mayoritas BERSIH. Watermark `bellzxshop` cuma 1 foto (filter `if 'bellzxshop' not in f.lower()`).
- **MASUK SHEET**: `url_foto_asli` = path lokal Windows (`C:/Users/arija/Downloads/fashion_assets/<file>.jpeg`), `kategori=fashion`, `posted=FALSE`, `link_affiliate=""` (outfit utuh → caption inspirasi OOTD, bukan affiliate langsung).
- **TOKEN GOOGLE HABIS 1 JAM** → refresh: `curl -X POST oauth2.googleapis.com/token grant_type=refresh_token` pakai client_secret `installed` (`client_secret_3131524149-...json`) + `refresh_token` dari `ziyan_google_token.json`. Simpan `access_token` baru.
- **PITFALL**: python baca path absolut Windows (bukan posix `C:/...`). `base64` bash GAGAL file >~100KB (Argument list too long) → kirim lewat `requests` Python, bukan curl CLI. Workflow n8n otomatis composite + post tiap 87 mnt.
- Watermark detection: Tesseract tidak ada (binary), `easyocr` tidak terinstall. Pakai `vision_analyze` sampling (5 foto cukup untuk pola). Jangan brute-force 150x vision (mahal).

### YOUTUBE TRANSCRIPT GAGAL (429) — WORKAROUND
- `yt-dlp --write-auto-subs` → HTTP 429 (rate limit keras, butuh impersonation). `captionTracks` URL kosong.
- Solusi: (a) `vision_analyze` ke frame, (b) 9Router `web-search` ringkasan, (c) Bos kasih `.srt`/`.vtt` manual.
- Kasus (2026-08-07): 2 video ADANG HDYT "agentic AI gratis + CLI ke GUI" → tidak bisa transcript → suruh **Claude Opus 4.6 Thinking** (`ag/claude-opus-4-6-thinking`) analisa dari judul → rencana upgrade (ReAct loop + GUI Streamlit/Telegram). Plan: `ziyan_upgrade_plan.md`.
- **Opus CALL**: `POST 127.0.0.1:20128/v1/chat/completions model=ag/claude-opus-4-6-thinking` (proxy paksa SSE walau `stream:false` → parse `iter_lines()` eval `data:` → `choices[0].delta.content`). Model PALING PINTAR di 9Router, pakai untuk strategi/bedah video/koreksi skill. Jangan pakai Gemini biasa kalau Bos mau "model paling pintar".

### DATA ENTRY DARI HP — Sheets/Form > Firestore
- **Keputusan Bos (2026-08-07)**: input produk dari HP → **Google Sheets + Form LEBIH GAMPANG** dari Firestore (Firebase Console ribet di mobile).
- Rencana: migrasi workflow dari Firestore → Google Sheets (`link_affiliate, url_foto_asli, kategori, harga, diskon, posted`) + Google Form (link di HP, isi → auto Sheet).
- **OAuth SELESAI (2026-08-07)**: token di `ziyan_google_token.json`, Sheet `1wLqdaYcjdaxXD1nEXPIv9PHObFhQPCi80cSiUHqEG8w` (ZIYAN Shopee Affiliate) sudah dibuat dengan header + 1 contoh row.
- **JANGAN pakai `google-workspace` setup.py** (generate URL PKCE + redirect `localhost:1` → tukar gagal `invalid_grant`). Pakai plain URL + manual curl → lihat `references/google_oauth_sheets_setup.md`.
- Client secret yang jalan = **`installed` (Desktop)** type, `redirect_uris:["http://localhost"]`. Web type → `redirect_uri_mismatch` Error 400.
- **Forms API belum enable** (`forms.googleapis.com`) → 403 SERVICE_DISABLED saat bikin Form. Bos harus enable dulu di Console, lalu saya lanjut bikin Form + sambung ke Sheet.
- Update workflow Firestore→Sheets: ganti node `Firestore Read` jadi `Google Sheets` (Read), `Firestore Update` jadi `Google Sheets` (Update Cell `posted=true`).
- Catatan: Service Account Firebase (`firebase-adminsdk`) BISA akses Sheets kalau di-share, tapi TIDAK bisa akses Form. Kalau mau Form → harus OAuth biasa.

### Firebase v2 (kandidat ganti Sheets)
- Pakai **Service Account JSON** (Firebase Admin SDK), BUKAN Web API Key. Simpan ke `ziyan_credentials/firebase_admin.json`.
- Firestore = penyimpan link affiliate + status posted (NoSQL scalable). Bos punya project `ZiyanCorp` (Auth aktif, Firestore belum di-enable).
- Tradeoff: Sheets node n8n native (cepat); Firestore butuh HTTP Request REST (scalable, multi-klien).
- Quirk kritis: `firestore.client(app, database_id='default')` WAJIB explicit (error 404 kalau tidak). venv Hermes rusak cryptography → pakai `.venv_firebase` sendiri. Lihat skill `ziyan-firebase-backend`.

## BUILD LOG: Workflow Shopee Affiliate → FB Page (2026-08-07, PRAKTIK + TERBUKTI)
Arsitektur final (hybrid compliant, 10 node, TERBUKTI post ke Page `975723622288353`):
1. Schedule 09:00 → 2. Firestore/Sheets ambil 1 `posted=false` → 3. **AI Generate Caption** (9router `openrouter/auto` chat) → 4. Build Prompts → 5. 9router Generate BG (`flux-1-schnell`) → 6. PIL composite 1080x1080 (foto asli + bg) → 7. FB Post Photo (multipart) → 8. mark `posted=true`.
- **BUKTI**: post id `975723622288353_122141094105223725` masuk ke Page Celine Aurel.
- **CAROUSEL DITOLAK** (subcode 33, butuh Meta review) → pakai single-photo. Jangan ulang carousel.
- **SELESAI (2026-08-07)**: OAuth Desktop app (`installed` type, client `3131524149-2ek5m9fg8o60p78bl8b1a546m7aj5o19`) authorize sukses → token di `ziyan_google_token.json`. Sheet `1wLqdaYcjdaxXD1nEXPIv9PHObFhQPCi80cSiUHqEG8w` (ZIYAN Shopee Affiliate, header + 1 row contoh) + Form `1G1TDq7VzFqMN50tAOJw5dY5J36wRha3yCRzlp4aeto0` sudah dibuat. Form BELUM tersambung ke Sheet via API (`responseDestination` tidak didukung batchUpdate versi ini) → Bos sambung manual UI (Responses → ikon spreadsheet → pilih existing Sheet ID above). Setelah tersambung: ubah node n8n Firestore→Google Sheets (`ziyan_workflow_v2.json` rebuild, DB id `8a30e6f0-bb49-404f-98db-ff6b309fcd65`).
- File workflow: `C:\Users\arija\ziyan_workflow_v2.json`. n8n DB `workflow_entity` id `8a30e6f0-bb49-404f-98db-ff6b309fcd65`.
- **UPDATE (2026-08-07 malam) → 12 NODE, interval 87 menit, multi-channel:** Workflow di-rebuild jadi: Schedule (87 mnt) → Sheets Read (`posted!=TRUE`) → Parse → AI Caption (9router) → Build Prompts → 9router BG (flux-1-schnell) + Promo BG → PIL composite → **FB Post Photo (multipart) + FB Upload Video (paralel)** → Sheets mark `posted=true` + **X Post Tweet (executeCommand python, aktif)**. Firestore DIGANTI Sheets (Bos mau input HP via Sheets/Telegram, bukan Firestore). FB token di `ziyan_fb_credentials.env` (page token fresh, scope `pages_manage_posts`). X token di `ziyan_x_*.env` (OAuth1.0a, JALAN). Threads SKIP (subcode 33 review Meta).

PITFALL build (dari sub-agent, DIKOREKSI — jangan ulang):
- 9router-image URL salah: sub-agent nulis `https://api.9router-image.com`. BENAR = `http://127.0.0.1:20128/v1/images/generations` (proxy lokal).
- Node "function" n8n = **JavaScript**, BUKAN Python. Composite gambar → pakai **Code node mode Python** atau external script (PIL).
- Carousel FB benar: upload per-foto → `creation_id`, publish pakai `attached_media=[{media_fbid}]`. BUKAN album `url` (gagal muncul).
- FB auto-post ke **profil pribadi TIDAK didukung API** → hanya Page.
- Threads auto-post butuh **app review Meta** (business_use_case) → manual/semiotomatis sampai lolos.
- Sub-agent QC bisa nyasar baca file salah (mis. `.gemini/antigravity`) → Orkestrator WAJIB verifikasi hasil sub-agent sendiri.

FB TOKEN (terbukti error #200):
- Generate User Token di Graph Explorer HARUS centang `pages_manage_posts` + `pages_read_engagement`. Tanpa `pages_manage_posts` → `(#200)` meski token valid + tidak expired.
- Page token `me/accounts` umur pendek → pakai user token fresh saat test post.
- `.env` jangan spasi tanpa quote (`FB_PAGE_NAME="Celine Aurel"`) → shell anggap command terpisah.

ENV/SECRET:
- Bos sering paste App Secret/Token ke chat. Orkestrator WAJIB pindah ke file `.env` lokal + sarankan rotate. Jangan biarkan secret melayang di chat.

## N8N v2.33.4 FUNCTION / IMPORT / WEBHOOK GOTCHAS (terbukti 2026-08-08, build `wa_order_notif` 15x iterasi)
Workflow gagal 15x dengan gejala `status:error` + `resultData:[]` (gagal SEBELUM node manapun jalan). Root-cause nyata:
- **`Date.now()` di Function node → SILENT FAIL.** Hapus, pakai timestamp dari webhook body atau hardcode. (Terbukti: ada Date.now gagal, hilangkan → success.)
- **Webhook `responseMode: onReceived` → "Error in workflow".** Hapus field itu (default / `lastNode` jalan).
- **Webhook PATH CONFLICT:** rebuild berkali-kali pakai path mirip (`wa-order-*`) → n8n simpan registrasi lama di memory → execution error kosong. Pakai **path unik segar** tiap build besar, atau restart n8n. Minimal Webhook→Function(echo) SELALU jalan → kalau gagal = path conflict, bukan logic.
- **HTTP Request ke eksternal tanpa creds (401) → workflow error.** Tambah `"continueOnFail":true` + `"onError":"continueRegularOutput"` di node params.
- **Import REST `POST /api/v1/workflows`:** strip `active`+`tags` (read-only), WAJIB `"settings":{"executionOrder":"v1"}`. Dapat ID baru → re-activate (`POST /api/v1/workflows/{id}/activate`).
- **Isolasi cepat:** Webhook→Function echo dulu (jalan?), lalu tambah 1 node + test tiap kali. Detail + pola restart Windows: `references/n8n_v233_debug_gotchas.md`.

## N8N CODE NODE — `child_process` DILARANG (PITFALL 2026-08-07)
- **Gejala**: workflow "Shopee Affiliate Video Bot" (Start → Run Python Bot → Notify) gagal: `Problem in node 'Run Python Bot'` → `Module 'child_process' is disallowed [line 2]`.
- **Penyebab**: n8n **Code node** jalan di sandbox yang memblokir `require('child_process')` / spawn subprocess. Node yang panggil Python via child_process → ditolak.
- **FIX**: ganti node itu jadi **Execute Command** (type `n8n-nodes-base.executeCommand`), BUKAN Code node. Execute Command diizinkan jalankan shell/python di luar sandbox.
- **Aturan**: kalau perlu jalankan script Python/CLI dari n8n → **Execute Command node**. Code node hanya untuk logika JS/Python murni tanpa subprocess.

## YOUTUBE SERVICE ACCOUNT — TIDAK BISA UPLOAD (KOREKSI KRITIS 2026-08-07)
- Bos punya SA `apikey@ziyancorp.iam.gserviceaccount.com` (project `ziyancorp`, file `ziyan_google_service_account.json`). SA **TIDAK BISA dipakai upload** ke channel CELINE AUREL.
- **BUKTI GAGAL**: `videos().insert` pakai SA → `401 youtubeSignupRequired` ("Unauthorized"). YouTube HANYA izinkan SA upload lewat **YouTube CMS / Brand Account terverifikasi**, BUKAN channel personal/manager biasa. Enable API + invite Manager SUDAH dilakukan tapi tetap 401.
- **JANGAN andalkan SA untuk upload Shorts**. Catatan lama "SA lebih tepat" SALAH — hapus dari ingatan.
- **SOLUSI YANG JALAN = OAuth User Token dari akun manager**:
  - Akun `The Visually Satisfying` (`UC2Z2COmJtCphYAkQ_M_wLFg`) ternyata JUGA manager CELINE AUREL. Saat OAuth consent pakai akun itu → `channels().list(id='UCzY1VDdRBSpDDHzBn_NcSLg')` accessible → `videos().insert` SUKSES (test video `QCySbhFvu-k`: https://youtube.com/shorts/QCySbhFvu-k).
  - Token di `ziyan_youtube_token.json` (field `channel_id`=`UCzY1VDdRBSpDDHzBn_NcSLg`, `refresh_token` tersimpan → tidak expired berbulan-bulan).
  - Cara tukar code: lihat section "YOUTUBE OAUTH CODE EXCHANGE" (pola 1 blok Python, code valid ~5 mnt).
  - **PITFALL**: kalau `channels?mine=true` balik channel LAIN (bukan CELINE AUREL) = akun login saat consent salah. Ulangi di Incognito pakai akun yang persis manager channel target.
- **SA TIDAK DI-INJECT KE 9ROUTER** (9Router tidak punya provider youtube). Simpan SA sebagai cadangan dokumentasi saja, jangan pakai untuk upload.

## YOUTUBE OAUTH CODE EXCHANGE — PITFALL (2026-08-07)
- **Error 400 Bad Request saat tukar code** = (a) `code` kadaluarsa (>5 menit sejak Bos copy), atau (b) var shell `$RESP` hilang di subshell berbeda (bash MSYS tidak persist antar `python3 -c`).
- **POLA HANDAL (tested jalan)**: jalankan exchange + simpan + cek channel dalam **SATU blok Python** (bukan pipa curl→python terpisah):
  ```python
  import json, urllib.request, urllib.parse
  CID='3131524149-...'; CSEC='GOCSPX-...'; CODE='4/0AXEQxIAB...'
  data=urllib.parse.urlencode({'client_id':CID,'client_secret':CSEC,'code':CODE,'grant_type':'authorization_code','redirect_uri':'http://localhost'}).encode()
  resp=json.loads(urllib.request.urlopen(urllib.request.Request('https://oauth2.googleapis.com/token',data=data,headers={'Content-Type':'application/x-www-form-urlencoded'})).read())
  tok={'client_id':CID,'client_secret':CSEC,'access_token':resp['access_token'],'refresh_token':resp['refresh_token'],'scope':resp['scope'],'token_uri':'https://oauth2.googleapis.com/token'}
  json.dump(tok, open('C:/Users/arija/AppData/Local/hermes/ziyan_youtube_token.json','w'))
  ```
- Simpan ke `ziyan_youtube_token.json` (PISAH dari `ziyan_google_token.json` yang scope Sheets/Forms — jangan merge sembarangan karena scope beda).
- Setelah tukar: VERIFIKASI `channels?mine=true&access_token=...` → cek `snippet.title` = channel target. Kalau kosong = akun salah saat consent.

## YOUTUBE SHORTS REDISTRIBUTION (2026-08-07, MULTI-CHANNEL)
- **KEPUTUSAN AKHIR (2026-08-07)**: Upload test nyasar ke channel "The Visually Satisfying" (bukan CELINE AUREL) karena akun login saat OAuth = owner channel itu. Video `QCySbhFvu-k` dihapus. Bos lihat tidak ada opsi Owner di Settings→Permissions (channel pribadi) → **BUAT CHANNEL YOUTUBE BARU** sebagai target. Node YouTube dicabut sementara (workflow balik 12 node). Token `ziyan_youtube_token.json` disimpan (valid) tapi wajib diulang setelah channel baru. Detail + URL authorize + cara ulang: `references/youtube_celine_aurel_upload.md` + skill `ziyan-youtube` section "CHANNEL CELINE AUREL".
- Bos mau sebar konten TikTok `@celineaurel` ke semua sosmed (FB + X + YouTube Shorts). Strategi: download video TikTok → **strip watermark** (crop/inpaint PIL + 9router) → upload ke tiap platform.
- **PITFALL WATERMARK**: video TikTok punya watermark "TikTok" → kalau di-repost polos ke IG/YouTube = **shadowban**. Wajib buang dulu.
- **YouTube OAuth (upload Shorts)**: pakai **OAuth User Token** (bukan SA — SA GAGAL 401, lihat section SA di atas). Token `ziyan_youtube_token.json` sudah punya scope `youtube.upload` + `youtube`, bound ke channel CELINE AUREL (`UCzY1VDdRBSpDDHzBn_NcSLg`), terverifikasi upload sukses (video test `QCySbhFvu-k`).
- **URL AUTHORIZE (installed client `3131524149-2ek5m9fg8o60p78bl8b1a546m7aj5o19`)**:
  ```
  https://accounts.google.com/o/oauth2/v2/auth?client_id=3131524149-2ek5m9fg8o60p78bl8b1a546m7aj5o19.apps.googleusercontent.com&redirect_uri=http://localhost&response_type=code&scope=https://www.googleapis.com/auth/youtube.upload%20https://www.googleapis.com/auth/youtube&access_type=offline&prompt=consent
  ```
  Bos buka → login akun channel "Celine Aurel" → copy `code=` dari address bar → tukar jadi token (pakai pola di section "YOUTUBE OAUTH CODE EXCHANGE" di atas) → simpan ke `ziyan_youtube_token.json`.
- Upload Shorts: `POST youtube.googleapis.com/youtube/v3/videos?uploadType=file&part=snippet,status` (metadata: `snippet.title`, `status.privacyStatus=public`, `snippet.categoryId=26` fashion). Pakai `requests` + file path (bukan base64 besar).
- **IG/Threads**: tetap BLOKIR review Meta (subcode 33) → skip auto-post.

## STREAMLIT DASHBOARD (GUI KOMISARIS, GRATIS & LOKAL)
- Bos (komisaris) mau kontrol tanpa terminal → bikin dashboard web lokal.
- **TEKNIK (2026-08-07)**: venv Hermes (`.venv_firebase`) TIDAK punya pip → buat venv baru: `uv venv ziyan_dash_env --python 3.11` lalu `uv pip install --python ziyan_dash_env/Scripts/python.exe streamlit requests`.
- Jalankan: `ziyan_dash_env/Scripts/python.exe -m streamlit run ziyan_dashboard.py --server.port 8501 --server.headless true` (background). Akses `http://localhost:8501` di HP via browser.
- File: `C:\Users\arija\AppData\Local\hermes\ziyan_dashboard.py` (baca n8n SQLite + Sheet + status X + kontrol workflow on/off).
- Ini implementasi "GUI buat komisaris" dari rencana Opus (ReAct + GUI). Streamlit <50 baris cukup untuk kontrol + view foto antrian.
- **Catatan**: `streamlit run` butuh shell yang bukan "no job control" → jalankan via `cmd.exe /c "..."` di background, bukan bash langsung (bash no job control → streamlit tidak bind port).

## REFERENCES
- `references/agent-skills-spec.md` — spec Agent Skills (agentskills.io) + contoh nyata + pitfall ZIYAN (dari riset 6 sumber 2026-08).
- `references/affiliate_fb_threads_pipeline.md` — curl exact: FB token exchange, me/accounts, post carousel, Threads limitation, 9router-image, Firebase Admin.
- `references/google_oauth_sheets_setup.md` — OAuth Desktop app (tanpa PKCE), manual curl token exchange, bikin Sheet/Form, pitfall setup.py/google-workspace.
- `references/telegram_sheets_fb_pipeline.md` — arsitektur Telegram bot → Sheet → FB (interval 87m, ID Sheet/Form/n8n, setup gateway).
- `references/x_twitter_oauth_setup.md` — X app-only bearer GAGAL post (403); cara enable OAuth 1.0a User Context (PIN flow) biar Free Tier bisa tweet.
- `references/fashion_asset_ingestion.md` — mass content dari zip (extract, filter watermark, isi Sheet, pitfall path/base64/token).
- `references/9router_antigravity_models.md` — katalog 13 model `ag/*` di 9Router Proxy + kehebatan tiap model + cara panggil. Catatan: Antigravity BUKAN app terpisah, bisa dipanggil langsung lewat 9Router.
- `references/n8n_v233_debug_gotchas.md` — 15x iterasi debug `wa_order_notif`: Date.now silent-fail, path conflict, responseMode, import read-only fields, restart Windows.
- `references/youtube_celine_aurel_upload.md` — BUKTI upload Shorts CELINE AUREL (OAuth user jalan, SA GAGAL 401), cara Python + node n8n.

