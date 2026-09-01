---
name: ziyan-blog-seo
description: "SOP blog ZIYAN: competitor research, NotebookLM, autopost."
version: 1.1.0
author: ZIYAN Orchestrator
license: MIT
tags: [ziyan, blog, seo, notebooklm, content, monetization]
---
# ZIYAN — SOP Blog & SEO

Berlaku SETIAP kali Bos minta generasi artikel blog. Load skill ini + `ziyan-agent-architecture` (NotebookLM CLI) + `ziyan-youtube` (Blogger autopost).

## Communication & Report Style (preferensi Bos — terbukti)
- **Bahasa Indonesia**, langsung ke inti, **singkat padat jelas**.
- Laporan WAJIB **terstruktur** (tabel > paragraf panjang).
- **Otonom**: eksekusi task rutin/already-approved TANPA minta izin berulang.
  HENTIKAN & tanya HANYA jika: instruksi ambigu, atau task BARU yang membebani
  sistem secara signifikan dan belum pernah disetujui Bos.
- JANGAN pakai filler chatbot ("Tentu saja", "Ide bagus", "Saya mengerti").

## Communication & Report Style (preferensi Bos — terbukti)
- **Bahasa Indonesia**, langsung ke inti, **singkat padat jelas**.
- Laporan WAJIB **terstruktur** (tabel > paragraf panjang).
- **Otonom**: eksekusi task rutin/already-approved TANPA minta izin berulang.
  HENTIKAN & tanya HANYA jika: instruksi ambigu, atau task BARU yang membebani
  sistem secara signifikan dan belum pernah disetujui Bos.
- JANGAN pakai filler chatbot ("Tentu saja", "Ide bagus", "Saya mengerti").

## Alur Wajib (tiap artikel)
1. **Riset Topik Trending — AGENT yang cari (BUKAN Bos kasih keyword)**
   - Dispatch sub-agent RISA: cari topik trending TERBARU di X/Twitter (niche AI/Tech/Finance/Business/Quantum/n8n/AI Agent). Bukti wajib: URL tweet/thread + engagement. JANGAN halusinasi topik.
   - Pilih 1 topik paling hot & relevan ZIYAN.
   - LALU riset 10 sumber terpercaya (kompetitor top organic via Bing/DuckDuckGo, BUKAN google.com yang keblokir reCAPTCHA).
   - Masukkan 10 URL ke NotebookLM: `notebooklm source add -n <NB> --type url <url>` (bukan acak).
   - Koreksi 8/3: jangan usul topik sendiri lalu langsung tawar bikin notebook — agent WAJIB riset trending dulu, lalu jalankan pipeline sampai SELESAI tanpa berhenti tanya Bos (kecuali task sistem-berat baru yang belum disetujui).

2. **SEO Outline (NotebookLM)**
   - Perintah generate report: Judul SEO, Meta Description, H1/H2/H3, LSI Keywords, saran internal/external link.

3. **Draft Markdown**
   - Generate report -> simpan `.md`. Struktur rapi saat upload blog.

4. **Two-Brain Polish**
   - Jika draf kaku -> masukkan ke sub-agent 9router (`openrouter/google/gemma-4-26b-a4b-it:free` / `poolside/laguna-s-2.1` / `channel-researcher`) untuk natural tone.
   - BUKAN Claude/ChatGPT berbayar (ZIYAN pakai free 9router).

5. **Aset Multimedia Wajib (embed di blog)**
   - Cover: Infografis PNG (NotebookLM `generate infographic`) + Alt Text SEO.
   - Mind Map JSON: convert ke teks tree / embed di tengah artikel (kalau bahas sistem).
   - Audio Overview: embed player. SoundCloud BELUM ada akun ZIYAN -> sementara embed YouTube (video IonQ) atau Telegram voice note. BUTUH Bos sediakan akun SoundCloud kalau wajib.

6. **Upload Blogger (terbukti jalan 8/3)**
   - Lihat `references/blogger_api_upload.md` untuk script lengkap & token yang benar.
   - Blog ID ZYN AI corp = `598320500315317650` (ziyancorp.blogspot.com).
   - Token: `youtube_token_ziyanmalik.json` + client `youtube_desktop_client.json` (sudah punya scope blogger).
   - PITFALL: jangan embed gambar base64 besar (6MB+) -> Blogger balas 400. Pakai URL eksternal (YouTube thumbnail) sebagai cover.

## Platform Blog ZIYAN
- Blogger: "ZYN AI co" (ziyancorp.blogspot.com) -> autopost via API (lihat `ziyan-youtube-blogger-oauth` + `references/blogger_api_upload.md`).
- LinkedIn: carousel dari slide deck.
- Jadwal: <=1 artikel/hari (anti AdSense scaled-content / NOV).

## Penjadwalan Karyawan & Kapasitas Harian (Free tier NotebookLM)
- **RISA** (Riset): trending X + 10 sumber — 5-10 riset/hari
- **NOVA** (NotebookLM): inject 10 sumber + 8 artefak — **3 notebook/hari** (max 3 video Free)
- **FAZA** (Video): download Long (16:9), upload YouTube private — 3 video/hari. Shorts = Bos generate native di HP (JANGAN crop).
- **PANDA** (Distribusi): TG/X/LinkedIn/Blog/monetisasi — 5-10 post/hari
- **Kapasitas max/hari**: 3 Long-form + 3 Shorts + 3 Audio (limit Free). Blog post unlimited (cuma butuh draft MD).
- Nama notebook: `ZIYAN_<topik>_<tanggal>`.

## Pengiriman File ke Bos (Discord gabisa file besar)
- Shorts/Long untuk Bos download: upload ke **OneDrive** (arijalmeutuwah@hotmail.com) → kasih link, atau kirim via **Telegram bot**.
- JANGAN kirim file >25MB lewat Discord chat.

## Etik (sesuai prinsip Bos)
- Pakai data orisinal ZIYAN (riset kita), BUKAN rekap web umum.
- Wajib AI disclosure.
- JANGAN janjikan "cuan dari NotebookLM" ke klien sebelum ada buai sendiri (riset 8/3: TIDAK ADA bukti kuat orang cuan murni dari artefak NotebookLM — yang beredar cuma tutorial).

## NotebookLM CLI (terbukti — lihat `references/notebooklm_cli_verified.md`)
- `notebooklm list` — list notebook
- `notebooklm source add -n <NB> --type url <url>` — inject sumber
- `notebooklm generate report -n <NB> "<prompt>"` — draft (NO --title flag)
- `notebooklm generate video -n <NB> "<prompt>" --format explainer|brief|cinematic` — NO short
- `notebooklm generate <type> -n <NB> "<prompt>"` — infographic/mind-map/data-table/quiz/slide-deck/audio
- `notebooklm artifact wait <id> -n <NB> --timeout 120` — poll
- `notebooklm download <type> -n <NB> <output_path>` — download

## Pitfalls (verified 8/3)
- Google Search keblokir reCAPTCHA -> sub-agent gagal riset validasi. Pakai Bing/DuckDuckGo/fetch langsung.
- `notebooklm generate report` TIDAK punya flag `--title` -> prompt positional saja.
- `notebooklm download` butuh subcommand type lalu positional path (bukan `--output-dir`).
- `notebooklm generate video --format short` DITOLAK di CLI -> Short 9:16 HANYA di mobile app NotebookLM (Bos generate di HP). **ATURAN BOSS 2026-08-04: JANGAN crop explainer via ffmpeg — agent HANYA download Long (16:9), Boss yang bikin Short native.** Ffmpeg crop DEPRECATED untuk ZIYAN.
- NotebookLM FREE = MAX 3 video + 3 audio/hari.
- JANGAN computer_use / Playwright / Chromium klik UI NotebookLM & Google Flow (Google blokir "browser not secure") -> semua via CLI + storage_state.json cookie Netscape. Antigravity project Bos (`operate_user_chrome.py` Playwright) = OBSOLETE, jangan disentuh/modifikasi.
- Blogger 400 jika content terlalu besar (base64 image 6MB+) -> pakai URL eksternal.

## Support files
- `references/blogger_api_upload.md` — script Python upload Blogger yang terbukti jalan + token yang benar.
- `references/notebooklm_cli_verified.md` — command NotebookLM CLI lengkap yang sudah diverifikasi.
- `references/seo_blog_sop_full.md` — draft SOP lengkap (mirror file di disk `C:\Users\arija\ziyan_seo_blog_sop.md`).
