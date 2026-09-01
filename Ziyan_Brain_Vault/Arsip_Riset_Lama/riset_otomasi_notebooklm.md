# Riset: Agent Generate Video NotebookLM Secara Mandiri (ZIYAN / Compound Daily)
Tanggal riset: 2026-08-01 · Status: riset saja, TIDAK ada eksekusi

## Ringkasan Eksekutif
**Ada jalur yang jauh lebih baik dari computer_use.** NotebookLM memang tidak punya
API publik resmi, TAPI komunitas sudah reverse-engineer RPC internal `batchexecute`
(RPC yang dipakai web app sendiri). Library paling matang: **`notebooklm-py`**
(18k★, MIT, di PyPI) — punya perintah `generate video`, `download video`, dan
**auth headless via master token** (satu kali login manusia, lalu berbulan-bulan
tanpa browser). Ini = jalur paling feasible untuk agent 100% mandiri, tetap pakai
mesin NotebookLM asli (kualitas Video Overview terjaga).

---

## JALUR 1 — `notebooklm-py` (unofficial Python API + CLI) ⭐ REKOMENDASI UTAMA
- Repo: https://github.com/teng-lin/notebooklm-py · PyPI: `pip install notebooklm-py`
- Pakai **undocumented internal Google API** (bukan scraping DOM) → cepat & tahan rebrand UI.
- Fitur relevan:
  - `notebooklm create "<judul>" --use` — buat notebook
  - `notebooklm source add-research "<query>" --mode deep --from web --import-all --cited-only`
    → **cari sumber otomatis + impor otomatis** (persis langkah yang sekarang Bos kerjakan manual)
  - `notebooklm generate video "<instruksi>" --format explainer|brief|cinematic|short
     --style classic|whiteboard|kawaii|anime|watercolor|documentary|... --wait --timeout 1800`
  - `notebooklm download video ./out.mp4 --latest` (juga `--all`, batch — fitur yang UI web tak punya)
  - `artifact list --type video --json` untuk polling status via cron
- **Auth headless (kunci kemandirian):** `notebooklm login --master-token --account mziyan266@gmail.com`
  (extra `[headless]`). Master token durable (bulanan/tahunan), me-re-mint cookie
  otomatis tanpa browser (layer L4). Ada juga `auth refresh` untuk cron keepalive,
  `auth import-cookies`, dan `NOTEBOOKLM_AUTH_JSON` untuk CI.
  Doc: `docs/auth-cookie-lifecycle.md`, `docs/cli-reference.md`, `docs/quota-limits.md`.
- Pros: pakai akun Google AI Pro/Ultra Bos (kuota langganan, bukan bayar per detik);
  output = Video Overview asli; ada CLI → gampang dipanggil dari cron/Orchestrator;
  bisa dijadikan skill agent.
- Cons/caveat: **unofficial** — endpoint internal bisa berubah sewaktu-waktu;
  berpotensi bertentangan dengan Google ToS (automated access); rate limit per tier;
  master token = kredensial sangat sensitif (simpan di `ziyan_credentials/`, jangan ke chat).

## JALUR 2 — `notebooklm-mcp` (roomi-fields) — REST API + MCP
- https://github.com/roomi-fields/notebooklm-mcp (v3.0, TypeScript/npm)
- 33 endpoint HTTP REST (cocok untuk cron/n8n/curl) + MCP server. Dual transport:
  `batchexecute` RPC dengan **fallback Playwright** otomatis, auto-reauth, multi-akun rotation.
- Video: format Brief/Explainer, 6 visual style, pilihan bahasa, custom instruction.
- Pros: kalau Orchestrator lebih suka HTTP/MCP daripada CLI Python; multi-account
  rotation = bagus untuk 3 short/hari tanpa kena limit satu akun.
- Cons: sama-sama unofficial; Node stack tambahan.
- Alternatif sejenis: `gnh1201/notebooklm-rest-api` (wrapper REST di atas notebooklm-py),
  `agmmnn/notebooklm-sdk` (TS) + `n8n-nodes-notebooklm-sdk`, `K-dash/nblm-rs` (Rust, Enterprise),
  `proyecto26/notebooklm-ai-plugin` (skill agent, 9 artifact termasuk Video Overview MP4),
  `PleasePrompto/notebooklm-skill` (7.5k★, Claude skill).

## JALUR 3 — Playwright/Puppeteer murni (DOM automation)
- Contoh: `israelbls/notebooklm-podcast-automator` (FastAPI + Playwright, attach ke
  Chrome `--remote-debugging-port=9222` dengan profil yang sudah login),
  `DataNath/notebooklm_source_automation`, `khengyun/notebooklm-mcp`.
- Pola penting: **jangan login lewat browser automation** (Google blokir
  "This browser or app may not be secure"). Pakai **profil Chrome persisten** /
  CDP attach ke browser yang sudah login → cookie reuse.
- Pros: tidak bergantung RPC internal, mudah dipahami.
- Cons: lambat (10–100× lebih lambat dari RPC), rapuh terhadap perubahan UI, tetap
  butuh sesi browser hidup. Ini praktis = versi terprogram dari computer_use kita sekarang.

## JALUR 4 — Google resmi ber-API: Veo via Gemini API / Vertex AI
- Docs: https://ai.google.dev/gemini-api/docs/video · https://ai.google.dev/gemini-api/docs/veo
- Model aktif (per hari riset): `veo-3.1-generate-preview`, `veo-3.1-fast-generate-preview`,
  `veo-3.1-lite-generate-preview`, plus legacy `veo-2.0-generate-001`.
  Video dengan **audio native**, text-to-video & image-to-video, ada video extension.
- Pola API: `generate_videos()` → long-running **operation**, poll `operations.get`,
  lalu download file hasil. SDK `google-genai` (Python/JS). Vertex AI = versi enterprise
  (GCP project, service account → paling cocok untuk server otomatis penuh, ToS jelas).
- Pros: **resmi, legal, stabil, tidak akan patah**; benar-benar headless dengan API key
  atau service account; cocok untuk pipeline cron.
- Cons: **BUKAN Video Overview** — Veo bikin klip sinematik pendek (per-shot, hitungan
  detik), bukan explainer bernarasi dari sumber dokumen. Untuk video 5–10 menit harus
  dirakit sendiri (script → TTS → banyak klip Veo → ffmpeg). Dan **berbayar per detik**
  (kuota langganan AI Pro/Ultra TIDAK berlaku untuk API; billing terpisah).
- Google Flow (flow.google) = UI konsumer di atas Veo, **tidak ada API publik** → sama
  posisinya dengan NotebookLM. AI Studio hanya UI/playground. YouTube tidak punya API
  video-generation (Data API hanya upload/manage).

## JALUR 5 — Open-source "NotebookLM alternative"
- `MODSetter/SurfSense` (15.6k★) — riset web live + generasi konten, alternatif open NotebookLM.
- `earlyaidopters/notebooklmreimagined` — platform API-first.
- Open NotebookLM / `jeffcwolf/open-notebooklm-ollama` — podcast audio lokal (bukan video).
- Pipeline Veo: `0xsline/StoryGen-Atelier` (storyboard Gemini + Veo Vertex),
  `nabobery/veo3-workflow-agents`, `abderrahim-boutorh/video-generation-gemini` (9:16 vertikal, Veo 3.1).
- Pros: full kontrol, bisa gabung dengan Jalur B ZIYAN yang sudah ada.
- Cons: kualitas visual ala NotebookLM harus dibangun sendiri; effort besar.

---

## REKOMENDASI (arsitektur usulan)
**Primer: Jalur 1 (`notebooklm-py`) + master-token headless.** Menggantikan
computer_use/Brave sepenuhnya untuk long-form Compound Daily.

Alur otomatis usulan (cron Orchestrator):
1. Topik dari rotasi niche (Tech/AI/Business/Finance) — sudah ada di skill ZIYAN.
2. `notebooklm create "CD <tanggal> <topik>" --use`
3. `notebooklm source add-research "<topik>" --mode deep --from web --import-all --cited-only`
4. `notebooklm generate video "<angle + audiens EN>" --format explainer --style documentary --wait --timeout 1800`
   (untuk Shorts: `--format short`)
5. `notebooklm download video "C:/Users/arija/cd_<tanggal>.mp4" --latest`
6. Upload via YouTube Data API (refresh_token compound yang sudah terbukti).
7. Log ke `ZIYAN_COMPANY_LOG` + dedupe `logs/uploaded.jsonl`.

**Sekunder/fallback:** Jalur 2 (REST/MCP, multi-akun) kalau butuh HTTP atau rotasi akun.
**Cadangan legal jangka panjang:** Jalur 4 (Veo di Vertex AI) — dipakai kalau RPC
internal patah atau kalau mau produk yang aman ToS; siapkan template pipeline
script→TTS→klip Veo→ffmpeg sekarang agar tidak panik nanti.
**Tetap pertahankan:** Jalur B (edge-tts + ffmpeg) untuk shorts volume tinggi.

## Caveat wajib disampaikan ke Bos
1. Jalur 1/2/3 = **unofficial**, melanggar semangat ToS Google (automated access).
   Risiko: rate-limit, sesi dicabut, worst case akun kena tindakan. Mitigasi:
   pakai akun khusus produksi, volume wajar, jangan paralel agresif.
2. Master token / cookie = kredensial setara password. Simpan lokal terenkripsi,
   **jangan pernah lewat chat/Discord/repo publik**.
3. Endpoint internal bisa berubah kapan saja → pin versi library, siapkan fallback
   Playwright dan alarm kegagalan di cron.
4. Video Overview generate bisa >30 menit → jadwalkan (generate cron pagi, download
   cron siang), jangan blocking-poll.
5. Format Short/Cinematic historisnya English-only & 18+; Explainer dukung banyak bahasa.
   Compound Daily target EN → aman.

## Link sumber
- https://github.com/teng-lin/notebooklm-py (docs: cli-reference.md, auth-cookie-lifecycle.md, quota-limits.md, rpc-reference.md)
- https://pypi.org/project/notebooklm-py/
- https://github.com/roomi-fields/notebooklm-mcp
- https://github.com/gnh1201/notebooklm-rest-api · https://github.com/agmmnn/notebooklm-sdk
- https://github.com/proyecto26/notebooklm-ai-plugin · https://github.com/PleasePrompto/notebooklm-skill
- https://github.com/israelbls/notebooklm-podcast-automator · https://github.com/DataNath/notebooklm_source_automation
- https://ai.google.dev/gemini-api/docs/video · https://ai.google.dev/gemini-api/docs/veo · https://ai.google.dev/gemini-api/docs/pricing
- https://github.com/MODSetter/SurfSense · https://github.com/0xsline/StoryGen-Atelier
- https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/ (rebrand NotebookLM → Gemini Notebook)
