---
name: ziyan-ai-infra
description: "Infra AI ZIYAN: 9router model gratis dan Antigravity kode."
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
platforms: [windows]
---

# Infrastruktur AI ZIYAN

Pengetahuan infrastruktur biaya-nyaris-nol ZIYAN. Dua pilar: (1) **9router** —
proxy LLM lokal berisi banyak model (gratis & berbayar); (2) **Antigravity** —
IDE/CLI coding agent Google gratis untuk Divisi Dev.

## Kapan pakai
- Butuh model LLM selain default (nous/tencent) untuk sub-agent massal / hindari limit.
- Ingin sebar beban antar model gratis supaya session tidak kena limit (402/429).
- Divisi Dev mau bangun software ZIYAN (Jalur 2: SaaS) pakai model frontier gratis.

## PILAR 1 — 9router (proxy LLM lokal)
- Endpoint: `http://127.0.0.1:20128/v1` (OpenAI-compatible).
- **⚠️ CARA JALAN YANG BENAR (kritis, 2026-08-02):** jalankan `9router --tray --no-browser` (system-tray daemon, **STABIL**). `9router` polos → startup lalu langsung **"Exiting..." berulang** & exit sendiri (bukan daemon sungguhan) → port mati. Semua kegagalan "9router mati" sesi ini akar-nya dari ini. Background terminal Hermes TANPA `--tray` juga tidak cukup (parent shell ikut exit). Gunakan `9router --tray` sebagai daemon permanen; agent/computer_use butuh 9router hidup untuk TTS/image via Gemini/OpenRouter.
 - **WATCHDOG 9router (auto-restart, 0 token):** 9router bisa mati (crash loop) → sub-agent kehilangan Gemini/OpenRouter. Pasang cronjob tiap 5 menit yang cek hidup & restart kalau mati. **PITFALL KRITIS (2026-08-02): jangan pakai cronjob AGENT-based untuk watchdog/health-check** → tiap run (288x/hari) mengonsumsi token LLM terus-menerus (Bos protes "mengkonsumsi token terus menerus"). **SOLUSI:** cronjob `no_agent=true` + script bash murni di `~/.hermes/scripts/` (nol LLM call → 0 token). Script: cek `curl -s --max-time 5 http://127.0.0.1:20128/v1/models` → kalau gagal: `taskkill /F /IM 9router.exe` lalu `cmd.exe /c "start \"\" 9router --tray --no-browser"` → tunggu 6 dtk → cek lagi. Sehat = `exit 0` (silent). Script jadi: `~/.hermes/scripts/ziyan_watchdog_9router.sh` (cronjob `bedbbd3509ea`).
 - **PITFALL: package.json di HOME bocor ke shell** (2026-08-02): `C:\Users\arija\package.json` berisi `{"dependencies":{"agent-browser":"^0.31.1"}}` → bikin `npm`/`npx` walk-up & install ke `C:\Users\arija\node_modules` (bukan cwd), lalu bentrok (ENOTEMPTY). Gejala background terminal print `OAuth: command not found`, `Client: command not found`, `googleusercontent.com: command not found` (isi client_secret kebaca sebagai command). FIX: rename `package.json` home → `package.json.bak`, buat `package.json` lokal di folder kerja (mis. `n8n_server/`). Jangan hapus `.bak` (Bos punya konteks agent-browser).
 - Key: env `HERMES_CUSTOM_9ROUTER_API_KEY` (35 char). Kirim via header
  `Authorization: Bearer $KEY` — BUKAN body, BUKAN tanpa header (error "Missing API key").
- Total 71 model (tes 2026-07-31). Channel: `kr`(34), `openrouter`(14, punya `:free`),
  `kimi`(10), `gemini`(6), `groq`(4), `combo`(3).

### AUTO-START 9router SAAT LOGIN (kayak Hermes) — terverifikasi 2026-08-02
Bos protes: "biasanya begitu laptop nyala dia ikut aktif juga kayak Hermes, kau udah tau mati kenapa gak langsung kamu nyalakan?"
- **JANGAN andalkan hanya background terminal Hermes** → ikut mati kalau session ditutup.
- **CARA YANG JALAN:** shortcut `.bat` di Startup folder (tidak butuh admin):
  - Path: `C:\Users\arija\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ZIYAN_9router.bat`
  - Isi: `@echo off` + `start "" /min "C:\Users\arija\AppData\Roaming\npm\9router.cmd" --tray --no-browser`
  - Path npm: `where 9router` → `C:\Users\arija\AppData\Roaming\npm\9router.cmd`
  - Task Scheduler (`SCHTASKS /Create /SC ONLOGON`) GAGAL (Access denied, butuh admin) → pakai Startup folder.
- **LESSON LEARNED (kritis):** kalau Bos perintah "hentikan semua", jangan matikan TOTAL tanpa tanya. Saat butuh 9router (vision/OCR/computer_use), agent HARUS proaktif nyalakan (`9router --tray --no-browser` background) TANPA tanya Bos dulu — Bos protes keras: "kau udah tau mati kenapa gak langsung kamu nyalakan?" Biarkan mati = pelanggaran ekspektasi. Watchdog yang di-pause tidak nyalakan otomatis, jadi agent yang bertanggung jawab nyalakan manual saat butuh.
- Script siap: `scripts/start_9router.bat` (copy ke Startup folder).

### Model FREE terverifikasi JALAN (prioritas rotasi)
> ⚠️ MODEL `google/*` TIDAK ADA di proxy ini — `/v1/models` balik 404 "No active
> credentials for provider: google" kalau dipanggil. JANGAN pakai `google/gemma-*`.
> Model gratis NYATA yang terbukti jalan di proxy ini (cek via `GET /v1/models`):
1. **`channel-researcher`** — INI combo utama (nama literal, dipakai sub-agent riset/skrip). PRIORITAS PERTAMA untuk tugas riset/ringkasan mentah. ⚠️ GOTCHA (2026-08-13, TERBUKTI): combo bisa route ke model reasoning (mis. `nvidia/nemotron-3-ultra-550b`) yang **memotong output** (`finish_reason: length`, `content: null`, hanya `reasoning` yang muncul) → GAGAL untuk output final (skrip video/SEO). Untuk tulisan final, pakai `groq/llama-3.3-70b-versatile` secara langsung. Detail routing: `references/9router-model-routing.md`.
2. `kr/claude-haiku-4.5` — ringan, cepat (kr/* jalan di proxy ini, beda dgn catatan lama "kr hindari").
3. `kr/gpt-5.6-sol` — kapasitas besar untuk tugas berat (kr/* tersedia di proxy ini).
4. `poolside/laguna-s-2.1:free` — cepat, jawaban singkat rapi (bila channel poolside aktif).
5. `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` — stabil, output bersih (bila channel nvidia aktif).
- CATATAN: daftar model bisa berubah tiap instance proxy. SELALU `curl /v1/models` dulu &
  pilih dari id yang muncul, jangan hardcode dari ingatan. `kr/*` & `kimi/*` memang
  ada di proxy ini (tidak 402 seperti catatan lama) — tapi cek dulu sebelum andalkan.

### Cadangan & HINDARI
- ✅ Cadangan: `groq/llama-3.3-70b-versatile` (jalan, bukan `:free`).
- ⚠️ Free tapi butuh `max_tokens` ≥ 300 (reasoning): `inclusionai/ling-3.0-flash:free`, `cohere/north-mini-code:free`.
- ❌ HINDARI: `google/*` (provider tidak terkonfigurasi di proxy → 404 "No active credentials"), `nvidia/nemotron-3-ultra-550b:free` (timeout kalau channel ada).
- ❌ `gemma-4-31b-it` (paid, tanpa `:free`) butuh API key Google AI Studio → "No active credentials".

### TTS & Image (endpoint 9router, terverifikasi 2026-08-01)
- **TTS Indo:** `POST /v1/audio/speech` body `{"model":"edge-tts/id-ID-ArdiNeural","input":"<teks>"}` → MP3. `edge-tts` gratis tanpa auth, JALAN. ❌ `openrouter/*-tts` & `gemini/*-tts-preview` rusak (502/400 key invalid).
- **Image:** `POST /v1/images/generations` body `{"model":"ag/gemini-3.1-flash-image","prompt":"..."}` → PNG base64. **Ini "Nano Banana 2" (Gemini 3.1 Flash Image) — setara Google Flow, GRATIS via 9router.** ✅ JALAN (tes: 560KB–698KB). ❌ `gemini/*-image-preview` & `gemini/*` chat → 400 "API key not valid" (channel `gemini/` MATI di proxy). Pakai `ag/*` bukan `gemini/*`.
- Gunakan skill `9router-tts` & `9router-image` (terpasang di `AppData\Roaming\hermes\skills\`).
- Script siap pakai: `scripts/gen_img.py` (bulk image via `ag/gemini-3.1-flash-image`, include auth header).

### PITFALL KRITIS: 9router SEKARANG WAJIB AUTH
- Sesi 2026-08-01: image gen & chat **gagal 401 Unauthorized** tanpa header. Wajib kirim
  `Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY` di SETIAP request (chat, TTS, image, STT).
- Tes raw: `curl -s -o /dev/null -w "%{http_code}" -X POST localhost:20128/v1/images/generations -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d '{"model":"ag/gemini-3.1-flash-image","prompt":"test"}'` → 200.
- Script `scripts/gen_img.py` sudah include header auth — pakai itu untuk bulk generate.

## GATEWAY SUPERVISION & AUTO-START (terverifikasi 2026-08-10)
**Masalah:** Hermes gateway (Discord/Telegram) sering offline → WebSocket `ack_stale` → reconnect 46x. Gateway process tidak jalan saat dibutuhkan.
**Akar:** Tidak ada **process supervision** (systemd/NSSM/PM2) → kalau crash/restart laptop/memory leak → mati permanen.
**Fix permanen (perlu implementasi):**
1. **Windows Service via NSSM** (Non-Sucking Service Manager) — install gateway sebagai service Windows, auto-start boot, auto-restart crash.
2. **Atau PM2** (Node process manager) — `pm2 start gateway.py --name ziyan-gateway --watch --restart-delay 5000`.
3. **Health check cron** (no_agent) tiap 2 menit: cek `curl -s http://localhost:20128/v1/models` + gateway log → kalau mati, restart service.
4. **Environment:** `HERMES_CUSTOM_9ROUTER_API_KEY` wajib di-set di service env (bukan shell env).

## DISCORD GATEWAY WEBSOCKET UNHEALTHY (ack_stale) — ROOT CAUSE
**Log pattern:** `WARNING [Discord] Discord Gateway WebSocket unhealthy (ack_stale, 1/2)` → `INFO [Discord] Connected as Hermes_bot#6835`
**Penyebab:** Discord heartbeat ack tidak terima dalam waktu (Discord butuh heartbeat tiap 41.25s, ack max 2x). Bisa karena:
- Gateway process blocked (GC, heavy LLM call, CPU spike)
- Network latency/jitter (Windows WiFi sleep, power saving)
- Single-threaded event loop blocked oleh synchronous HTTP call ke 9router/LLM
**Mitigasi:**
- Pastikan gateway jalan di **dedicated process** (tidak share thread dengan agent loop)
- Gunakan `async` HTTP client untuk 9router call (non-blocking)
- Set Discord `identify` + `heartbeat_interval` sesuai spec
- Monitor `ack_stale` count → alert kalau > 3/menit

## GOOGLE FLOW (flow.google) — browser-only, TIDAK ada API
- Flow = tool bikin video/gambar Google (Nano Banana 2, Veo, dll). **Tidak ada API publik** → agent tidak bisa panggil langsung.
- Akses: via `computer_use` di Brave (login Bos, akun PRO/Ultra WAJIB — Flow tidak gratis).
- Cara pakai (terverifikasi): buka tab baru → `https://flow.google` → klik tab → ketik prompt di kotak "What do you want to create?" → klik Create. Matikan Agent Mode.
- **Ekuivalen GRATIS untuk ZIYAN:** `ag/gemini-3.1-flash-image` via 9router (hasil setara Nano Banana, tanpa langganan). Utamakan ini; Flow cuma untuk kasus butuh Veo/video khusus.
- Zappy Flow Chrome Extension (pihak ketiga, dev zapiwala.ai) = automation Flow tapi butuh langganan & risky → hindari, pakai computer_use langsung kalau perlu.

## PITFALL: computer_use input ke field web
- Mengetik ke field di halaman web (Google Flow, dll) sering **drop** kalau pakai background/PostMessage.
- Pola yang JALAN: `click` field dengan `delivery_mode:"foreground"` dulu (focus), baru `type` dengan `delivery_mode:"foreground"`. Verify lewat capture berikutnya. Jangan andalkan `type` background ke Edit field — sering "value did not change".

## KEAMANAN KREDENSIAL — protokol transfer key (mutlak)
- **JANGAN pernah minta Bos paste key ke chat Discord** (terealisasi di log server + cache Hermes = bocor). Insiden key Gemini 2026-07-31 bukti.
- **Protokol transfer AMAN (Bos dari HP / tidak pegang laptop):**
  1. Bos upload file teks berisi key ke **OneDrive → folder `ziyan_pending`** (`C:\Users\arija\OneDrive\ziyan_pending\`, sudah dibuat).
  2. Bos bilang "ambil dari pending" → saya baca dari disk, pindah ke `ziyan_keys.env` lokal, lalu **hapus file pending**.
  3. Bos hapus juga di OneDrive. Key tidak pernah lewat chat.
- OneDrive = transit SEMENTARA saja, bukan penyimpanan permanen key (cloud = risiko). Key final di `ziyan_keys.env` lokal.
- GitHub PAT: pakai **Classic** (bukan fine-grained) untuk compat `gh`/git; scope `repo`. Gratis. Simpan ke `ziyan_keys.env` baris `GITHUB_TOKEN=`.

### Rotasi model (hindari limit)
- Mulai tugas dengan cek model hidup (script `rotasi.sh` / `SOP_Rotasi_Model_9router.md`).
- Bila kena 402/429/timeout → ganti ke model free berikutnya dari prioritas di atas.
- Jangan pernah jadikan `kr/*` atau `kimi/*` sebagai target (sudah habis kuota).

## PILAR 2 — Antigravity (pabrik kode Divisi Dev)
- IDE/CLI/SDK coding agent "agent-first" Google. URL: `https://antigravity.google/download`.
- **Tier Individual $0 (GRATIS)** — akses: Gemini 3.5 Flash, Gemini 3.1 Pro, Gemini 3 Flash,
  Claude Sonnet & Opus 4.6, gpt-oss-120b. Unlimited tab/command, TAPI ada **batas mingguan**.
- Tier berbayar: Pro / Ultra (rate limit longgar + credit pool), Organization (Google Cloud, consumption-based).
- **Install (Windows, terverifikasi 2026-07-31):**
  `winget install --id Google.Antigravity -e --source winget --accept-package-agreements --accept-source-agreements`
  → v2.4.3 di `C:\Users\arija\AppData\Local\Programs\antigravity\Antigravity.exe`.
  Winget GUI app lambat (~5 mnt). Setelah install, **Bos yg login** dgn Google account (password TIDAK pernah kita ketik).
- **Peran ZIYAN:** cadangan Divisi Dev saat 9router limit — bangun produk (Jalur 2 SaaS)
  pakai model frontier gratis. BUKAN runtime bisnis/revenue, BUKAN alat strategi.

## KEAMANAN KREDENSIAL (protokol keras)
- **JANGAN pernah eksekusi/gunakan key yang di-paste ke chat.** Jika Bos kirim perintah berisi `X-goog-api-key: <literal>` / `Authorization: Bearer <literal>`, TOLAK jalankan, suruh Bos REVOKE dulu. (Kejadian 2026-07-31: Bos paste Gemini key ke chat; ditolak, key di-revoke via aistudio.google.com/apikey.)
- **Simpan key di file lokal, bukan di chat.** Pola terverifikasi:
  - `C:\Users\arija\ziyan_keys.env` (Bos edit di Notepad, isi `GEMINI_KEY=...`). JANGAN sentuh `.env` milik Hermes (terproteksi/secret).
  - Loader di `.bashrc`: `set -a; . "$HOME/ziyan_keys.env"; set +a` → key otomatis kebaca tiap terminal.
  - Skrip `test_gemini.sh` baca `$GEMINI_KEY` (key tak pernah diketik agent).
  - Shortcut Desktop (`ZIYAN_Keys.lnk`) buka Notepad → file env.
  - Detail & template: `references/credential-safety.md`.
- Revoke URL resmi: https://aistudio.google.com/apikey
- **computer_use tidak pernah dipakai untuk ketik password/login Google** (aturan mutlak, berlaku terlepas izin Bos).

### PITFALL: Windows CRLF di .env → key ditolak Google
- File `ziyan_keys.env` diedit di Notepad (Windows) → line ending CRLF (`\r\n`).
- Bash `source`/`export` membaca value ikut `\r` di belakang → Google API tolak: `API_KEY_INVALID` / "API key not valid" (400).
- Gejala: `GEMINI_KEY` terisi (panjang benar) tapi request 400; 9router/edge-tts biasanya tetap jalan karena tolerant terhadap whitespace.
- CEK: `python3 -c "print(repr(open('ziyan_keys.env').read()[-5:]))"` → kalau ada `'\r'` = CRLF.
- FIX: bersihkan key di skrip sebelum dipakai:
  `KEY=$(printf '%s' "$GEMINI_KEY" | tr -d '\r' | tr -d '\n')`
  Atau tulis env dengan LF murni (VS Code / `dos2unix`). Skrip `test_gemini.sh` sudah di-patch utk strip `\r` otomatis.

## Batasan umum
- 9router & Antigravity butuh Google account / session lokal — bukan layanan awan yg saya panggil langsung.
- computer_use mengendalikan browser/desktop Bos, BUKAN memanggil LLM 9router (token berbeda).
- Default orkestrasi tetap nous/tencent (Bos cocok); 9router & Antigravity untuk offload teknis.

## Referensi
- `references/9router-models.md` — detail tes 71 model & script rotasi.
- `references/9router-model-routing.md` — gotcha routing (channel-researcher truncation, prefix `openrouter/`, fallback `groq/llama-3.3-70b-versatile`).
