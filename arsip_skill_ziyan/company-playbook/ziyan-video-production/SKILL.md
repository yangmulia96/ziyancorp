---
name: ziyan-video-production
description: "Bikin & download video ZIYAN: NotebookLM atau gratis."
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
platforms: [linux, macos, windows]
---

# Produksi Video ZIYAN — NotebookLM ONLY (perintah mutlak Bos, 2026-08-02)

## ⚠️ ATURAN MUTLAK — HANYA NotebookLM
Bos: **"Produksi video menggunakan NotebookLM. Tidak boleh yang lain."**
- Video ZIYAN HANYA boleh dibuat lewat NotebookLM (Jalur A).
- **Jalur B (edge-tts + ffmpeg gradient)** & **Jalur B2 (pyttsx3 offline)** = **DILARANG**. Bos tolak hasilnya ("Ga betul vidoe kayak gini.. hapus semua itu") — 4 video gradient robotik dihapus dari Compound Daily.
- OpenMontage (Jalur C) sudah dihapus & dilarang.
- Kalau NotebookLM butuh Bos login: Bos generate manual → taruh file di `OneDrive/ziyan_pending/` → agent ambil & upload. Atau Bos izinkan computer_use (lihat pitfall Brave di bawah). JANGAN ganti ke ffmpeg/pyttsx3 sebagai "cadangan".

Skill untuk membuat & mendownload video promosi ZIYAN.

## Kapan pakai
- Bos: "buat video di NotebookLM", "download video", "bikin video ZIYAN".
- Konten promosi / explainer / short untuk YouTube, TikTok, media ZIYAN.

## JALUR A — NotebookLM / Gemini Notebook (kualitas tinggi, sinematik)
Gunakan untuk video unggulan. Visual dinamis, narasi natural.

### Alur (via computer_use di Brave Bos yang SUDAH login)
1. **Login:** Google memblokir sesi browser AUTOMATION ("This browser or app may not be secure"). JANGAN coba login lewat browser tool saya. Gunakan Brave pribadi Bos yg sudah login `mziyan266@gmail.com` — kendalikan via `computer_use` (background, tidak curi kursor Bos).
2. Buka tab Gemini Notebook → buat notebook baru → "Copied text" → tempel naskah sumber → Insert.
3. Panel Studio → **Video Overview** → pilih format:
   - **Short** (~60 dtk, Inggris + 18+)
   - **Explainer** (panjang, dukung Indonesia) ← pilih kalau butuh bahasa ID
   - **Cinematic** (sinematik, Inggris)
4. Klik **Generate** → dialog tertutup = request masuk antrean. Generate jalan background, bisa **>30 menit**.
5. **TUNGGU** lalu cek panel Studio sampai kartu video muncul (label "Short · 1:11 · xm ago").
6. **⚠️ LANGSUNG KLIK DOWNLOAD — JANGAN PUTAR DULU.** Bos hanya butuh file, bukan pemutaran. (Pelajaran: pernah saya klik Play dulu, Bos protes.)
7. Dialog **Save As** muncul. Lokasi default sering aneh (mis. `nb_proof`, bukan Downloads). Langsung `set_value` ke path absolut, mis. `C:\Users\arija\ziyan_notebooklm_short.mp4`, lalu klik **Save**.
8. **Verifikasi lewat terminal** (bukan cuma lihat UI): `ls -la <path>` / `python3 -c "import os;print(os.path.getsize(...))"`. Kalau belum ada, cek tombol "New download available" di Brave → history download.
9. **JANGAN kirim video NotebookLM ke Discord/chat** — simpan di disk laptop saja (`C:\Users\arija\`). Bos tegas: "video notebooklm gak usah kirim kesini, cukup di laptop aja" + jaga token session agar tidak limit. HANYA kirim MEDIA: bila Bos eksplisit minta ("coba kirim hasilnya"). Video Jalur B (tes/gratis) BOLEH dikirim bila Bos minta lihat.

### Pitfall
- Sesi automation Google = diblokir login. Pakai Brave pribadi Bos.
- Jangan mainkan video kalau Bos minta download.
- Save As bisa default ke folder acak → selalu set path absolut & verifikasi.
- Subtitle/transkrip video sering dimatikan → bedah pakai skill `divisi-content-intel`, jangan mengarang.

### JALUR A2 — SELF-GEN via `notebooklm-py` CLI (TERBUKTI 2026-08-03, tanpa browser)
NotebookLM video juga bisa di-generate MANDIRI lewat CLI `notebooklm-py` (tanpa computer_use/Brave). Auth butuh cookie Netscape (bukan browser-cookies).
- Venv: `C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m notebooklm` (notebooklm-py==0.7.3).
- **Windows DPAPI blocks `login --browser-cookies brave/chrome`** (rookiepy gagal decrypt App-Bound-Encrypted cookie). JANGAN coba jalur itu.
- **Auth benar:** Bos export Netscape cookies dari `notebooklm.google.com` (ekstensi "Get cookies.txt LOCALLY") → agent filter Google domains → `python convert_netscape_cookies.py Downloads/cookies_google.txt .notebooklm/profiles/default/storage_state.json` (`convert_netscape_cookies.py` di `C:\Users\arija\`). Lalu `python -m notebooklm auth check --test` → "Authentication is valid." 1-klik: `C:\Users\arija\sync_notebooklm_auth.bat`.
- **Konversi cookie:** session cookie (expiry=0) → `"expires": -1` (Playwright tolak `null`); `sameSite` tetap `"Lax"`.
- **FLAG TRAP:** `add-research ... --import-all` WAJIB pakai `--wait` (default). Gabungan `--import-all --no-wait` ERROR. Contoh jalan: `notebooklm source add-research "topik" --from web --mode fast --import-all` (tanpa --no-wait) → "Imported N sources".
- **PITFALL PARSE ID (2026-08-04):** `add-research --json` balikin `rc=0` tapi **notebook ID TIDAK ada di JSON stdout** — hanya muncul di stderr sebagai `notebook <uuid>` (mis. `notebook 759af02d-634b-4d01-bdd2-fedcc68e6fe2`). Jangan parse id dari key `id`/`notebook_id` di stdout (kosong → abort salah). Ambil id via regex `notebook ([0-9a-f-]{36})` di stderr, atau `notebooklm list`.
- **PITFALL IMPORT_RESEARCH (2026-08-04):** stderr bisa log `RPC IMPORT_RESEARCH failed/timed out (server-error retries exhausted)` tapi sumber TETAP masuk (`sources.list shows all N requested URLs among new sources; treating as success`). Notebook tetap bisa dipakai untuk `generate video` — jangan anggap gagal/abort.
- **PITFALL WINDOWS PATH (2026-08-05):** `notebooklm source add /c/Users/.../file.md` GAGAL di Windows — CLI pakai `os.path.exists()` (Windows-native python) yang TIDAK kenal path MSYS `/c/...`, sehingga dianggap file tak ada & **meng-ingest STRING PATH sebagai inline text** (sumber jadi sampah, bukan isi file). FIX: pakai path Windows asli `C:\Users\...` supaya terdeteksi file & konten ke-ingest benar. Atau `--type text` dengan isi konten langsung (bukan path).
- **NOTEBOOK CREATE ID DI STDOUT (2026-08-05):** beda dengan `add-research --json` (ID cuma di stderr), `notebooklm create "Judul"` mengembalikan ID di STDOUT: `Created notebook: <uuid> - <title>`. Parse UUID dari stdout — lebih andal. Alur self-gen ringkas: `create` → ambil ID → `source add -n <id> "C:\...\script.md"` → `generate video -n <id> --format brief --no-wait --json` (JANGAN `--wait`, lihat PITFALL --wait BROKEN).
- **FORMAT MAP:** CLI `--format` = `explainer|brief|cinematic`. `brief` = tombol **Short** di UI (~60 dtk, <60s). Untuk Short pakai `--format brief` (bukan `explainer`).
`**generate video:** `notebooklm generate video "<DESCRIPTION/PROMPT>" -n <id> --format brief --no-wait --json` — **JANGAN `--wait`** (crash, lihat PITFALL --wait BROKEN di bawah; di notebooklm-py 0.7.3 `--wait` shell-out ke subcommand `api` yang tak ada). **PENTING (2026-08-12, TERBUKTI): positional cuma SATU = DESCRIPTION/prompt video.** Bukan `"judul" + "prompt"` terpisah — itu VALIDATION_ERROR `Got unexpected extra argument`. `task_id` dari output JSON == `artifact_id` (sama). **POLL WAJIB `notebooklm use <nb_id>` dulu** (set context aktif) sebelum `notebooklm artifact poll <task_id> --json`, else balik `not_found`. Poll loop di background: `use` → cek `status=="completed"` + field `url` (.mp4) → `curl -L` download. Generate butuh >180s (biasanya 30+ menit server-side) → jalankan di `terminal(background=true)`, jangan foreground.
- **PITFALL WAIT CLAMP + PIPELINE IDEMPOTEN (2026-08-05):** di host ini `process(wait)` di-clamp maks **60 detik** — TIDAK cukup untuk generasi 30+ menit. Maka 1 cron run TIDAK bisa selesaikan riset→generate→download→upload atomik. Pola yang dipakai: (1) Redirect output ke log: `... --json "prompt" > _gen.log 2>&1` supaya URL download tetap tersimpan di disk walau proses di-kill. (2) Simpan `video_pipeline_state.json` (notebook id, path log, status, uploaded). (3) Tiap run CEK state dulu — kalau `status=generating` jangan start generasi baru, cukup baca `_gen.log`; kalau sudah ada URL `.mp4` → download (`curl -L <url> -o file.mp4`) + upload lalu set `uploaded=true`. Ini cegah duplikat & menyambung antar run.
- **STALENESS:** kalau `auth check` lolos tapi `add-research`/`auth refresh` bilang "Authentication expired or invalid. Redirected to accounts.google.com" → cookie STALE (Google mutar token). Solusi: Bos export ulang cookie dari notebooklm.google.com yang MASIH login, convert ulang. `auth check` hanya cek "SID ada di file", BUKAN bukti session hidup.

### JALUR A2b — PIPELINE OTONOM CRON (generate → download → upload dalam 1 proses)
Kendala: generate video >30 mnt, tapi di sesi cron `process(wait)` di-clamp 60 dtk & `notify_on_complete` TIDAK didukung. Satu cron-run TIDAK bisa selesaikan riset→generate→download→upload atomik.
Pola terbukti (2026-08-07):
1. `create` → ID dari stdout → `source add -n <id> "C:\Users\...\source.md"` (path Windows asli, single-quote agar backslash literal; `$VAR` TIDAK terekspansi di string backslash-double-quote → selalu hardcode tanggal/path).
2. Di SATU proses background: `notebooklm use <nb_id>` (WAJIB set context, else `artifact poll` balik `not_found`), lalu jalankan `generate video ... --format brief --no-wait --json > _gen.log 2>&1` (simpan `task_id` dari output JSON `{"task_id":...,"status":"pending"}` — task_id INI == artifact_id), lalu POLL LOOP: `notebooklm artifact poll <task_id> --json` tiap 30-60s sampai `status=="completed"` (timeout ~90 mnt). Bila completed, extract field `url` (.mp4) → tulis ke _gen.log atau langsung `curl -L "$url" -o video.mp4` → chain `harvest.py` (download+upload) dalam proses yang SAMA. **JANGAN `--wait`** — crash (lihat PITFALL --wait BROKEN). `artifact poll` pakai NotebookLMClient langsung, aman (tidak shell-out `api`).
3. CHAIN `harvest.py` di DALAM proses background yang SAMA (setelah generate) → download + upload berurutan dalam satu proses yang bertahan walau sesi cron berakhir. JANGAN pisah ke run berikutnya.
4. `harvest.py` idempoten (lihat `scripts/compound_pipeline_harvest.py`): parse `_gen.log` cari URL `.mp4` → `urllib.request.urlretrieve` → panggil `ziyan_upload.py --file --title --tags --category 28 --privacy public` (token `ziyan_credentials/youtube_token_compound.json`). Update `pipeline_state.json` (generating→ready→downloaded→uploaded).

**PITFALL VERIFIKASI FILE MP4 ASLI (2026-08-13, TERBUKTI):** `curl -L "$url" -o video.mp4` bisa MENYIMPAN **HTML ERROR PAGE** (bukan video) bila URL butuh sesi auth/cookie atau sudah kadaluarsa — ukuran bisa 902KB tapi `file video.mp4` bilang **'HTML document'**. `curl` balik rc=0 (DL "sukses") padahal file BUKAN MP4 → upload jadi video kosong/rusak. DIAGNOSA NYATA: run 2026-08-12 menyimpan `compound_video.mp4` 902KB yang ternyata HTML (generate pakai 2 positional arg → VALIDATION_ERROR, tapi poll lama keburu 'completed' dengan URL stale; curl download tanpa cookie → HTML). FIX WAJIB di `harvest.py`/`compound_video_gen.py`: SETELAH download, VERIFIKASI (a) `file video.mp4` mengandung 'MP4' (BUKAN 'HTML'), (b) ukuran ≥ 1MB (NotebookLM Short ~9MB, Long lebih besar). Bila gagal → JANGAN lanjut upload; log `DOWNLOAD_INVALID`, simpan URL orphan, lalu regenerate (jangan pakai file tersebut). Jangan percaya rc=0 curl sebagai bukti video valid — selalu cek magic bytes + size.
5. Verifikasi lintas-run lewat `pipeline_state.json` + `process(action='poll')` pada pid background, BUKAN notify (cron tidak support notify).
**SCRIPT SIAP-PAKAI:** `scripts/compound_video_gen.py` (generate→poll→download, sudah benar: single-positional prompt + `use` sebelum `artifact poll`). Jalankan di background: `python compound_video_gen.py --notebook-id <id> --source <md> --out <mp4> --format explainer [--task-id <id>]`.
PITFALL ORPHAN (2026-08-07): run sebelumnya sukses generate (URL 302 valid) tapi TIDAK pernah upload karena proses background mati saat sesi cron berakhir. FIX: chain harvest DI DALAM proses background. Simpan URL orphan ke file tersendiri untuk recovery manual (jangan upload dengan metadata tebakan).
Cek duplikat upload: flag `uploaded` di state + `ziyan_upload.py` (ledger dedup) mencegah upload ganda antar-run.

**PITFALL --wait BROKEN (2026-08-08, notebooklm-py 0.7.3):** `generate video --wait` meng-shell-out ke subcommand `api` yang TIDAK ada di CLI → error `Error: Command "api" not found` + JWT token dieksekusi sebagai perintah shell (crash total, generasi gagal, tidak ada output ke log). STEP YANG BENAR (TERBUKTI 2026-08-12): (1) `generate video "<DESCRIPTION>" -n <nb_id> --format brief --no-wait --json` (SATU positional = prompt/description, BUKAN 'judul'+'prompt' → VALIDATION_ERROR) → simpan `task_id` dari output (task_id == artifact_id); (2) **`notebooklm use <nb_id>` dulu** lalu POLL `notebooklm artifact poll <task_id> --json` dalam loop (interval 30-60s) sampai `status=="completed"` — `use` WAJIB, tanpa itu poll balik `not_found`; perintah ini pakai NotebookLMClient langsung (`cli/artifact_cmd.py`), TIDAK shell-out `api`, sehingga aman; (3) bila `completed`, field `url` berisi URL download .mp4 → `curl -L` download + upload via `ziyan_upload.py`. Sudah dijalankan empiris 2026-08-12: generate→poll→download sukses; poll butuh context `use`.

## JALUR B — Gratis tanpa API key (mass-production)
## JALUR B — ❌ DILARANG (pelajaran pahit, 2026-08-02)
Bos: **"Produksi video menggunakan NotebookLM. Tidak boleh yang lain."**
Jalur B (edge-tts + ffmpeg gradient) & Jalur B2 (pyttsx3 offline) = **DILARANG** untuk produksi video ZIYAN.
Bos tolak hasilnya ("Ga betul vidoe kayak gini.. hapus semua itu") — 4 video gradient robotik dihapus dari Compound Daily.
Script `render_short.py` / `make_video_pipeline.py` tetap ada di disk sebagai referensi teknis, tapi **JANGAN jalankan** untuk video ZIYAN. Gunakan NotebookLM.

### JALUR C — OpenMontage — ❌ DIHAPUS (pelajaran pahit, 2026-08-02)
OpenMontage (calesthio/OpenMontage) SUDAH DIHAPUS dari disk (`rm -rf ziyan_openmontage`).
Alasan: butuh **27 menit/video**, API `imagen` 404 (user baru diblokir), Gemini image 429 (quota free habis),
Google TTS 401 (butuh GCP project, key AI Studio tidak cukup), `video_gen` berbayar tidak ada → hasil cuma
**image stills (bukan video AI)**. Tidak efisien untuk kita. **JANGAN rekomendasikan/sarankan OpenMontage lagi.**
Alternatif video berkualitas: (1) **NotebookLM via computer_use** (Bos login sekali, agent klik generate),
(2) **CapCut open-source** (`OpenCut-app/OpenCut`, 80K★ di GitHub) — lihat `references/opensource-video-editors.md`.

### Catatan
- Biar jadi animasi (bukan statis), butuh tahap ekstra (Manim/CapCut). CapCut sudah terinstall di Brave Bos.
- **CapCut open-source (OpenCut)** = `OpenCut-app/OpenCut` (80K★ di GitHub) — alternatif gratis buat edit video, bisa diotomatisasi. Bedah sebelum pakai (cek API/CLI-nya). Lihat `references/opensource-video-editors.md`.
- NotebookLM tetap jadi video final ZIYAN (sepakat Bos). Agent BISA generate via computer_use (Bos login sekali).

## 9router (proxy lokal, untuk sub-agent, BUKAN otak orkestrasi)
- Proxy `http://127.0.0.1:20128/v1`, key di env `HERMES_CUSTOM_9ROUTER_API_KEY`.
- Kirim key via header `Authorization: Bearer $KEY` (bukan body; tanpa header → 401 Unauthorized).
- computer_use TIDAK pakai token 9router (ia kontrol browser, bukan panggil LLM).
- **TES MODEL FREE — PERBAIKI (2026-08-13, TERBUKTI via 9Router):** JANGAN percaya daftar lama `google/gemma-*`. Fakta proxy sekarang (skill `ziyan-ai-infra` = otoritatif): `google/*` APA ADUNYA → 404 "No active credentials for provider: google" (termasuk `google/gemma-4-31b-it:free`). `openrouter/google/gemma-4-31b-it:free` ada tapi sering **429 rate-limited** → tidak stabil. ✅ JALAN & STABIL untuk generate skrip/SEO: `groq/llama-3.3-70b-versatile` (non-reasoning, output bersih, tanpa suffix `:free`). ✅ Riset: `channel-researcher` (combo) — ⚠️ WASPN: combo bisa route ke model reasoning (mis. nemotron-ultra) yang **memotong output** (`finish_reason: length`, `content: null`) → tidak bisa untuk output final. Untuk tulisan final (skrip/SEO) pakai `groq/llama-3.3-70b-versatile` LANGSUNG, BUKAN channel-researcher. ❌ HINDARI: `kr/*` & `kimi/*` (402), `nvidia/nemotron-3-ultra-550b:free` (timeout), `poolside/*` (429 — TERMASUK `laguna-s-2.1`; 1 call bisa lewat, tapi multi-call load PASTI 429). Detail routing: `references/9router-model-routing.md` (di skill `ziyan-ai-infra`).
  - **REFINASI EMPRIS (2026-08-14):** 2 call BERURUTAN (sequential) ke `openrouter/poolside/laguna-s-2.1:free` via 9Router — (1) generate script NotebookLM, (2) generate metadata/social — **KEDUA sukses, tidak 429**. Risiko 429 lebih ke arah *concurrent / heavy multi-call load*, bukan 2 call berurutan. Tetap wrap tiap call dengan fallback `groq/llama-3.3-70b-versatile` (snippet `references/9router-free-chat.md`) supaya aman kalau rate-limit naik. Untuk 1 call utama (mis. script gen) model user bisa dipakai langsung tanpa takut 429.
  - **UPDATE 2026-08-16 (empiris, 2x cron run Compound Daily):** klaim REFINASI EMPRIS di atas **SUDAH KADALUARSA untuk periode ini**. `openrouter/poolside/laguna-s-2.1:free` kini KONSISTEN **429** — terbukti gagal pada CALL PERTAMA (test) DAN pada 2 call berurutan (gen script + gen metadata) di DUA run cron berurutan (05:01 & 09:06 WIB/UTC, 16 Agt 2026). Penyebab body: `poolside/laguna-s-2.1:free is temporarily rate-limited upstream` (HTTP 200 tapi `{"error":{...[429]...}}`). **Tindakan otomatis wajib:** (1) jadikan `groq/llama-3.3-70b-versatile` PRIMARY free model untuk skrip/SEO/metadata; (2) poolside hanya opsi sekunder, jangan andalkan; (3) bila user EXPLICITLY minta poolside dan 429 → **langsung fallback ke groq, JANGAN loop-retry poolside, JANGAN abort task**. Semua via 9Router port 20128 (FREE). Pola ini sudah terbukti jalan di run 09:06 (script 107w + metadata lengkap staged via groq). Re-validasi poolside berkala — rate-limit free tier fluktuatif.
- **PARSING 9ROUTER WAJIB:** response selalu ada trailing text (`data: [DONE]`) → `json.loads()` GAGAL ("Extra data"). Selalu pakai `json.JSONDecoder().raw_decode(raw)[0]`. Saat generate banyak aset (skrip+metadata+social) dalam 1 script, WRAP tiap call dalam **fallback loop**: coba model user dulu → kalau HTTP 429/5xx, fallback ke `groq/llama-3.3-70b-versatile`. Snippet siap-pakai: `references/9router-free-chat.md`.

## PIPELINE YOUTUBE "COMPOUND DAILY" — FULL OTOMATIS (status 2026-08-01)
Channel `mziyan266@gmail.com` = **"Compound Daily"** (@CompoundDaily-v7c), 1-satunya channel. Niche 4-in-1: **Technology, AI, Business, Finance**. Target audiens internasional → **bahasa INGGRIS**.

### Arsitektur otomasi (semua gratis, jalan via cronjob)
```
[Topic Rotation] → [Script Gen dari riset keyword] → [NotebookLM generate video] → [Download ke disk]
   → [Judge agent QC] → [Upload jadwal random Compound Daily] → [log ZIYAN_COMPANY_LOG]
```
**TIDAK ADA tahap ffmpeg/pyttsx3/edge-tts** (dilarang Bos). Video HANYA dari NotebookLM.

### Jadwal (waktu PRIME TIME AMERIKA, konversi WIB)
- **Shorts**: 3x/hari → 06:00 / 12:00 / 18:00 ET = **18:00 / 00:00 / 06:00 WIB**
- **Long-form**: 3x/minggu (Selasa/Kamis/Sabtu) → prime time US
- Rotasi niche harian: Senin=Tech, Selasa=AI, Rabu=Business, Kamis=Finance, Jumat=AI (ulang)
- **UPLOAD pakai jadwal RANDOM** (bukan serentak) → biar tidak kelihatan bot (perintah Bos).

### CRON WINDOW-GATING & OFF-WINDOW PREP (2026-08-10, terbukti di cron run)
Cron pipeline DI-GATE oleh waktu. Jangan generate/upload di luar jendela — buang quota NotebookLM (3 video/hari) & risiko spam YouTube.
- **Short (≤60s, format `brief`)**: generate/upload HANYA saat UTC **15:00–23:00**.
- **Long (10–15 mnt, format `explainer`)**: HANYA **Senin/Rabu/Jumat 19:00–22:00 ET** (= UTC 23:00–02:00).
- **GOTCHA ET vs UTC (hari)**: hari Mon/Wed/Fri dihitung dari **ET**, BUKAN UTC. Contoh nyata: 10 Agt 01:01 UTC = **Minggu** 21:01 ET → long rule TIDAK berlaku (bukan Mon/Wed/Fri di ET) & short rule juga off (01:01 UTC ∉ 15:00–23:00). Hasil: OFF-WINDOW, no video.
- **INSTRUKSI "short window UTC 15:00-23:00 ≈ ET 19:00-22:00" TIDAK KONSISTEN** (15:00–23:00 UTC = 11:00–19:00 EDT, bukan 19:00–22:00). Terapkan batas eksplisit UTC/ET di atas; JANGAN pakai aproksimasi teks instruksi.
- **OFF-WINDOW (cron fired di luar ke-2 jendela)**: Steps generate/upload/QC **SKIP**. Tapi tetap kerjakan: (1) STEP 1 riset tren fresh → `research/trending_topics.md`; (2) STAGE script + `metadata_qc.json` di `workdir/videos/<TANGGAL>/` untuk topik rank-#1 (siapkan narasi Short/Long); (3) set `video_pipeline_state.json` `status="off_window_prep"` + `next_action` = generate pada run in-window berikutnya. Ini menjaga pipeline siap tanpa buang quota.
- **State file** `workdir/video_pipeline_state.json` = sumber kebenaran lintas-run. Simpan: `run_time_utc`, `window` (on/off + alasan), `day_et`, `primary_topic`, `script_file`, `metadata_file`, `notebooklm_auth` (hasil `auth check --test`), `youtube_token` (path + scope), `last_uploaded_video_id`, dan `video_file`/`uploaded`/`video_id` (null saat off-window). Run berikutnya CEK state dulu sebelum generate (lihat PITFALL WAIT CLAMP di JALUR A2).
- **QC otomatis saat off-window = N/A**; catat di log `logs/pipeline.log` (prepend run-block per run).

### Sumber konten
- **HANYA: NotebookLM** (Jalur A) untuk semua video. Generate via Brave login Bos (computer_use) atau Bos generate manual → `OneDrive/ziyan_pending/`.
- Video pilot sudah ada: `C:\Users\arija\ziyan_notebooklm_short.mp4`.

### ⚠️ PITFALL — Brave GAGAL di-drive computer_use (2026-08-02)
Sesi ini: agent coba buka Brave via terminal `start` / `cmd /c start` / computer_use capture → Brave **tidak muncul di list_windows** & proses mati setelah launch. cua-driver tidak bisa match window Brave (app name apa pun). 
**SOLUSI sementara:** Bos buka Brave MANUAL (klik 2x icon) → login NotebookLM → agent pandu generate via computer_use (kalau window ke-detect) ATAU Bos download manual → taruh di `OneDrive/ziyan_pending/` → agent ambil. Jangan habiskan banyak putaran coba launch Brave otomatis; langsung suruh Bos buka manual. (Catatan: ini mungkin limitasi driver di host ini, BUKAN aturan permanen — retest kalau cua-driver update.)

### Kredensial YouTube Upload (OAuth WEB)
> **STATUS 2026-08-01: UPLOAD SUDAH JALAN (terverifikasi HTTP 200, video ID `HvN-fR1FcLQ`).** Token OAuth valid SUDAH ADA di `ziyan_credentials/youtube_token_compound.json` — berisi `refresh_token` + scope `youtube.upload`, terikat channel **Compound Daily** (`UCzWib2-2CPkWo315fzucaUw`, @compounddaily-v7c). JANGAN cari `./credentials/youtube_oauth.json` (file itu memang tak pernah ada; path di instruksi cron SALAH). Pakai token compound untuk upload publik.
- `ziyan_credentials/google_client_secret.json` = tipe **web** (project `lofty-layout-504106-n4`).
- `ziyan_credentials/youtube_desktop_client.json` = tipe **installed** (client_id `789747689443-qk9ns1v1...`) — dipakai saat menukar/refresh token.
- Upload butuh **refresh_token** (dapat sekali via OAuth flow browser). Cara aman:
  1. Orchestrator generate URL otorisasi → tempel ke chat.
  2. Bos buka di Brave/HP, login `mziyan266@gmail.com`, izinkan YouTube.
  3. Google balikin **authorization code** di address bar → Bos copy ke chat (BUKAN token).
  4. Orchestrator tukar kode → simpan `refresh_token` ke `ziyan_credentials/` lokal (TIDAK lewat chat).
- **METODE UPLOAD TERVERIFIKASI (pakai ini, bukan yt-dlp):** YouTube Data API v3 `videos.insert` via `requests`, multipart/related (metadata JSON + file video). Refresh token dulu (`oauth2.googleapis.com/token`, grant_type=refresh_token, pakai `youtube_desktop_client.json`) → dapat `access_token` → POST `https://www.googleapis.com/upload/youtube/v3/videos?uploadType=multipart&part=snippet,status,contentDetails` dengan header `Authorization: Bearer <access_token>`. Skrip jadi: `scripts/youtube_upload_api.py`. Resep lengkap + verifikasi channel: `references/youtube-upload-api.md`.
- `yt-dlp` (v2026.07.04) sudah terinstall di venv Hermes → `yt-dlp --upload` pakai token (alternatif, tapi API langsung lebih andal).
- Script existing: `nb_proof/youtube_uploader.py` (perlu audit — pakai pickle token + `InstalledAppFlow.run_local_server`, JADI INTERAKTIF & TIDAK HEADLESS). JANGAN pakai untuk cron/otonom.
- **UPLOAD HEADLESS TERBUKTI (2026-08-05):** pakai `ziyan_upload.py` (resep lengkap di `references/youtube-compound-upload.md`): load `ziyan_credentials/youtube_token_compound.json` (refresh_token + scope youtube.upload) + `ziyan_credentials/youtube_desktop_client.json` (nested di `installed.*`), lalu `Credentials.refresh(Request())` → build `youtube("v3")` → `videos().insert(part="snippet,status", media_body=MediaFileUpload(...))`. Tanpa browser. Arg: `--file --title --description --tags --category --privacy`.

### Pitfall YouTube otomatis
- **UPLOAD SUDAH BISA** lewat token di `ziyan_credentials/youtube_token_compound.json` (scope `youtube.upload`, channel Compound Daily). Jangan lagi anggap BLOCKED. Cek validitas tiap run: refresh token → `channels?mine=true` harus 200 & balikin Compound Daily.
- Path `./credentials/youtube_oauth.json` di instruksi cron TIDAK ADA — jangan cari file itu; pakai `ziyan_credentials/youtube_token_compound.json`.
- **TOKEN BISA HILANG (2026-08-15, terbukti):** file `youtube_token_compound.json` bisa terhapus dari disk → upload GAGAL (`FileNotFoundError` / token kosong). **SELALU verifikasi keberadaan file sebelum klaim "upload sudah jalan"** — tiap run: `os.path.exists(path)` + refresh → `channels?mine=true` harus 200 & balikin Compound Daily. Recovery BUTUH Bos (tidak otonom): (1) Hermes bangun OAuth URL dari `youtube_desktop_client.json` (`https://accounts.google.com/o/oauth2/v2/auth?client_id=<id>&redirect_uri=http://localhost&response_type=code&scope=https://www.googleapis.com/auth/youtube.upload&access_type=offline&prompt=consent`), (2) Bos buka, login `mziyan266@gmail.com`, authorize, (3) copy CODE dari address bar (setelah redirect gagal ke localhost), (4) Bos jalankan `python3 ziyan_credentials/reauth_compound.py <CODE>` → tukar code → simpan token → verifikasi channel terikat Compound Daily. Token Celine Aurel (`youtube_token_celineaurel.json`) TERPISAH & tidak memulihkan Compound Daily.
- Shorts 3x/hari rawan **spam flag** YouTube → variasikan topik + jangan identik pixel.
- Niche 4-in-1 terlalu lebar untuk algoritma → pakai rotasi konsisten (lihat jadwal).
- NotebookLM generate >30 mnt → jangan poll, jadwalkan cek via cron.
- **HAPUS video butuh scope `youtube.force-ssl`** — token upload-only (`youtube.upload`+`youtube.readonly`) → DELETE balik **403 Forbidden**. Untuk bisa hapus, re-auth dengan scope tambahan `youtube.force-ssl` lalu tukar code baru.
- Monetisasi YouTube TIDAK cepat: butuh 1000 subs + 4000 jam tayang (YPP) ATAU funnel ke Jalur 1 (AI Service Agency) lewat description/link. Riset "cara cepat cuan" → delegate sub-agent (affiliate + funnel, bukan harap YPP).

## Verifikasi akhir
- File ada di disk + ukuran ~9 MB (NotebookLM, Jalur A).
- Video NotebookLM: **JANGAN** kirim MEDIA: ke chat (simpan di laptop, sesuai instruksi Bos). Kirim MEDIA: hanya bila Bos minta.
- **JANGAN pernah produksi via ffmpeg/pyttsx3/edge-tts** (dilarang Bos, lihat ATURAN MUTLAK di atas).
