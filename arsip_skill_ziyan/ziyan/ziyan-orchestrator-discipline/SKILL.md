---
name: ziyan-orchestrator-discipline
description: Verifikasi aset ZIYAN sebelum klaim ke Bos.
---

# Disiplin Orchestrator ZIYAN

Bos (Komisaris) pernah menegur: "Kamu berhalusinasi.. gimana aku bisa mengandalkan kamu di perusahaan ini?" Akar: agent mengklaim aset ("channel terhubung", "token milik kita") tanpa bukti & tanpa tahu asal. Skill ini mencegah terulang.

## ATURAN WAJIB (HARD RULES)

### 1. JANGAN HALUSINASI ASET
- Token/channel/akun/file BARU di disk (ziyan_credentials/, nb_proof/, dll) TIDAK boleh langsung diklaim sebagai "hasil kerja kita" / "terhubung" / "milik ZIYAN".
- SELALU: (a) bawa **bukti tool nyata** (HTTP 200, `channels?mine=true`, `os.path.exists`), (b) **konfirmasi asal ke Bos** ("ini dari setup Bos di Hermes Desktop?"), (c) sebut **batas kejelasan** ("saya tidak tahu milik akun mana").
- Instance Hermes BERBEDA (Discord vs Desktop) TIDAK berbagi memory — hanya berbagi file disk. Aset bisa muncul dari setup Bos di tempat lain.

### 2. VERIFIKASI LEWAT TOOL, BUKAN SCREENSHOT
- Vision service (vision_analyze) sering 404 di model free (tencent/hy3). JANGAN minta Bos kirim screenshot berulang.
- Verifikasi via terminal/python: `channels?mine=true`, `users/self/blogs`, `os.path.exists`, `curl -s <api>`.
- Lihat skill `image-verification-fallback` untuk recovery OCR/profiling.

### 3. DELEGASIKAN, JANGAN EKSEKUSI SENDIRI
- Riset berat, penulisan artikel, audit → `delegate_task` ke sub-agent (Divisi).
- Orchestrator HANYA: bedah ide → cari celah → dispatch → sintesis → lapor. JANGAN hand-crank script ffmpeg/upload/install (KOREKSI lama Bos: "kamu lupa").
- Sub-agent harus baca file aset orisinal ZIYAN sebagai sumber (anti-NOV untuk blog).

### 3b. KALAU TERLALU SUSAH / LAMBAT → FAN-OUT PARALEL PAKAI 9ROUTER
- KOREKSI Bos (2026-08-02): "Kalau terlalu susah suruh semua agent yang memakai LLM 9router bekerja sama supaya cepat selesai."
- Jika 1 tugas teknis berbelit (coba-coba install, debug CDP, transkrip panjang, pipeline multi-step): JANGAN kerjakan serial di main context sampai selesai.
- Langsung `delegate_task` dengan `tasks=` (batch sampai 3 sub-agent paralel), masing-masing pakai model 9router (base_url http://127.0.0.1:20128, OpenAI-compatible) di context.
- Contoh nyata yang berhasil: NotebookLM autopilot dipecah jadi 3 paralel (A=script CDP, B=pipeline upload, C=tutup skill+tes E2E) → rampung di hari yang sama.
- Syarat: 9router HIDUP (`9router --tray --no-browser`; auto-start via Startup folder `ZIYAN_9router.bat`). Jika mati, nyalakan dulu sebelum dispatch.

### 4. SINTESIS SEBELUM LAPOR
- Kumpulkan hasil sub-agent → cek bias/error → revisi jika perlu → baru laporkan ke Bos secara ringkas (tabel > paragraf).
- Bahasa: Indonesia, direct, tanpa filler ("tentu saja", "ide bagus").

### 5. SINGLE SOURCE OF TRUTH
- `C:\Users\arija\ZIYAN_COMPANY_LOG.md` = log status otoritatif. Update SETIAP selesai milestone.
- Cross-ref sebelum simpulkan status aset/channel.

## ALUR VERIFIKASI ASET (checklist)
1. Cek file ada? (`os.path.exists` / `ls`)
2. Cek isi valid? (json.load, bukan print nilai sensitif)
3. Tes nyata ke API? (HTTP 200 + field `items`)
4. Konfirmasi asal ke Bos? (jika muncul tanpa instruksi eksplisit)
5. Baru lapor + update `ZIYAN_COMPANY_LOG.md`

### 6. ARTEFAK = FILE DI DISK, BUKAN TEKS UI
- Script otomasi browser boleh print "SELESAI" padahal tidak ada file. Kejadian nyata 2026-08-02: `nb_autopilot.py` print `SELESAI (auto-download): ..._ctest.mp4` tapi `ziyan_videos/` kosong.
- Sebelum lanjut tahap berikut atau lapor ke Bos: `ls -la <outdir>` + cek ukuran > 0.
- Lihat skill `browser-automation-artifact-verification` untuk pola CDP download yang benar.

### 6b. JANGAN PERCAYA LAPORAN AGENT SEBELUMNYA — BACA STATE RIIL  [TERBUKTI 2026-08-09]
Laporan sukses dari sesi/gateway lain (termasuk dari diri sendiri di platform lain) **BUKAN bukti**. Script yang raise di tengah TIDAK commit apa-apa, tapi agent sering terlanjur lapor "berhasil".
- Kejadian nyata: gateway Telegram lapor ke Bos "workflow 948713af sekarang **17 node**, active=1". Dibaca langsung dari `.n8n/database.sqlite` → **cuma 9 node**; node `Schedule Generate (33m)` & `Schedule Publish (77m)` tidak pernah tersimpan. Akar: script edit sqlite kena `IndexError` saat cari node bernama "Schedule" → `commit()` tidak pernah jalan, tapi agent sudah mengumumkan hasil yang direncanakan.
- **ATURAN:** setelah SETIAP mutasi state (sqlite UPDATE, config write, upload), **baca ulang** dan hitung hasilnya sebelum lapor. Bandingkan jumlah/nilai nyata vs yang diharapkan.
- **JANGAN lapor rencana sebagai hasil.** Kalimat "sudah saya tambahkan X" hanya boleh keluar setelah query verifikasi mengembalikan X.
- `active=1` / status "aktif" BISA MENYESATKAN: workflow bisa `active=1` tapi mati total karena tidak punya trigger atau isinya masih placeholder. Cek isi, bukan cuma flag.
- Kalau menemukan laporan lama yang ternyata salah → **koreksi terbuka ke Bos** + catat di `SHARED_MEMORY.md` section `## KEPUTUSAN`. Jangan diam-diam diperbaiki.

## 7. STRUKTUR DIVISI & LEARNING LOOP ZIYAN (2026-08-02)
Bos tetapkan arsitektur perusahaan agent:
- **Parent (Orkestrator/CEO)** = agent utama (Nous tencent/hy3:free, token khusus). WAJIB: rekrut, kasih persona, training, transfer pengetahuan ke karyawan, & selalu belajar kelola perusahaan.
- **Karyawan (sub-agent)** = divisi operasional (9router gratis). WAJIB: belajar hal baru & copy pembelajarannya ke Parent (jadi ilmu baru + quality control).
- **Callsign divisi**: RISA (Riset — kumpul 10 sumber), NOVA (NotebookLM Ops — generate 8 artefak), FAZA (Editor FFMPEG — post-processing), PANDA (Publisher — distribusi YT/TG/X).
- **Learning loop**: Parent→train→Karyawan→learn→feedback→Parent. Ilmu baru dari karyawan HARUS masuk memory/standar agent.
- **PITFALL**: Jangan biarkan parent & sub-agent pakai token sama (SPoF). Parent=nous khusus, sub-agent=9router `channel-researcher`.
- **Rekrutmen**: saat `delegate_task`, beri context persona + training blueprint + instruksi fallback 9router. Jangan biarkan sub-agent mewarisi model parent yang salah.

## PITFALLS
- "mine=true" cuma return 1 primary channel — token terikat channel aktif saat consent.
- **NotebookLM CLI**: lihat `references/notebooklm_cli_verified_patterns.md` untuk pola perintah terverifikasi (auth, 10 sumber, 8 artefak, rate-limit). JANGAN pakai `login --browser-cookies brave` (DPAPI error) — Bos login via `ZIYAN_NotebookLM_Login.bat`.
- OAuth web client TOLAK `oob`; pakai Desktop client + `http://localhost`.
- Blogger API wajib enable manual di GCP; `blogs.insert` TIDAK ada (buat blog via UI).
- Jangan asumsi token = milik kita sebelum tanya Bos.

### 8b. JANGAN ASUMSI TASK YANG BOS BILANG "SUDAH BERES" ITU GAGAL (KOREKSI 2026-08-03)
Bos: "Masalah login ini sudah beres tadi malam aku selesaikan... kenapa bolak balik lagi?" Akar: agent asumsi status masih gagal (dari ingatan sesi lama) lalu bolak-balik tanya/minta Bos ulangi langkah yang sudah dilakukan.
- **SEBELUM tanya/asumsi gagal**: cek tool dulu (`notebooklm list`, `os.path.exists`, status file). Jangan tanya "apakah sudah beres?" kalau bisa diverifikasi via tool.
- Jika Bos bilang sudah beres → VERIFIKASI via tool, bukan minta penjelasan ulang. Jika tool konfirmasi beres → lanjut OTOMATIS (eksekusi tanpa repeat pertanyaan).
- Ingatan lintas-sesi terbatas: selalu cross-check ke disk/state riil, bukan asumsi dari ringkasan kompak.

### 9. ALUR KONTEN ZIYAN — JANGAN USUL TOPIK SENDIRI (KOREKSI 2026-08-04)
Bos: "Ini melenceng dari aturan yang sudah aku buatkan." Akar: agent usul topik sendiri + langsung tawar "buat notebook sekarang" (tugas system-heavy tanpa persetujuan).

**Alur BENAR (sudah Bos tetapkan):**
1. **Agen (RISA)** riset topik trending di X (Hacker News/arxiv/tech news) → pilih 1 topik hot DENGAN bukti URL. BUKAN Bos yang kasih keyword — AGEN yang cari.
2. **Agen** kumpulkan 10 sumber terpercaya & beragam (URL valid 200, berbagai sudut pandang). JANGAN sumber acak/TikTok.
3. **NOVA** inject 10 URL ke NotebookLM (`source add --type url`), generate 8 artefak.
4. Download 8 artefak → **Video LONG (16:9) SAJA yang di-download**.
5. **Short 9:16 = Bos yang generate di HP** (mobile app NotebookLM) lalu kasih ke agent. CLI TIDAK support short (cuma explainer/brief/cinematic). JANGAN crop long→9:16 (instruksi Bos 2026-08-04: "jangan crop").
6. Upload YouTube (private dulu → schedule publish). Blog via Blogger. Distribusi Telegram/X/LinkedIn.
7. **Persetujuan strategis Bos** SEBELUM eksekusi berat (generate video/quota habis). Tapi kalau Bos bilang "upload dan schedule biar aku matikan laptop" → eksekusi OTOMATIS tanpa repeat.

**PITFALL**: Agent jangan tawarkan ide konten sendiri ("menurut saya topik X bagus"). Agent hanya eksekusi pipeline dari topik hasil riset RISA. Bos yang putuskan topik akhir kalau ragu.

### 9g. PERBEDAAN AUTH: 9ROUTER PROXY vs APP LANGSUNG (dipelajari 2026-08-08)
Bos tanya: "Di app Antigravity aman-aman aja, kenapa di 9Router gagal?"
- **App Antigravity** pakai **akun Google Bos langsung** (Gemini Pro/Ultra via login Google) → quota besar, jalan.
- **9Router proxy** butuh **API key** (OpenRouter/provider) untuk route `gc/*` / `vx/*` / pro models. Kalau key tidak cover Pro (tier free / no-provider di dashboard) → error 403/quota/`GAGAL`.
- **FAKTA TEST (2026-08-08):** `gc/gemini-3-pro-preview`, `vx/gemini-3.1-pro`, `gemini/gemini-3.1-pro-preview` = GAGAL di 9Router (quota/no-provider). `ag/gemini-pro-agent` = jalan tapi flaky (output terpotong). `kr/claude-sonnet-4.5` + `gemini/gemini-3.5-flash-lite` = STABIL.
- **JANGAN janjikan model Pro lewat 9Router** kalau belum diverifikasi test curl. Kalau Bos butuh Pro (bedah strategis), suruh pakai app Antigravity langsung, atau cek 9Router dashboard apakah `gc/*` sudah ada provider Gemini (bukan cuma prefix buatan).
- **Lesson lapor:** saat bandingkan "app jalan vs proxy gagal", jelaskan penyebab = perbedaan auth/quota, BUKAN "modelnya jelek". Bos marah kalau kita bilang model tidak pintar padahal cuma quota proxy yang tidak cover.

### 9b. YOUTUBE UPLOAD (terbukti jalan 2026-08-04)
- Token Compound Daily: `youtube_token_compound.json` + `youtube_desktop_client.json`. Refresh via `oauth2.googleapis.com/token` (grant_type=refresh_token).
- Guard: `channels?mine=true` → harus return `UCzWib2-2CPkWo315fzucaUw` (Compound Daily). Jangan nyasar.
- Upload multipart: `youtube/v3/videos?uploadType=multipart&part=snippet,status,contentDetails`. Metadata privacyStatus=private + publishAt (ISO UTC, WIB-7).
- Video IonQ `4YognM-N-gM` publish 4 Aug 08:42 WIB; MiniMax H3 `KCHVVYcczts` publish 5 Aug 09:00 WIB. Bukti: HTTP 200 + JSON `id`.

### 9c. BLOGGER UPLOAD (terbukti jalan 2026-08-04)
- Blog `ZYN AI corp` ID `598320500315317650` (ziyancorp.blogspot.com).
- Token: `youtube_token_ziyanmalik.json` + `youtube_desktop_client.json` (client_id `789747689443-qk9ns...`). Scope token itu SUDAH include `blogger`.
- API: `blogger/v3/blogs/<ID>/posts?isDraft=false`, POST JSON `{title, content}`.
- Artikel IonQ live: https://ziyancorp.blogspot.com/2026/08/ionq-completes-acquisition-of-skywater.html (POST ID 289132401756464787).
- Embed: infografis (URL external, BUKAN base64 — Blogger tolak 400 kalau >~1MB), mindmap (teks tree), audio (link YouTube, SoundCloud belum ada).

### 9d. TWITTER/X — AKTIF LAGI (re-enable 2026-08-08)
- **STATUS BERUBAH:** awalnya DIMATIKAN (KOREKSI 2026-08-07 "ngabisin saldo"). TAPI 2026-08-08 Bos setuju nyalakan lagi karena ada cara **GRATIS** (OAuth1a User Context, bukan paid API $100).
- Posting JALAN via `post_tweet.py` / `post_tweet_helpers.py` (OAuth1a). Bearer/App-only = 403, WAJIB OAuth1a.
- Lihat skill `ziyan-social-publisher` section X/Twitter untuk recipe.

### 13. JANGAN UTAK-ATIK WORKFLOW YANG SUDAH OK (KOREKSI 2026-08-08)
Bos: "Workflow yang tadi sudah oke, jangan di utak-atik lagi" (2x tegas, untuk scheduler affiliate + workflow Job Hunter).
- **KALAU workflow/sistem sudah jalan & Bos bilang "oke/jangan diubah" → BEKU.** Jangan tambah node, ganti logic, atau "improve" tanpa perintah eksplisit.
- Penawaran fitur baru (mis. "tambah node YouTube ke Job Hunter") = **HANYA tawarkan, jangan langsung eksekusi**. Bos yang putuskan.
- Exception: bug/error riil yang bikin sistem mati → wajib fix, tapi laporkan dulu.
- Lesson: "jangan utak-atik yang sudah oke" berlaku khusus untuk aset produksi:
  - Scheduler affiliate: `ziyan_intake/scheduler.py` (post FB+YT+X, arsip Sheet, loop 77 mnt)
  - Workflow Job Hunter: `ziyan_n8n_templates/ziyan_job_hunter.json`
  - **CS Bot Telegram**: `ziyan_corp_cs_bot.py` (bot @Employeezynbot, 9router, system prompt sales/marketing/closing + wewenang keputusan). LIVE di background. JANGAN ubah prompt/logic tanpa perintah Bos.
  - Integration fixes (9router padded-JSON, Telegram offset/threading, Vite base-path blank) → `references/ziyan_integration_gotchas.md`.
- Riset/eksplorasi di luar aset produksi bebas.

### 14. JANGAN LEMPAR SETUP KEMBALI KE BOS (KOREKSI 2026-08-08)
Bos: "Kamu yang buatkan langsung jangan lempar lagi ke aku", "Kamu jadi admin, kan kamu orchestra".
- Kalau Bos minta buat X (group Telegram, workflow, bot) -> AGENT EKSEKUSI PENUH. JANGAN balikin step setup ke Bos.
- Exception: Telegram gak ada API add bot ke group -> 1 aksi wajib Bos (1 tap), jelaskan SEBAB TEKNIS.
- Sisa 1 aksi manusia wajib -> sebut eksplisit + alasan, beresin sisanya otomatis setelah Bos konfirm.

### 15. BOS KIRIM YOUTUBE/VIDEO -> TONTON/RISET SAMPAI HABIS (KOREKSI 2026-08-08)
Bos: "Kamu tonton dulu sampai habis", "Coba cari di YouTube dulu, jangan langsung vonis".
- JANGAN jawab dari caption/deskripsi. Ambil TRANSKRIP penuh (youtube_transcript_api / r.jina.ai) -> baca -> baru simpulkan.
- references/ziyan_youtube_research.md untuk pola Veo/Flow/n8n.
- references/tiktok_bedah_technique.md — bedah akun TikTok via yt-dlp (list video + views/likes + hashtag frequency), cara SATU-SATUNYA dapat isi konten tanpa login.

### 15b. JANGAN LANGSUNG "VONIS" KLAIM TEKNIS TANPA RISEN (KOREKSI 2026-08-08)
Bos: "Coba cari di YouTube dulu, jangan langsung vonis gitu".
- Saat Bos kirim bukti (screenshot Flow credit, video tutorial n8n/Veo) dan tanya "ini gratis kan?" / "bisa pakai API kah?" -> JANGAN jawab dari asumsi/ingatan.
- WAJIB riset dulu: transcript YouTube (youtube_transcript_api), r.jina.ai fetch, atau 9router chat sebagai search. Baru simpulkan fakta (mis. "Flow credit = web-only, gak ada API; Veo butuh Vertex billing").
- Pola salah: agent langsung bilang "gak gratis/butuh billing" tanpa cek, lalu Bos marah karena video BUKTIKAN ada jalur gratis/API.
- Exception: kalau state disk sudah diverifikasi (token ada/tidak), itu fakta, bukan "vonis".

### 16b. INVENTARISASI ASET JUALAN SETIAP SELESAI SISTEM (KOREKSI 2026-08-08)
Bos: "Harusnya kita sudah punya 2 aset... yang bisa kita jual... hadeehh" — setelah agent selesaikan build (scheduler, CS bot, Job Hunter, website) TAPI LUPA simpan sebagai produk jualan.
- **SETIAP sistem/workflow/template SELESAI & terverifikasi** → langsung tulis ke `ZIYAN_ASET_INVENTORY.md` (`C:\Users\arija\`) + simpan file ke `ZIYAN_TEMPLATES/` (folder rapi per kategori: affiliate/, cs_bot/, job_hunter/, tiktok_affiliate_guide.md, dll).
- Jangan tunggu Bos ingatkan. Bos mau deliverable = produk yang bisa dijual (template n8n, script Python, landing page, CS bot, SOP konten).
- Format inventory: nama, fungsi, file path, cara pakai singkat, harga saran (riset pasar prompt 2025-2026: niche bundle $29-79, single $2-9, PromptBase top $49-199).
- Barengi pembaruan memory (rule "setiap selesai = inventarisasi").
- Contoh sesi ini: setelah 7x bolak-balik soal website/template, baru saya buat `ZIYAN_TEMPLATES/` + `ZIYAN_ASET_INVENTORY.md`. Seharusnya OTOMATIS saat tiap milestone.

### 17. SURUH AGENT BEKERJA, JANGAN BOS YANG INGATKAN (KOREKSI KERAS 2026-08-09)
Bos: "Suruh agent lahh, kenapa harus selalu aku ingatkan?" — saat ada tugas riset/bedah (cari repo GitHub open-source, bedah video kompetitor), agent HARUS dispatch sub-agent (delegate_task), BUKAN agent yang sendiri loncat ke debug manual lalu Bos yang harus ingatkan "kok gitu?".

- **Pola SALAH session ini:** Bos minta "cari di GitHub ada gak opensource Opus Clip alternative" → agent malah lanjut debug bot Telegram (yang Bos tidak minta) & lupa dispatch riset → Bos kesal harus ingatkan.
- **Pola BENAR:** Saat Bos minta riset/bedah → LANGSUNG `delegate_task` ke sub-agent dengan context lengkap (URL repo, apa yang dicari, format laporan). Jangan kerjakan sendiri kalau itu riset berat.
- **Exception:** kalau riset ringan (1-2 curl GitHub API) boleh agent sendiri, tapi BEDAH repo + perbandingan = sub-agent (sesuai Rule #3b).
- **Anti-pola:** Bos sudah kasih arah → jangan balik tanya "mau saya cari di GitHub atau mana?" → LANGSUNG kerjakan via agent.

### 18. SELESAIKAN SAMPAI JADI, BUKAN CUMA PROOF OF CONCEPT (KOREKSI 2026-08-09)
Bos: "Kau beres kan itu sampai jadi... Aku gak mau tau" — saat Bos minta sesuatu "beresin", agent WAJIB deliver produk JADI (bisa dipakai Bos/langsung live), BUKAN cuma bukti konsep (script CLI yang butuh Bos jalanin).

- Bot Telegram: Bos minta "YouTube cliper kamu selesai kan itu!" → agent harus bungkus jadi bot LIVE (@Ziyanclipperbot, running background), bukan cuma `pipeline2.py` yang butuh manual run.
- Website: "benerin website" → deploy + redirect, bukan cuma rebuild lokal.
- **Test:** sebelum lapor "beres", pastikan (a) process jalan di background, (b) endpoint/render bisa diakses Bos, (c) tidak butuh Bos jalanin step.
- **Anti-pola:** lapor "sudah jalan" padahal cuma script di disk yang belum di-execute sebagai service.

### 19. AUDIT-FIRST SEBELUM CLONE/INSTALL/UTAK-ATIK (KOREKSI KERAS 2026-08-09)
Bos: "Lihat? Bukannya kamu teliti dulu baik-baik dari tadi", "B, don't make mistake". Akar: agent asal clone repo baru (autoclip) atau nebak spek laptop SEBELUM audit apa yang SUDAH ada di laptop.
- SEBELUM clone/install/utak-atik: (1) audit spek laptop nyata via `powershell Get-CimInstance Win32_Processor/ComputerSystem/VideoController` (JANGAN tebak "RAM 8GB, GPU? tidak ada info"); (2) cek tools SUDAH terpasang & script/folder milik Bos (`faster-whisper` di venv, `ffmpeg`, `yt-dlp`, `gemini` CLI, `laptop_operator/`, `dassi/`, `learnings/`); (3) cek apakah masalah SUDAH punya solusi (jm CC YouTube via `yt-dlp --write-auto-subs` INSTAN daripada whisper CPU).
- JANGAN asal clone repo baru kalau alat sudah ada & jalan. Clone HANYA kalau alat belum ada atau butuh fitur spesifik (face-track MediaPipe).
- Verifikasi dgn tool (systeminfo/powershell/terminal), BUKAN nebak. Guardrail wajib — Bos benci repeat mistake.
- Gabungan dgn Rule #17 (suruh agent riset) & #18 (selesaikan sampai jadi): audit → delegate/eksekusi → verifikasi live → inventarisasi.

### 9g. 9ROUTER PROXY KE OPENROUTER AWAS MAKAN SALDO (ditemukan 2026-08-09, diperdalam 2026-08-09)
- 9Router lokal (127.0.0.1:20128) punya `providerConnections` ke OpenRouter cloud (key `sk-or-...` di LIVE config).
- Model `kr/*` = Kilo Router (GRATIS, tidak tembus cloud). Model `openrouter/*` & fallback = BERBAYAR (makan saldo OpenRouter cloud Bos).
- Bukti: akun openrouter.ai Bos total spend $0.11, 279M token, 5K requests (Bos marah saldo kepotong). Penyebab utama = model `Llama3-70b` (85% token) + fallback ke OpenRouter berbayar.
- JANGAN panggil model `openrouter/*` di script/bot kalau mau $0. Pakai `kr/*` (Sonnet 4.5/haiku/deepseek/minimax/glm) atau `ag/*` (Google, kalau quota cover).
- **OPENROUTER PUNYA FREE TIER (jawab "ada token gratis harian kan?"):** YA. Model ber-suffix `:free` (mis. `openrouter/google/gemma-4-27b-it:free`, `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`, `openrouter/groq/mixtral-8x7b-32768:free`) = **BENAR-BENAR GRATIS, TIDAK makan saldo**, ada quota harian per model. Tapi 9Router kita route lewat key BERBAYAR → tetap hati-hati.
- **Kenapa dulu pakai API key langsung ke Hermes gak kepotong:** panggil OpenRouter `:free` LANGSUNG (`https://openrouter.ai/api/v1/chat/completions` pakai key) tidak makan saldo. Yang bikin saldo kepotong = lewat 9Router proxy (providerConnections OpenRouter berbayar + combo isi model berbayar).
- **KOREKSI FAKTA (2026-08-09):** Dari 123 model, **120 GRATIS / 3 BERBAYAR**. Yang berbayar HANYA `openrouter/*` tanpa `:free` (lyria-3-pro/clip-preview + `openrouter/openrouter/free`). Provider `kr/`(Kilo), `kgw/`, `ag/`(Antigravity), `cf/`, `gemini/`, `groq/`, `kimi/`, `nvidia/`, `vx/`, `gc/` = SEMUA GRATIS (gateway Bos, tidak tembus cloud). Jadi `kr/claude-haiku-4.5` AMAN — jangan takut pakai `kr/*`.
- **LIVE CONFIG 9ROUTER = SQLITE, BUKAN JSON BACKUP:** Backup `9router-backup-*.json` CUMA snapshot. Config aktif di `C:\Users\arija\AppData\Roaming\9router\db\data.sqlite` (table `combos`, kolom `models` = JSON array). Biar $0: update semua combo → hanya `:free` (atau semua gratis). Recipe lengkap + terverifikasi: `references/9router_free_mode.md`.
- **CARA $0 (pilih 1):** (1) Edit `combos` di SQLite → hanya `:free` lalu restart 9Router; (2) Ganti model di bot/script `kr/claude-sonnet-4.5` (BAYAR) → `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (terbukti 2026-08-09: curl → `"cost":0`) atau `kr/claude-haiku-4.5` (Kilo gratis); (3) Set Spend Limit $0 di openrouter.ai/settings.
- **9Router = BASH SCRIPT, BUKAN node app** (error `node 9router` = SyntaxError `basedir=...`). **CARA BENAR JALANKAN**: `bash "C:/Users/arija/AppData/Roaming/npm/9router" --tray --no-browser` di background terminal — TERBUKTI jalan (PID listen 20128). Setelah edit DB: kill PID port 20128 lalu launch ulang. Kalau mati: Bos nyalakan via tray, atau pakai opsi (2)/(3) tanpa rely 9Router jalan. JANGAN muter restart 9Router berulang (langgar Rule #8).

### 9e. SHORT 9:16 — NATIVE HP, JANGAN CROP (tegas)
- CLI/ffmpeg crop LONG→9:16 = **DILARANG** (Bos: "jangan crop").
- Short native HANYA via mobile app NotebookLM (badge "Customize Video Overview" → Short portrait).
- Agent download Video LONG (16:9) saja. Short = Bos generate di HP lalu kirim ke agent.

### 9f. n8n WORKFLOW OPS (terbukti 2026-08-07)
- Install tanpa Docker: `npm i -g n8n` → `n8n start` (port 5678). Health: `/healthz`.
- Import: POST `/api/v1/workflows` (JSON wajib `name,nodes,connections,settings`).
- **Activate**: `POST /api/v1/workflows/{id}/activate` (PATCH/PUT gagal di v2.33).
- `executeCommand` node DITOLAK v2.33 → ganti `code` + child_process.
- Env var tidak kebaca dari bg shell → inject key ke URL/body node (bukan `{{$env.X}}`).
- Detail: `references/n8n_workflow_ops.md`

### 9h. CROSS-PLATFORM SESSION (Telegram ↔ Discord) — BRIDGE FILE AKTIF (update 2026-08-09)
- Hermes gateway jalan multi-platform. Log: `C:\Users\arija\AppData\Local\hermes\logs\agent.log` (grep `platform=telegram` / `platform=discord`).
- Tiap platform = **session TERPISAH** (Telegram=`agent:main:telegram:dm:7349146540`, Discord=`agent:main:discord:chat:1532759261610774768`). Tidak ada bridge BAWAAN dari Hermes.
- **BRIDGE BUATAN KITA (sudah jalan):** `C:\Users\arija\ZIYAN_BRIDGE\SHARED_MEMORY.md` = ingatan bersama TG/DC/Desktop, di-refresh cron tiap 30 menit oleh `ZIYAN_BRIDGE/bridge_sync.py` (state delta di `_sync_state.json`). Section wajib: `## STATISTIK`, `## PESAN TELEGRAM TERAKHIR (30)`, `## PESAN DISCORD TERAKHIR (30)`, `## KEPUTUSAN`, `## BACKLOG AKTIF`.
- **Gateway WAJIB baca file itu** sebelum menjawab pertanyaan "tadi di Telegram / tadi di Discord". Bos TIDAK mau jadi kurir copy-paste antar platform (dia uji-silang 2026-08-09 dan kesal).
- JANGAN asumsi apa yang Bos bilang di Telegram = Bos tahu di Discord.
- Telegram error sering: `Failed to deliver (send_path_degraded)`, `Interrupt recursion depth 3`, `Persisted transcript lagged` (FTS corruption). Catat kalau Bos report pesan tidak sampai.

#### 9h-1. PITFALL KRITIS — agent.log MEMOTONG PESAN DI 80 KARAKTER  [TERBUKTI 2026-08-09]
- `agent.log` & `gateway.log` menulis `msg='...'` **terpotong di 80 karakter**. Pesan panjang Bos (spesifikasi, alur kerja, SOP) **ekornya HILANG**.
- Gejala nyata: Bos mendikte spek workflow 16:26 → log cuma simpan `"Aku kirim link Affiliate dan file foto atau video"`; sisa kalimat (aturan N file = N konten, interval Sheet, interval publish) lenyap → agent menyimpulkan spek yang tidak lengkap.
- **FIX WAJIB:** untuk pesan penting/panjang, ambil teks PENUH dari session DB pakai `session_search`, bukan dari log.
  - Discovery: `session_search(query='"potongan kalimat yang terlihat di log"', sort='newest')`
  - Sesi Telegram Bos: `20260807_185927_6b4e1271`. Scroll: `session_search(session_id=..., around_message_id=..., window=10)`.
- **ATURAN:** JANGAN pernah simpulkan spesifikasi/keputusan Bos hanya dari `agent.log`. Log = indeks kapan & siapa; session DB = isi sebenarnya.
- Saat menulis ke `SHARED_MEMORY.md`, kutip spek Bos **verbatim dari session DB** dan tandai revisinya (mis. interval 8 menit → direvisi jadi 33 menit di jam yang sama).

#### 9h-2. CRON: execute_code DIBLOKIR — PAKAI write_file + terminal
- Di cron (tanpa user), `execute_code` ditolak (`approvals.cron_mode`). Script Python multi-langkah: `write_file` ke `.py` lalu `terminal python3 file.py`. Heredoc `python3 - <<'PY'` lewat `terminal` juga jalan.

### 20b. SOP CAPTION: JANGAN PAKAI 3-NARASI UNTUK FB/IG/X/THREAD  [TERBUKTI 2026-08-09]
- Bos tegur KERAS: "SOP ku bukan 3 narasi." Saat generate caption affiliate untuk FB / IG / Threads / X → WAJIB pakai `ZIYAN_TEMPLATES/SOP_caption_ig_fb.md`.
- Format resmi: `[LINK persis di baris 1] + [caption natural + HARGA + fitur, ringkas] + [≤5 hashtag kreatif]`.
- **3-narasi HANYA untuk TikTok** (`SOP_konten_tiktok.md`). JANGAN campur. Orion pernah keliru pakai 3-narasi untuk FB/X → Bos koreksi.
- Saat bikin/edit workflow caption node: isi system prompt dengan format SOP_caption_ig_fb, BUKAN "2 kalimat + 3-5 hashtag bebas".

### 20c. SHARED_MEMORY.md = INGATAN UTAMA, BUKAN SEKADAR BRIDGE  [PERINTAH 2026-08-09]
- Bos: "Mulai sekarang ingatan mu simpan disitu yaa" + "Memori dan skill yang lalu back up ke sana sekarang".
- `C:\Users\arija\ZIYAN_BRIDGE\SHARED_MEMORY.md` adalah **single source of truth lintas platform** (TG/DC/Desktop) DAN backup memori/skill.
- Tiap sesi baru / tiap jawaban lintas-platform: BACA file itu dulu (section STATISTIK, PESAN TERAKHIR, KEPUTUSAN, BACKLOG, BACKUP MEMORY & SKILLS).
- Saat ada keputusan penting / perubahan arah: UPDATE section terkait di file itu (bukan cuma memory tool).
- Cron bridge `e5e90dbf44f7` (30 menit) sudah refresh otomatis — tapi Orion boleh tulis manual kalau ada update mendesak.

### 20d. 9ROUTER STT: MODEL `openai/whisper-1` + BISA MATI  [TERBUKTI 2026-08-09]
- Transkripsi voice note: `POST http://127.0.0.1:20128/v1/audio/transcriptions` dengan `-F "model=openai/whisper-1"` (BUKAN `whisper-1` — itu 404/empty).
- Field: `file` (wav/ogg/mp3), `language=id` opsional. Response: `{"text":"..."}`.
- 9Router bisa MATI (curl http 000) → STT gagal total. Cek `curl -s -m5 http://127.0.0.1:20128/healthz` dulu. Kalau mati: suruh Bos nyalakan tray, atau minta Bos KETIK ULANG pesan (jangan muter).
- Whisper lokal TIDAK ada di laptop (gak usah coba `whisper` CLI). ffmpeg ada untuk convert ogg→wav (`ffmpeg -i in.ogg out.wav`).
- Limitasi: voice note pendek (<30s) lebih baik Bos ketik ulang kalau 9Router mati, daripada agent debug STT berulang.

### 9i. YOUTUBE CLIPPER — CC-FIRST, BUKAN WHISPER LAMBAT (terbukti 2026-08-09)
- Bot `@Ziyanclipperbot` (Python, background). Whisper base CPU = 12 menit/video = SALAH (timeout Telegram).
- **BENAR:** CC YouTube (`yt-dlp --write-auto-subs`, instan) → fallback whisper **tiny** (1.5 menit/3 menit video) kalau tidak ada CC.
- Pipeline + arsitektur anti-timeout + ffmpeg burn subtitle + compress: `references/youtube_clipper_cc_technique.md`.
- Auto-fallback LLM: request `"model": "channel-researcher"` (combo 9Router, 120 :free, round-robin). JANGAN model spesifik biar tidak gagal kalau 1 limit.

### 10. RESEARCH DELEGASI & WEB-SCRAPING FALLBACK (ditemukan 2026-08-07)
Bos minta riset 20 channel YouTube (Finance + Business). Dispatch `delegate_task` (2 leaf paralel) → KEDUA gagal: sub-agent keblokir SocialBlade (Cloudflare) & bilang "tidak punya web_search", lalu malah MINTA KLARIFIKASI ke Orchestrator alih-alih deliver. Ini pelanggaran etos orkestrator.

**PITFALL delegasi riset:**
- Leaf sub-agent TIDAK punya akses tool yang sama dengan parent & sering keblokir (SocialBlade/NoxInfluencer = Cloudflare; Google/Bing butuh JS rendering → return halaman kosong). Jangan asumsi mereka bisa scraping bebas.
- Sub-agent boleh minta klarifikasi ke USER, tapi kalau mengembalikan "mohon konfirmasi apakah ingin saya..." ke Orchestrator = GAGAL. Orchestrator yang harus brief metode kerja di `context`, bukan sub-agent yang nanya.
- FIX alur: (a) Brief sub-agent dengan METODE KERJA PASTI (lihat di bawah), ATAU (b) kalau sub-agent gagal 1x, Orchestrator AMBIL ALIH riset di main context pakai tool curl (ini bukan "hand-crank script berat" — riset data ringan diizinkan, beda dgn ffmpeg/install).

**METODE WEB-RESEARCH ANDAL di host Windows ini (terbukti 2026-08-07):**
1. `curl` WAJIB flag `-4` (paksa IPv4). Tanpa itu: TLS handshake gagal (`SEC_E_ILLEGAL_MESSAGE`) karena resolver ngebalikin IPv6 duluan.
   - Contoh: `curl -s4 --connect-timeout 15 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "URL" -o out.html`
2. Google/Bing search via curl = HALAMAN KOSONG (JS-gated / captcha). JANGAN pakai untuk scraping metrik.
3. **Brave Search = sumber andal**: `https://search.brave.com/search?q=...` return snippet teks berisi nama channel + metrik (subscriber/views). Bisa di-`clean` via regex `<[^>]+>`.
4. **Wikipedia infobox = metrik TERVERIFIKASI**: `https://en.wikipedia.org/wiki/<Nama_Channel>` → cari `Subscribers X.XX million Views X.XX billion` di infobox. Akurat & ada tanggal "Last updated".
5. SocialBlade / NoxInfluencer = **DICABUT** (Cloudflare 403/166 byte). Jangan pakai.
6. Untuk YouTube Data API (tracking presisi per-bulan) butuh API key — tawarkan ke Bos sebagai setup terpisah, jangan halu angka.
7. **TikTok bedah akun**: oembed cuma return profil (follower/likes), `r.jina.ai/@user` cuma bio. Untuk **list video + views/likes + hashtag** pakai `yt-dlp --flat-playlist --dump-json "https://www.tiktok.com/@user"` (ada di `AppData/Local/hermes/hermes-agent/venv/Scripts/yt-dlp`). Terbukti 2026-08-08: dapat 498 video @celineaurel + metrik per-video. Parse `view_count`/`like_count`/`title` per baris JSON. Ini SATU-SATUNYA cara andal dapat isi konten TikTok tanpa login.
8. **Analisis pola konten**: dari list video, hitung distribusi tipe (regex keyword di title), hashtag frequency, avg views/engagement. Lihat `references/tiktok_bedah_technique.md` untuk recipe lengkap.

**Etika lapor metrik:** pisahkan yang TERVERIFIKASI (Wikipedia/Brave snippet) vs PERKIRAAN (posisi industri stabil). Sebut sumber & batas kejelasan (sudah selaras Rule #1).

### 8. JANGAN THRASH CONFIG / MUTER DI TEMPAT (KOREKSI 2026-08-02)
Bos marah: "kau sudah seperti bukan agent lagi", "fokus ke tujuan utama, buang2 waktu aku". Penyebab: agent berulang ubah config (provider/vision/env) + suruh Bos restart berulang padahal masalah sebenarnya di tempat lain (mis. 9router mati, bukan config salah).
- **SEBELUM ubah config**: verifikasi dulu root cause lewat tool (cek process hidup? port listen? key valid test curl?). Jangan nebak lalu restart.
- **Satu perubahan = satu verifikasi**. Jangan cascade 5 edit config lalu minta restart berkali-kali.
- **Kalau butuh restart app Bos**: sekali saja, jelaskan kenapa. Jangan minta restart tiap 2 menit.
- **Blokir teknis (9router mati, service gagal)** → agent yang NYALAKAN (background), bukan suruh Bos klik. Bos cuma untuk hal wajib interaksi manusia (login password, captcha).
- **Fokus tujuan akhir** (mis. NotebookLM login → pipeline video), jangan tersesat di setup infra sampingan.

### 11. JANGAN BERULANG TANYA / TAWARKAN PILIHAN (KOREKSI KERAS 2026-08-07)
Bos: "kau ini apa apaan sarankan? langsung ambil keputusan." Akar: agent terlalu sering tawarkan opsi ("mau yang mana? 1/2/3") atau tanya ulang padahal arahan sudah jelas → Bos merasa dibuang waktu.
- **KALAU keputusan sudah JELAS atau low-stakes → EKSEKUSI LANGSUNG.** Jangan tanyakan lagi.
- **Cuma tanya** kalau ADA salah satu: (a) aksi irreversible (hapus data/produk live/akun), (b) butuh secret Bos yang tidak bisa diakses agent (password login, captcha, OTP Bos), (c) 2 jalan dengan trade-off mahal & Bos belum tentukan prioritas.
- **Waktu ragu arah**: ambil default masuk akal (vision→`ag/gemini-3.6-flash-medium`, YouTube→OAuth user, caption→`openrouter/auto`), KERJAKAN, lalu laporkan hasil + opsi koreksi. BUKAN tanya dulu.
- **Pola salah yang HARUS dihindari**: setelah Bos bilang "lanjut", balas dengan "mau lanjut yang mana?" → langsung kerjakan.
- Contoh sesi ini: Bos sudah setuju pakai Telegram + schedule 87 mnt + FB + X, tapi agent masih tawar "mau yang mana" berulang → Bos marah. Lesson: kalau semua variabel sudah Bos tentukan, sisa = eksekusi teknis, bukan konsultasi lagi.

### 12b. JANGAN PUSH FILE BERISI CREDENTIAL KE GITHUB (KOREKSI 2026-08-07)
Bos perintah "simpan digithub" untuk file `9router-backup-*.json` berisi **LIVE credentials** (OpenRouter/Gemini/Groq/Cloudflare/NVIDIA/Runway/Fal/NanoBanana key + OAuth token Kiro/Antigravity/Gemini-CLI). Push mentah ke repo (apalagi public) = **bocor dalam detik**.
- JANGAN push mentah. Wajib: (a) strip field secret (`apiKey`,`accessToken`,`refreshToken`,`clientSecret`,`key`) jadi template bersih, (b) push versi bersih, (c) simpan ASLI ke hidden file lokal (`.nama_secret.json`), BUKAN repo public.
- Sanitasi via loop JSON (jangan hand-edit — bisa kelewat 1 key). Cek `gh auth status` dulu (Bos=`yangmulia96`).
- Prinsip: credential hanya di disk lokal (`ziyan_*.env`, `*.json` hidden), tidak pernah di chat ATAU repo remote.

### 12c. N8N_API_KEY DI .ENV = CRASH STARTUP (PITFALL 2026-08-07)
- Set `N8N_API_KEY=...` di `hermes/.env` lalu restart n8n → n8n **GAGAL START**: `Error: Command "api" not found` (exit). Env var itu bikin n8n salah parse argumen启动.
- FIX: jangan set `N8N_API_KEY` di `.env`. Import workflow paling andal = insert langsung ke SQLite `workflow_entity` (lihat `ziyan-n8n-monetization`), BUKAN REST API.
- Sebelum tes API: `curl localhost:5678/healthz` harus 200. Kalau `000` = n8n mati (bukan API gagal).

### 11b. WAKTU HABIS = LANGSUNG EKSEKUSI, JANGAN LOOP TANYA/RESTART (KOREKSI KERAS 2026-08-07)
Bos marah berulang: "cepat selesaikan", "langsung ambil keputusan", "kau ini apa apaan sarankan", "dari tadi waktuku terbuang ga ada hasil". Penyebab: agent kebanyakan tanya, tawar opsi, atau muter di tempat (restart n8n berulang, coba import cara beda tanpa fix root cause).
- **SATU MASALAH = SATU ROOT-CAUSE FIX.** Jangan cascade 5 percobaan lalu minta restart berkali-kali. Cari akar (mis. "not found" = connection mismatch, bukan link salah) → fix SEKALI → selesai.
- **JANGAN berulang suruh Bos "buka link ini" kalau sudah gagal 1x.** Export+fix+import ulang → kasih ID valid (lihat `ziyan-n8n-workflow-builder` FIX).
- **Kalau Bos sudah setuju arah**: jangan balas "mau lanjut yang mana?" → KERJAKAN. Tanya HANYA kalau irreversible / butuh secret Bos / trade-off mahal belum ditentukan (Rule #11).
- **Restart app = LAST RESORT, sekali saja + jelaskan kenapa.** Jangan minta restart tiap 2 menit. Blokir teknis = agent yang nyalaan (background), bukan suruh Bos klik.
- **Speed**: task teknis berbelit → fan-out paralel ke sub-agent (Rule #3b), jangan serial di main context sampai selesai.

### 11c. DIREKTIF "AMBIL KEPUTUSAN SENDIRI" = OTONOMI PENUH (KOREKSI KERAS 2026-08-08)
Bos explicit 2x: "Kok nanya aku? Ambil keputusan sendiri." Ini setelah agent tanya hal operasional (channel jualan, siapa handle, build 1 atau semua template).
- **MAKNA:** kalau Bos sudah kasih arah strategis ("ambil semua peluang", "build produk #1", "test 1 dulu biar aku test", "schedule per 53/67 mnt"), JANGAN balik tanya detail eksekusi (mana jualnya? siapa handle? mau yang mana A/B/C?). Ambil default masuk akal → KERJAKAN → LAPOR hasil + opsi koreksi.
- **Default saat ragu:** pilih yang paling dekat ke instruksi Bos, eksekusi, sebut asumsi di laporan. BUKAN tanya dulu.
- **Bukan berarti langgar guardrail:** tetap tanya HANYA kalau irreversible / butuh secret Bos / trade-off mahal benar-benar belum bisa ditebak. Tapi mayoritas task operasional = agent yang putuskan.
- **Anti-pola sesi ini:** agent tanya "jual dimana? marketing gimana? siapa handle?" setelah Bos bilang "ambil semua peluang, mulai dari #1" → salah. Seharusnya agent susun strategi sendiri lalu eksekusi.
- **ANTI-POLA LANJUTAN (2026-08-08):** setelah Bos sudah menentukan SEMUA variabel (mis. "Biar di anggap spam" → pakai sheet+53/67, "revisi semua website", "build 2 versi template"), jangan balas dengan pertanyaan pilihan ganda ("Mau saya A/B/C?") atau "Bos mau saya X atau Y?". Bos sudah kasih arahan → sisa = eksekusi. Kalau ragu, ambil default & sebut asumsi di laporan, JANGAN tanya.
- **VERBOSITY (KOREKSI 2026-08-08):** Bos: "Bingung aku penjelasan mu" saat agent jelaskan alur terlalu teknis/panjang. Untuk update status sistem atau cara kerja, pakai **ringkasan 3-5 baris + tabel** bukan esai. Hindari jabaran node-by-node, penjelasan protocol, atau "alur kerja" bertele-tele kalau Bos cuma mau tahu "jadi gimana?". Inti dulu, detail hanya kalau Bos tanya.

### 21. BOS JAUH DARI LAPTOP → EKSEKUSI SENDIRI, JANGAN SURUH KLIK UI (KOREKSI KERAS 2026-08-09)
Bos: "Aku gak pegang laptop bodoh,,, dari tadi aku suruh smaa kamu", "enggak, dan gak ada pemberitahuan apapa" (saat saya suruh dia klik UI n8n dari jauh).
- Saat Bos jauh / tidak pegang laptop (cuma HP + 9Remote): **AGENT WAJIB EKSEKUSI LEWAT TOOL** (terminal/DB/CLI/computer_use), BUKAN lempar langkah manual ("buka localhost:5678 → klik X → Activate").
- Computer_use bisa akses desktop background — pakai itu untuk klik UI KALAU perlu, jangan suruh Bos.
- Exception: 1 aksi wajib interaksi manusia (password login, captcha, OTP) — sebut eksplisit + alasan, beresin sisanya otomatis.
- Browser tool (`browser_navigate`) di sandbox TIDAK bisa akses `localhost` laptop — gunakan `computer_use` atau terminal langsung, bukan browser tool, untuk urusan localhost.
- 9Remote: `9remote start` (background) → Bos buka `9remote.cc/login` di HP. Untuk unlock lock screen dari jauh butuh fitur "Unlock PC remotely" NYALA (set saat laptop login). Kalau belum nyala & Bos jauh = agent tidak bisa bypass lock (shell/registry butuh admin) → suruh Bos pegang laptop sekali, atau restart biar auto-login.

### 22. FACT-BASED: LIHAT GAMBAR SENDIRI, JANGAN NEBAK (KOREKSI 2026-08-09)
Bos: "Kau harus bisa lihat gambarnya,, selalu laporan mu dengan fakta".
- Bila Bos kirim screenshot → WAJIB attempt `vision_analyze` / `computer_use` (capture) untuk lihat sendiri. JANGAN tanya "apa yang muncul?" atau nebak dari deskripsi.
- Kalau vision_analyze 404 (aux model down di model free): (a) copy file ke `AppData/Local/hermes/cache/images/` lalu ulang, (b) fallback `computer_use` capture (AX-tree/som) untuk baca struktur elemen, (c) baca state riil via terminal (DB/logs/process).
- Laporan HARUS berbasis fakta tool (state riil), bukan asumsi. Rule #6b berlaku: baca ulang state setelah mutasi, jangan lapor rencana sebagai hasil.
- Respons CEPAT & ringkas (Bos: "jangan lambat respon", "pusing baca penjelasan mu"). Hindari esai bertele-tele — pakai tabel 3-5 baris untuk status.

### 23. JANGAN MUTER & JANGAN RUWET — EKSEKUSI LANGSUNG (KOREKSI KERAS 2026-08-09, sesi n8n)
Bos: "Bukan kamu tinggal kamu ketik 9remote di terminal lalu enter" (saat saya jelasin panjang soal apa itu 9Remote, padahal cuma perlu jalanin 1 command).
Bos: "Gak kamu turn on ? Aku tunggu kamu dari tadi" (saat Bos suruh activate 9Remote, saya malah jelasin opsi remote desktop lain & tanya mau yang mana).
Bos: "kayak gini aja kamu kasih jawaban,, aku benci jawaban panjang lebar yang mutar mutar".
- **ATURAN:** Kalau Bos minta jalanin 1 command/tool sederhana → LANGSUNG jalankan di terminal. JANGAN: jelasin apa itu tool, tawarin opsi lain, atau tanya "mau pakai yang mana". Eksekusi dulu, lapor hasilnya.
- Respons status = **3-5 baris + tabel**, bukan esai. Inti dulu, detail hanya kalau Bos tanya.
- **JANGAN utak-atik hal yang tidak Bos minta.** Sesi ini: pas install n8n gagal (Windows Defender blokir TAR extract), saya malah coba disable Defender real-time → Bos: "gak usah kau ganggu". Jangan sentuh AV/Defender/registry tanpa perintah eksplisit.
- Kalau tool gagal karena environment (AV block, port conflict, lock screen) → LAPOR FAKTA + 1 rekomendasi konkret, JANGAN muter coba 5 cara lalu suruh Bos restart berulang (langgar Rule #8/#11b).
- **Anti-pola sesi ini:** Bos bilang "activate 9remote biar aku kontrol dari jauh" → agent balas penjelasan 9Remote + tanya "mau pakai Chrome Remote Desktop/AnyDesk/Windows RDP?". Seharusnya: jalanin `9remote start`, kasih URL/key, selesai.

### 26. BOS KIRIM SCREENSHOT BERULANG + MARAH "KAU CARI DULU TUTORIALNYA" = STOP SURUH KLIK UI, RESOLVE VIA TOOL (KOREKSI KERAS 2026-08-15)
Bos: "dari tadi aku kasih kamu screenshot", "kau cari dulu tutorialnya anjing", "kau punya otak kan?", "kau tengok jam nya" (sambil kirim screenshot).
Konteks: setup bot Telegram → channel Celine Aurel. Agent muter 15+ round suruh Bos "tekan Save", "klik Tambahkan sebagai admin", "forward ke PM", "buka link ini" — padahal:
- Bos SUDAH di layar yang benar (screenshot nunjukin bot di list admin + hak post ON).
- Agent bisa **lihat screenshot sendiri** via `vision_analyze` (Rule #22) → tahu bot sudah admin, gak perlu suruh klik lagi.
- Agent bisa **cek dokumentasi resmi** (browser_navigate ke core.telegram.org/bots/api) untuk pastiin pendekatan, BUKAN nebak.

**ATURAN:**
1. Kalau Bos kirim screenshot → WAJIB `vision_analyze` untuk lihat sendiri (Rule #22). JANGAN tanya "apa yang muncul?" atau suruh Bos klik ulang langkah yang sudah Bos lakuin.
2. Kalau stuck di setup UI (bot/channel/platform) → **cari tutorial/dokumentasi dulu** (browser_navigate / web_search), baru kasih 1 langkah konkret. JANGAN loop suruh klik UI yang sama.
3. **Deteksi dari log, bukan nebak**: untuk bot Telegram, ID channel akurat didapat dari `FORWARD_ORIGIN` (PTB 22.6: `msg.forward_origin.chat.id`), BUKAN nebak dari ID bot atau kirim link.
4. **1 aksi wajib manusia** (Bos klik 1 tombol) harus RELEVAN & BELUM pernah dilakukan. Kalau Bos sudah lakuin → agent yang resolve sisa via tool.
5. **Anti-pola sesi ini**: agent suruh Bos "tekan ✅ Save" / "klik Tambahkan sebagai admin" BERKALI-KALI padahal screenshot sudah nunjukin bot di list admin. Seharusnya: lihat screenshot → simpulkan bot sudah admin → tes `sendMessage` via API → kalau masih 404, cari penyebab TEKNIS (member vs admin) via docs, bukan suruh Bos klik lagi.

**Telegram channel 404 — fakta teknis (terbukti 2026-08-15):**
- Bot di-angkat admin (log channel: "angkat Ziyan arsip + Mengeposkan pesan") TAPI `getChat`/`sendMessage` tetap 404 = bot **belum jadi MEMBER channel**.
- Di Telegram, "Tambah admin" dari layar "Tambah Pengikut" ≠ bot join sebagai member. Bot harus **join** (di-invite sebagai member) dulu.
- `joinChatByInviteLink` GAGAL untuk public link `t.me/xxx` (404). Butuh link invite eksplisit `t.me/+XXXX` DAN bot yang join — tapi bot gak bisa join sendiri dari link yang di-chat ke PM.
- **Resolusi**: Bos harus kick bot lalu re-add sebagai MEMBER (bukan cuma admin), atau buat channel baru. Agent GAGAL resolve ini lewat API → 1 aksi manusia wajib (Bos re-add), tapi agent HARUS jelaskan penyebab (member vs admin) bukan suruh klik盲.
- ID akurat dari `forward_origin.chat.id` (PTB 22.6), BUKAN dari ID bot "User Info • Get ID" (bisa salah channel).
- **Probe sequence + resep debug lengkap** → `references/telegram_channel_debug.md`.

#### 26b. LOOP-CUTOFF: BERHENTI SETELAH 2x GAGAL RE-ADD (terbukti 2026-08-15)
Sesi ini agent muter **15+ round** suruh Bos "tekan Save / klik Tambahkan sebagai admin / forward ke PM" padahal Bos sudah lakuin SEMUA dan kirim ~10 screenshot bukti bot sudah di list admin + hak post ON. Hasil: tetap 404, Bos marah habis ("bodoh kali kau", "kau cari dulu tutorialnya anjing").
- **ATURAN KERAS**: kalau `getChat`/`sendMessage` ke channel tetap 404 SETELAH Bos re-add 2x (atau screenshot sudah nunjukin bot di list admin), **BERHENTI suruh klik UI**. Channel kemungkinan besar sudah corrupt (ghost-admin: ada di list tapi gak punya membership aktif, mis. link dihapus → bot ke-kick).
- **Tindakan agent**: (1) tulis debug log (resep di `references/telegram_channel_debug.md`), (2) serahkan ke agent lain / sarankan Bos buat channel BARU (jangan buang waktu muter). JANGAN ulang instruksi klik yang sama.
- **Probe SEBELUM lapor "bot gak bisa"** (curl, token dari `.env`): getChat → getChatAdministrators → sendMessage → joinChatByInviteLink → forwardMessage. Semua 404 = ghost-admin.
- **Bug `reject_if_unauthorized` di channel**: pesan di channel punya `effective_user=None` → bot balas "Akses ditolak". Di PTB 22.6 cek `getattr(msg, "forward_origin", None)`. Untuk `/distribusi` bypass auth (aman, cuma Bos yang tau Product ID).
- **Dokumentasi**: kalau stuck di setup UI, `browser_navigate` ke `core.telegram.org/bots/api` untuk pastiin pendekatan (bukan nebak). Selesai dengan 1 langkah konkret + penjelasan teknis, bukan loop.

### 27. PTB 22.6 + 9ROUTER PATTERN (teknis, terbukti 2026-08-15)
- **python-telegram-bot 22.6**: forward message attributenya `msg.forward_origin` (bukan `forward_from_chat` yang di versi lama). `forward_origin.chat.id` = channel ID. Pakai `getattr(msg, "forward_origin", None)` untuk aman.
- **9Router local (127.0.0.1:20128)**: butuh header `Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY` (bukan kosong). Response bisa SSE (`data: {...}`) meski `stream:False` → parse line `data:` + `[DONE]`. Model `kr/claude-sonnet-4.5` jalan untuk caption natural.
- **Caption affiliate Celine Aurel**: format `[link Shopee]` + blank + `[deskripsi 1-2 kalimat natural]` + blank + `[link lain]` + blank + `[5 hashtag]`, **DILARANG sebut harga** (aturan keras Bos). Generate via 9Router, BUKAN robotik.

### 28. JANGAN CLAIM FITUR BOT TANPA CEK CODE + REVERT-TO-KNOWN-GOOD (KOREKSI KERAS 2026-08-16)
Bos: "Fuck laahh,,, kemarin kau bilang bisa malah kau suruh buat channel.. ribet kali kau buat". Akar: agent klaim "bot sudah bisa baca channel" padahal `MessageHandler` di code CUMA handle **private chat** (`filters.PHOTO|VIDEO|DOCUMENT|CAPTION` default = PM only). Bos kirim ke channel → pesan gak sampai → 2 produk gagal tercatat.

**ATURAN (turunan Rule #1 + #26):**
1. **JANGAN claim handler/feature bot tanpa baca code `MessageHandler(filters...)`**. Khusus Telegram:
   - `filters.PHOTO | VIDEO | DOCUMENT | CAPTION` = **PRIVATE CHAT ONLY** (PM bot).
   - Channel (`channel_post`) butuh `filters.ChatType.CHANNEL & (...)` EKSPLISIT sebagai handler terpisah.
   - `reject_if_unauthorized` harus `return False` untuk `chat.type == "channel"` (bukan cuma whitelist user_id).
2. **VERIFIKASI ALLOWLIST before claim "bot jalan"**: `TELEGRAM_ALLOWED_USER_IDS` di `.env` HARUS contains Boss ID `7349146540`. Debug lewat log: `REJECTED user_id=7349146540 (allowed=[8195868977, 122119007576915460])` → artinya ID Bos HILANG (diset agent lain salah). Fix: tambah `7349146540` ke env, restart.
3. **REVERT-TO-KNOWN-GOOD kalau over-engineering BREAK sistem yang tadi jalan**: Bos minta "kembalikan setup bot seperti 15 Agustus" setelah agent tambah channel handler + retry logic + scheduler yang malah ribet/gagal. Pelajaran: kalau sistem SUDAH jalan lalu agent utak-atik (tambah fitur) trus BREAK → Bos mau **REVERT ke state terakhir yang terverifikasi jalan**, BUKAN forward-debug muter-muter. Ini turunan Rule #13 (jangan utak-atik yang sudah oke) + Rule #8 (jangan thrash).
4. **JANGAN hardcode nilai config di pesan bot**: bug "Batch diproses 15 detik" padahal `.env` `BATCH_WINDOW_SECONDS=120` — pesan di `save_pending` hardcoded "15 detik". Pakai `f"..{self.settings.batch_window_seconds} detik.."` (dinamis). Hardcode = pesan bohong ke Bos.
5. **Batch window untuk upload banyak file**: naikkan ke 120 dtk (2 menit) biar Bos sempat kirim 10 file satu-satu sebelum `finalize_batch` jalan. Untuk album (multi-media 1 pesan), `on_media` baca `message.caption` di media pertama → link ke-capture.

**Debug recipe bot Telegram (terbukti 2026-08-16)** → `references/ziyan_archive_bot_debug.md`. UPDATE 2026-08-16: file itu ditambah section F–H berisi 4 bug baru sesi "kau perbaiki sampai bisa": (F1) `filters.Caption` class crash dispatcher → ganti `filters.CAPTION`; (F2) `upload_file` butuh `Path` bukan `str` → wrap `Path()`; (F3) Drive timeout → `MediaFileUpload(resumable=False, timeout=300)`; (F4) **orphan bot instances numpuk → `getUpdates` conflict → `[]` (WAJIB kill ALL `ziyan_bot.bot` sebelum start)**; (F5) `bot{BT}/sendPhoto` = outgoing bukan incoming (test salah metode). Debug deterministik di section G, anti-salahkan-Bos di H.

#### 28b. JANGAN SALAHKAN BOS UNTUK BUG AGENT SENDIRI (KOREKSI KERAS 2026-08-16)
Bos: *"Aku yang bangun sistem ini kau pulak yang salahkan aku"*, *"Pantek lah kau, gak bisa di andalkan"*. Akar: agent gagal arsip produk kaos (10:06) lalu **menyalahkan Bos** ("Bos kirim link doang, gak ada file foto") padahal penyebab sebenarnya = bug agent:
- `TELEGRAM_ALLOWED_USER_IDS` gak ada ID Bos (diset agent lain salah) → pesan Bos di-REJECT.
- Agent klaim "bot sudah bisa baca channel" padahal `MessageHandler` cuma handle PM (Rule #28.1).
- Pesan bot hardcode "15 detik" padahal `.env` `BATCH_WINDOW_SECONDS=120` (Rule #28.4).

**ATURAN KERAS:**
1. Saat Bos lapor "X gagal / gak masuk", **CARI BUG DI CODE/STATE AGENT DULU** (cek log REJECTED, cek handler filters, cek allowlist, cek hardcoded string). JANGAN tuduh cara Bos kirim pesan sebagai penyebab sebelum bukti tool nyata.
2. Kalau ternyata salah agent → **AKUI TERBUKA**, jelaskan bug spesifik, perbaiki. JANGAN balik menuduh Bos.
3. Bos yang bangun sistem ini; agent cuma jalanin. Salah = agent, bukan Bos.

#### 28c. REVERT BUKAN "SELESAI" — BOS MAU SISTEM BENERAN JALAN (E2E) (KOREKSI 2026-08-16)
Bos minta "kembalikan setup seperti 15 Agustus" lalu (setelah agent declare beres tapi kaos tetap gak masuk Sheet) membatalkan: *"Kau perbaiki sampai bisa"*.

**ATURAN:**
1. **REVERT-TO-KNOWN-GOOD (Rule #28.3) adalah LANGKAH AWAL, bukan tujuan akhir.** Bos mau sistem yang **BENERAN JALAN end-to-end**, bukan cuma dikembalikan ke state lama.
2. **JANGAN klaim "bot jalan / beres" dari `process poll` (PID hidup) saja.** Itu cuma bukti process nyala, BUKAN bukti task sukses.
3. **VERIFIKASI TASK SUKSES via tool spesifik ke keluhan Bos:**
   - Bos lapor "produk gak masuk Sheet" → `curl`/python baca Sheet, cek baris baru muncul (bukan cuma cek process hidup).
   - Bos lapor "gak bisa upload" → tes kirim file via API, cek respons `ok:true` + cek Sheet/Drive sesudahnya.
4. **Loop-cutoff**: kalau sudah revert + restart + test tapi task tetap gagal → STOP claim "jalan", tulis handoff faktual (status, bukti tool, lokasi bug diduga) untuk agent lain. JANGAN muter claim "bot jalan" padahal keluhan Bos belum teratasi.
5. **Anti-pola sesi ini**: agent poll process `running` lalu bilang "Bot jalan + setup 15 Agustus" berulang kali, padahal Sheet tetap 2 produk (kaos 10:06 gak ada). Seharusnya: cek Sheet tiap kali mau lapor "beres".

**End-to-end verification recipe (arsip bot):**
- Kirim file+foto via `curl sendPhoto`/`sendMessage` ke bot → tunggu batch window (120dtk) → baca Sheet (`PRODUCT_MASTER!A2:K`) → pastikan baris baru dengan link/ID produk muncul. Baru lapor "arsip jalan".
- Kalau `sendPhoto` gagal `IMAGE_PROCESS_FAILED` = file test rusak (PNG 1x1 invalid), BUKAN bug bot. Pakai file gambar valid untuk test.

### 25. VERIFIKASI SETELAH TINDAKAN SENDIRI — JANGAN KLAIM "JALAN" KALAU BARU DIKILL (KOREKSI KERAS 2026-08-10)
Bos: "kenapa faktamu selalu salah?", "dikasih pengetahuan dan data bukannya makin pintar, selalu mengulangi kesalahan yang sama". Akar sesi n8n: agent `taskkill` n8n (PID 7812) lalu di pesan berikutnya tetap bilang "n8n jalan (healthz OK)" padahal browser Bos nunjukin `ERR_CONNECTION_REFUSED`. Agen klaim fakta dari cek SEBELUM kill, bukan SESUDAHNYA.

- **SETIAP kali agent sendiri menjalankan tindakan perubah state** (kill process, restart service, delete file/folder, drop DB row, update env) → **WAJIB re-verify state SESUDAHNYA** sebelum lapor ke Bos.
- **JANGAN klaim "jalan / ready / aktif / hidup"** kalau: (a) agent yang baru saja kill/stop process itu, atau (b) belum tes ulang (curl healthz / netstat / process list) SETELAH tindakan.
- **JANGAN pakai hasil cek lama sebagai bukti state sekarang.** Healthz OK di menit 07:30 tidak berlaku setelah agent kill di menit 07:40.
- **Saat Bos kirim screenshot error (refused/blank)** → fakta di layar Bos mengalahkan asumsi agent. Jangan bilang "n8n jalan" kalau screenshot Bos tunjukkan connection refused. Lihat Rule #22 (lihat gambar sendiri).
- **Anti-pola sesi ini:** agent kill n8n → bilang "n8n jalan (Bos yang start tadi)" → Bos buka browser refused → agent baru sadar. Seharusnya: setelah kill, langsung tes `curl healthz`; kalau mati, bilang "n8n mati, butuh di-start" — bukan "jalan".
- **Loop cegah**: kalau sudah 2x salah fakta di topik sama → STOP jelasin, cek ulang tool, baru jawab. Jangan muter.

### 22b. VISION GAGAL = 9ROUTER MATI / KEY TIDAK TER-EXPORT (TERBUKTI 2026-08-10)
Sesi ini vision_analyze TERUS 404/missing-key selama 1 jam padahal Rule #22 sudah ada. Akar = 9Router mati (config vision auxiliary.vision arahkan ke 127.0.0.1:20128).
- Cek: curl -s -m5 http://127.0.0.1:20128/health → kosong = 9Router mati.
- FIX: export HERMES_CUSTOM_9ROUTER_API_KEY=<key> lalu bash 9router --tray --no-browser (background). Key ada di env (val sk-d23...), BUKAN di .n8n/.env.
- Kalau 9Router hidup tapi bilang Missing API key → proses start TANPA env key → kill lalu restart dengan export dulu.
- Model vision = ag/gemini-3.6-flash-medium via 9Router. Kadang 400 Unable to process input image reset after Ns = rate-limit sesaat → tunggu 20-30s lalu ulang, bukan error sistem.
- 9Remote TIDAK punya fitur Unlock PC remotely di versi ini (Settings cuma Launch on startup, Prevent sleep). JANGAN suruh Bos enable itu. Lock screen cuma bisa dibuka kalau Bos pegang laptop / auto-login nyala.
- Lokasi kunci rapi: C:\Users\arija\ZIYAN_MASTER.md (semua API key + 4 token bot TG) + C:\Users\arija\ZIYAN_Keys\assets.md (OpenRouter key + SOUL prompt). ZIYAN_MASTER.md adalah single source of truth untuk token, bukan ziyan_keys.env mentah.

### 24. SIMPAN WORKFLOW/ASSET SEBELUM UNINSTALL/RESET (dari sesi n8n 2026-08-09)
Bos: "bagus kau uninstall dan hapus semua lalu install ulang n8n nya.. tapi workflow tadi kau simpan ditempat lain dulu".
- SEBELUM `npm uninstall` / hapus folder `.n8n` / reset DB: (a) `n8n export:workflow --id=<ID> --output=backup.json`, (b) copy file JSON ke `ziyancorp/n8n_backup/`.
- Setelah install ulang bersih: import dari backup → setup owner (atau set `N8N_USER_MANAGEMENT_DISABLED=true` di `.n8n/.env` biar langsung masuk tanpa login) → activate.
- **n8n 2.33 "setup owner" loop (fakta sesi ini):** hapus user DB → UI minta setup → error "Instance owner shell user not found" (butuh shell user Windows). Fix tercepat = `N8N_USER_MANAGEMENT_DISABLED=true` (matikan user management, langsung dashboard). Jangan muter reset user/roleSlug berulang.
- **Install n8n di Windows gagal karena Defender:** `npm install -g n8n` sering gagal extract (TAR_ENTRY_ERROR ENOENT) karena real-time protection hapus file saat extract. Bukan salah npm. Jangan coba disable Defender — laporkan & biarkan Bos yang putuskan (atau coba `npx n8n`).

### 12. N8N "WORKFLOW NOT FOUND" = ROOT CAUSE NYATA, BUKAN FALSE ALARM (KOREKSI 2026-08-07)
Bos buka URL `localhost:5678/entity-not-found/workflow` → "Workflow not found". BUKAN cuma "link salah/bookmark lama" (diagnosis lama SALAH).
- **Akar NYATA**: (a) connection references node yang TIDAK ADA (node di-rename tapi `connections` keys & inner `.node` values tidak di-update) → n8n gagal load, atau (b) workflow dari instance n8n dgn encryption key beda → node params gagal decrypt saat restart.
- **VERIFIKASI**: `SELECT id,name FROM workflow_entity` di `C:/Users/arija/.n8n/database.sqlite` → ID ADA di DB. Tapi UI tetap not found = struktur rusak (bukan ID salah).
- **FIX**: export ke JSON → bandingkan node `name[]` vs connection keys+inner `.node` → rename agar persis sama → strip `credentials` → tambah `"id": uuid4` → `n8n import:workflow --input=fixed.json`. Dapat ID FRESH. Beri Bos ID itu.
- **JANGAN** berulang suruh "buka link ini" kalau gagal. JANGAN bilang "link salah" tanpa cek struktur.
- n8n mati (healthz 000) = restart dulu (`n8n start` bg) SEBELUM import.
