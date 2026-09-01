# AUDIT FOLDER `nb_proof` UNTUK ZIYAN
*Divisi Audit ZIYAN — 2026-08-01. Folder sumber: `C:\Users\arija\nb_proof` (107 MB, proyek lama "Compound Daily", faceless YouTube finance).*

Folder ini adalah eksperimen lama monetisasi (channel finance faceless + bot job-hunting). **Bukan ZIYAN**, tapi berisi beberapa pipeline otomasi biaya-nol yang langsung reusable untuk distribusi konten ZIYAN. Fokus nilai: pipeline NotebookLM→YouTube, generator visual gratis (Pollinations), analytics loop, dan riset algoritma YouTube.

---

## 1. KATEGORISASI FILE

| Kategori | File |
|---|---|
| **Pipeline video (NotebookLM)** | `nb_pipeline.py`, `pipeline_full.py`, `generate_longform.py`, `stok_seminggu.py`, `make_notebook6-9.py`, `operator_notebooklm.ipynb`, `nb_run_today.sh`, `nb_storage.json` |
| **YouTube automation** | `youtube_uploader.py`, `yt_analytics.py`, `audit_and_learn.py`, `apply_channel_metadata.py` |
| **Visual generator** | `generate_visuals.py` (Pollinations, gratis) |
| **Google/Gmail/Drive access** | `google_access.py` |
| **Job hunter (TIDAK relevan ZIYAN)** | `job_hunter_playwright.js` v1–v5, `check_login.js`, `job_hunter_profile.json`, `JOB_HUNTER_GUIDE.md` |
| **Riset .md (insight)** | `RIS.iyet_ALGORITMA_YT.md`, `STRATEGI_CUAN.md`, `COMPETITOR_ANALYSIS.md`, `BROWSER_ACT_MONETIZATION.md`, `MASTER_ACTION_PLAN.md`, `VIDEO2_TOOLS_ANALYSIS.md`, `laporan_notebooklm_tools.md`, `METADATA_COMPOUND_DAILY.md`, `RIS.iyet_AFFILIATE_*.md`, dll |
| **Debug/sampah** | `dbg_*.py`, `dbg/`, `dbg_profile/`, `_frames/`, `tmp/`, `cd_page.html`, `*_debug_*.html/png`, `login_check_*`, `upwork_*`, `cookie_proof.png`, `pipeline_run_*.log`, `__pycache__/` |
| **Installer/media besar** | `Claude Setup.exe`, `Hermes-Setup.exe`, `Inside_the_Zero-Employee_AI_Company.mp4` (9.9MB), `WhatsApp Video*.mp4` (15MB) |
| **🔴 RAHASIA** | `client_secret.json`, `client_secret_789747689443-*.json`, `all_google_cookies.json`, `gemini_key.txt`, `token_analytics.json`, `token_google_access.json`, `yt_token.pickle`, `cookie_proof.png` |

---

## 2. TABEL ASET REUSABLE

| Aset Reusable | File | Fungsi | Status | Manfaat ZIYAN |
|---|---|---|---|---|
| NotebookLM→YT full pipeline | `pipeline_full.py` | Generate video via NotebookLM CLI → caption (Gemini/9Router) → upload YouTube → hapus MP4. Multi-video/hari. | Kode utuh & modular. Butuh: notebooklm CLI + master-token, `client_secret.json`+OAuth token (kadaluarsa, harus re-consent), GEMINI_API_KEY (opsional, ada fallback 9Router lokal). | Backbone distribusi video ZIYAN otomatis end-to-end, biaya nol. Ganti NOTEBOOK_ID + topik → jalan. |
| Pipeline Short 9:16 | `nb_pipeline.py` | Set notebook → generate Short vertikal → download MP4, dengan guard 1-konten/hari. | Ringan, dependency sama (notebooklm CLI). NOTEBOOK_ID hardcoded lama → ganti. | Template inti untuk auto-generate video ZIYAN; guard harian mencegah spam. |
| Long-form stitcher | `generate_longform.py` | Generate beberapa segmen NotebookLM lalu ffmpeg concat + intro/outro card 16:9. | Butuh ffmpeg (umum) + notebooklm CLI. Logika stitch murni lokal & reusable tanpa akun. | Bikin video panjang ZIYAN (kompilasi/deep-dive) dari beberapa klip; `--stitch-only` bisa dipakai standalone. |
| Visual generator gratis | `generate_visuals.py` | Generate thumbnail 1280×720 + carousel 1080×1080 via Pollinations (flux) pakai curl. | **Jalan tanpa API key / tanpa auth.** Hanya butuh curl + internet. Paling siap-pakai. | Thumbnail & aset sosmed ZIYAN instan, 100% gratis. Tinggal ganti prompt/brand. |
| Analytics learn-loop | `audit_and_learn.py` (+`yt_analytics.py`) | Tarik metrik YouTube Analytics 28 hari, simpan history JSON/CSV, auto-tulis rekomendasi ke SKILL.md. | Butuh OAuth token valid + channel YPP. Token lama kadaluarsa. Pola self-updating skill = sangat reusable. | Loop feedback data→rekomendasi untuk channel ZIYAN; pola "auto-update skill" bisa dipakai lintas divisi. |
| Uploader YouTube | `youtube_uploader.py` | Upload MP4 resumable via YouTube Data API v3, OAuth. | Kode solid. Butuh `client_secret.json` + re-consent (token lama mati). | Modul upload siap-pakai untuk kanal ZIYAN. |
| Batch scheduler | `stok_seminggu.py` | Loop `pipeline_full.py` untuk stok 7 hari × 3 video, publishAt spread. | Bergantung pipeline_full + venv path hardcoded (perlu sesuaikan). | Isi antrean konten ZIYAN seminggu sekali jalan. |
| Google multi-API access | `google_access.py` | Consent Gmail/Drive/Calendar read via OAuth. | Butuh enable API + re-consent. | Kalau ZIYAN perlu baca Gmail/Drive untuk otomasi. |
| Riset algoritma YT | `RIS.iyet_ALGORITMA_YT.md` | Fakta resmi cara algoritma YouTube (watch time, AVD, viewed-vs-swiped). | Evergreen, dari sumber resmi. | Panduan optimasi retensi video ZIYAN — tetap valid. |
| Riset tooling NotebookLM | `laporan_notebooklm_tools.md` | Rekomendasi `teng-lin/notebooklm-py` (gratis, MIT, master-token self-healing). | Insight valid; dependency inti semua pipeline di atas. | Justifikasi & cara pasang engine video gratis ZIYAN. |

**Insight .md lain (parsial valid):** `STRATEGI_CUAN.md` (syarat YPP, RPM finance), `METADATA_COMPOUND_DAILY.md` (template deskripsi/tag channel) — masih berguna sbagai referensi, tapi niche "finance" spesifik Compound Daily, perlu di-reframe ke brand ZIYAN.

---

## 3. FILE RAHASIA — 🔴 JANGAN DIPAKAI / SHARE

Isi TIDAK dibaca/di-print. Ini kredensial akun eksternal milik Bos:

| File | Jenis |
|---|---|
| `client_secret.json` | OAuth client credential Google |
| `client_secret_789747689443-…apps.googleusercontent.com.json` | OAuth client credential Google (duplikat) |
| `all_google_cookies.json` | Cookie sesi Google penuh |
| `gemini_key.txt` | API key Gemini |
| `token_analytics.json` | OAuth access/refresh token YouTube Analytics |
| `token_google_access.json` | OAuth token Gmail/Drive/Calendar |
| `yt_token.pickle` | Token upload YouTube (pickle) |
| `cookie_proof.png` | Screenshot berisi cookie/sesi |

**Rekomendasi:** jangan commit, jangan kirim, jangan reuse token lama (kemungkinan besar kadaluarsa). Kalau ZIYAN butuh akun, buat kredensial baru bersih.

---

## 4. KESIMPULAN

### 5 ASET PALING BERHARGA UNTUK ZIYAN
1. **`generate_visuals.py`** — visual/thumbnail gratis tanpa key, siap pakai HARI INI.
2. **`pipeline_full.py`** — pipeline video otomatis end-to-end (generate→caption→upload), biaya nol.
3. **`nb_pipeline.py`** — template inti generate video (Short 9:16) + guard harian.
4. **`generate_longform.py`** — stitcher ffmpeg untuk video panjang (logika lokal, tanpa akun).
5. **`audit_and_learn.py`** — pola analytics→rekomendasi→auto-update skill (reusable lintas divisi).

### 3 YANG HARUS DIHAPUS (sampah/debug/tak relevan)
1. **Semua `dbg_*.py`, `dbg/`, `dbg_profile/`, `_frames/`, `tmp/`, `__pycache__/`, `*_debug_*.html/png`, `login_check_*`, `upwork_*`, `cd_page.html`, `cookie_proof.png`** — artefak debug/scrape sekali pakai.
2. **`job_hunter_playwright*.js` (v1–v5) + `JOB_HUNTER_GUIDE.md` + `check_login.js`** — bisnis job-hunting, TIDAK relevan untuk ZIYAN.
3. **`Claude Setup.exe`, `Hermes-Setup.exe`, `WhatsApp Video*.mp4` (15MB)** — installer & media besar makan ruang, bukan aset.

*Catatan: `client_secret*/token*/cookies/gemini_key.txt` juga sebaiknya dihapus/di-rotate demi keamanan, tapi masuk kategori RAHASIA, bukan sampah.*
