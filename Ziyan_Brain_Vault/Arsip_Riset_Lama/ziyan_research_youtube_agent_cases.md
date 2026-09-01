# Riset: Studi Kasus Nyata Channel YouTube yang Dibangun AI Agent

Disusun untuk: ZIYAN / Compound Daily
Tanggal riset: (sesi ini) | Peneliti: agent riset ZIYAN (leaf)
Metode: pencarian web (DDG via reader-proxy), Hacker News Algolia API, artikel dev.to/Medium, repo GitHub, artikel kebijakan platform. Reddit **tidak bisa diakses** (403 network policy) — semua sumber di bawah adalah pengalaman praktis yang terpublikasi, bukan teori.

---

## 1. Ringkasan Eksekutif (untuk Bos)

1. **Ada preseden nyata channel 100% agent** — yang paling dekat dengan model ZIYAN adalah `content-foundry` → channel **@TheCrackedEng**, yang secara eksplisit menyatakan "100% generated, voiced, and published autonomously by this repository". Arsitekturnya: multi-agent pipeline dengan **Judge agent** (quality gate) + disclosure konten sintetis by default.
2. **Kasus yang paling jujur soal angka** (dev.to, 6 minggu, 52 video, 30.170 views, **29 subscriber**) membuktikan: agent bisa menjaga konsistensi produksi, tapi **volume ≠ subscriber**. Distribusi & taste tetap bottleneck.
3. **Risiko terbesar bukan teknis, tapi kebijakan.** Januari 2026: 16 channel besar (total 4,7 miliar views, ~$10 juta/tahun) dikeluarkan dari YouTube Partner Program lewat *Inauthentic Content Policy*. Screen Culture & KH Studio diterminasi. YouTube sekarang menilai **level channel**, bukan per video.
4. **Pola pemenang = "Human+AI hybrid" yang terlihat berotoritas**, bukan "human-out-of-the-loop yang tak terlihat". Untuk ZIYAN artinya: agent boleh mengerjakan 90%+, tapi channel harus punya **sidik jari editorial** (sudut pandang, data eksklusif, opini, variasi format) dan **jadwal upload manusiawi** (rencana upload random Bos = benar secara strategi).
5. **NotebookLM sudah dipakai orang** sebagai mesin produksi video (Video Overviews) dan sudah ada tooling otomasi (2 repo GitHub + ekstensi Chrome). **OpenMontage tidak muncul sama sekali** di literatur studi kasus — kita jadi early adopter (risiko: tidak ada playbook orang lain; keuntungan: diferensiasi visual dari "AI slop" standar).
6. **Biaya bukan penghalang**: pipeline full-AI 10 menit + 5 shorts terbukti **< $5/episode**; dengan stack gratis (Edge TTS/Piper, Pexels, LLM lokal) bisa mendekati $0.

---

## 2. Tabel Studi Kasus

| # | Channel / Proyek | Siapa | Tech Stack | Hasil Nyata | Level Otonomi | NotebookLM / tools serupa |
|---|---|---|---|---|---|---|
| 1 | **@TheCrackedEng** (repo `pranshu97/content-foundry`) | Engineer indie, open-source | Multi-agent Python: Data Fetcher → Script Generator (LLM) → **Judge** (rubrik kualitas) → Voiceover → Visuals → Render → Publish. TTS: Edge (gratis) / Piper offline / Chatterbox voice-clone / ElevenLabs-OpenAI (berbayar). Visual: Pexels+Pixabay B-roll atau title card. Riset: DuckDuckGo gratis + YouTube API "outlier mining". SQLite state, resume per-stage, Streamlit review dashboard, notifikasi Telegram, hard budget cap | Repo publik dengan channel live; angka subs/revenue **tidak dipublikasi** (kami tidak berhasil verifikasi) | **Penuh** (upload otomatis sebagai draft Private/Unlisted secara default) | Tidak. Custom pipeline sendiri |
| 2 | **Channel sejarah medis (Shorts)** — dev.to "I Let AI Agents Run My YouTube Channel for 6 Weeks" (wcamon, Feb 2026) | Dokter + engineer | 2 agent berbasis **Claude dengan persistent memory**: "Midnight" (produksi, analytics, strategi) & "Dusk" (X/Twitter, blog, distribusi). Custom media engine + TTS, terjemahan 14–15 bahasa/video, YouTube Data API untuk upload+metadata | **6 minggu: 52 video, 30.170 views, 29 subs**, like rate 4–5% (normal 1–2%); 1 video 474 menit watch time, loop rate 109% | **Human-in-the-loop**: agent pitch, manusia approve ide & review kualitas | Tidak. Justru **anti-n8n/Make** ("tools tidak punya memori, konteks, judgment") |
| 3 | **The Machine Pulse + 3 channel lain (1 codebase)** — dev.to (Mar 2026) | Frontend engineer 12 tahun React | 10-step CLI pipeline satu perintah: script JSON + SHA-256 hash → **Google Cloud TTS Chirp 3 HD** (voice beda per channel) → **Whisper** untuk timing/word alignment → **Vertex AI Imagen 3** (65 gambar/episode) → **FFmpeg** (mixing, musik, subtitle, color grading) → verifikasi artefak. **Humanize score 100 poin** (deteksi AI fingerprint, "you"-count, ritme kalimat, spesifisitas, hook); < 90 → **Gemini 2.5 Flash** menulis ulang otomatis. Fact-grounding via Gemini + Google Search live. Auto-generate 5 Shorts/episode, tiap Shorts di-skor 10 poin | **Biaya < $5/episode** (gambar $4,20; TTS $0,21; Gemini $0,10; FFmpeg/Whisper gratis). 4 channel, 1 codebase, beda YAML config. Angka subs tidak dipublikasi | ~80% otomatis, topik & taste tetap manusia | Tidak |
| 4 | **Channel "Top 10" n8n** — Medium (owaiss, Apr 2026) | Solo builder | **n8n** end-to-end: AI generate 10 ide evergreen → Google Sheets sebagai content queue → LLM structured JSON output (intro/outro/ranking/image prompt) → video API (voiceover+gambar+transisi) → async polling → auto-upload | Sistem jalan tanpa editing/rekaman manual; angka performa tidak dipublikasi | Penuh (no-code) | Tidak |
| 5 | **Channel NotebookLM** — Medium (Nitin Gavhane, Jun 2026) | Solo creator | **Google NotebookLM Video Overviews** (talking-head dari sumber PDF/URL/YouTube) langsung diupload ke YouTube; monetisasi via niche + affiliate | Walkthrough praktis "apa yang berhasil & tidak"; angka spesifik tidak dibuka | Semi-otomatis (masih klik UI) | **Ya — NotebookLM inti**. Ekosistem otomasi: `void-mckenzie/NotebookLM_Youtube_Automator`, `rumilog/notebooklm-automate`, ekstensi Chrome "Video Automator for NotebookLM" |
| 6 | **4 channel tutorial tech faceless** — Medium (The Growtharo, "What I Learned After Failing My First Automated Channel") | Operator 4 channel | Slideshow + TTS robotik generasi awal | Channel pertama **gagal**; sekarang 4 channel faceless semua menghasilkan uang. Pesan inti: "YouTube automation bukan scam, tapi cara jualannya ke pemula itu scam" — banyak orang rugi beli blueprint, channel dihapus semalam | Faceless, bukan agentic | Tidak |
| 7 | **HN Show/Ask (beberapa praktisi)** | Anon | MoviePy + bot uploader (43101593); gaming highlights | 20 video → **47 subs**, CPM $2–4; 8 bulan → 50k subs tapi hanya **~$200/bulan** karena niche CPM rendah | Penuh/semi | Tidak |
| 8 | **Screen Culture & KH Studio (kasus negatif)** | Channel besar | AI trailer film palsu, produksi massal | **Diterminasi YouTube**. Jan 2026: total 16 channel besar (4,7 M views, ~$10jt/thn) keluar dari YPP | Penuh, tanpa authorship | — |

---

## 3. Tech Stack yang Terbukti Dipakai (rangkuman komponen)

| Lapisan | Pilihan yang terbukti di lapangan | Catatan untuk ZIYAN |
|---|---|---|
| Orkestrasi agent | Claude + persistent memory (kasus 2); multi-agent Python custom + SQLite state + resume per-stage (kasus 1); n8n (kasus 4) | Hermes agent kita setara kasus 1–2. **Persistent memory = pembeda utama** vs workflow n8n |
| Riset topik | DuckDuckGo gratis; YouTube Data API "outlier mining" (cari video jauh di atas median channel); Gemini + Google Search grounding | Wajib untuk Compound Daily (Tech/AI/Bisnis/Keuangan yang time-sensitive) |
| Scripting & QC | LLM + **Judge/rubrik terukur**: humanize score 100 poin, ambang skor, auto-rewrite bila gagal | Ini yang membedakan output layak tayang vs "AI slop" |
| TTS | Google Cloud TTS Chirp 3 HD (berbayar, kualitas tinggi); Edge TTS gratis; Piper offline; Chatterbox voice-clone lokal (MIT, aman dimonetisasi); ElevenLabs | Suara berbeda & konsisten per channel = identitas |
| Visual | Vertex AI Imagen 3 (~$0,04/gambar), stock B-roll Pexels/Pixabay, title card Pillow; **hindari slideshow statis** | Bos sudah benar menolak gradient robotik — itu persis pola yang di-flag YouTube |
| Assembly | FFmpeg + Whisper (word-level timing) — gratis, lokal | OpenMontage kita menempati slot ini |
| Upload | YouTube Data API v3 OAuth; default publish sebagai Private/Unlisted lalu direview (kasus 1) | Cocok untuk gate manusia/agent-reviewer sebelum publik |
| Compliance | Disclosure konten sintetis **by default** (kasus 1) | Wajib centang "altered/synthetic content" di YouTube |
| Ops | Hash artefak (SHA-256), resume, budget cap bulanan, dashboard review, notifikasi Telegram | Kita perlu ini agar produksi harian tak diam-diam rusak |

---

## 4. Pitfalls Nyata (dari orang yang sudah kena)

**A. Teknis / pipeline**
1. **Silent failure paling mematikan** — gambar gagal di-generate tapi pipeline lanjut → 3 episode terbit dengan frame hitam sebelum ketahuan. Solusi: *fail loud*, error fatal, verifikasi artefak sebelum render.
2. **Stale cache saat resume** — script diedit tapi audio lama dipakai. Solusi: hash konten, bandingkan saat resume.
3. **Async handling adalah bagian tersulit** (kasus n8n) — video generation lama; butuh state tracking + polling + recovery.
4. **Durasi video sulit dikontrol** — target 60 detik jadi 41 detik. Trik yang bekerja: tulis angka sebagai kata, minta eksplisit "SLOW PACING", tentukan 8–10 detik per scene.
5. **Analytics API telat 72+ jam** — optimasi real-time mustahil; agent harus memutuskan dengan data tidak lengkap.

**B. Konten / audiens**
6. **Agent tidak bisa menilai kualitas cerita** — bisa fact-check dan produksi, tidak bisa tahu apakah sesuatu bikin orang *merasa*. 20% terakhir (taste, timing, editorial) tetap manusia.
7. **Volume tidak otomatis jadi subscriber** — 52 video/30k views → 29 subs. Views datang dari algoritma, subs datang dari identitas.
8. **CTA di Shorts nyaris nol respons** — 0 balasan dari semua format CTA yang dicoba. Itu perilaku platform, bukan kesalahan agent.
9. **Visual AI punya plafon** — lama-lama terasa seragam.
10. **Salah niche = kerja 8 bulan untuk $200/bulan** (CPM $2–4). **Cek CPM niche sebelum produksi.** Tech/AI/Bisnis/Keuangan pilihan Bos justru salah satu CPM tertinggi — ini keunggulan awal kita.

**C. Kebijakan (risiko eksistensial)**
11. YouTube menilai **seluruh channel**, bukan per video, di bawah *Inauthentic Content Policy*.
12. Pemicu flag: **overposting** (jadwal yang manusia tak mungkin sanggup), template clone (video identik kecuali judul), slideshow gambar tanpa editing, konten tanpa komentar/nilai tambah.
13. Update kebijakan Juli 2025: **konten AI produksi massal tidak bisa dimonetisasi**; hybrid human+AI aman.
14. 3 strike → channel hilang. Channel bisa lenyap semalam — punya backup aset & rencana multi-platform.

---

## 5. Apakah Ada yang Pakai NotebookLM / OpenMontage?

- **NotebookLM: ya, sudah jadi jalur produksi nyata.** Video Overviews dipakai untuk membuat video siap upload; ada minimal 3 alat otomasi publik (`void-mckenzie/NotebookLM_Youtube_Automator`, `rumilog/notebooklm-automate`, ekstensi Chrome "Video Automator for NotebookLM") plus banyak tutorial "clone channel apa pun dengan NotebookLM". **Peringatan:** justru karena mudah dan hasilnya seragam (format talking-head/podcast dua suara yang khas), ini kandidat kuat kena label "templated/mass-produced" jika dipakai mentah dan bervolume tinggi. Aman kalau: sumbernya eksklusif (riset/data kita sendiri), visualnya di-remix (OpenMontage), dan ada sudut pandang.
- **OpenMontage: tidak ditemukan satu pun studi kasus channel yang memakainya.** Tidak ada playbook publik → kita harus menulis playbook sendiri, tapi juga berarti output kita tidak akan terlihat seperti sejuta channel n8n/NotebookLM lain. Ini keuntungan diferensiasi terhadap deteksi "AI slop".

---

## 6. Rekomendasi Konkret untuk Compound Daily

1. **Adopsi pola "Judge agent"** (kasus 1 & 3): rubrik skor terukur (deteksi kata-kata khas AI, jumlah sapaan "you", panjang kalimat rata-rata < 12 kata, angka spesifik bukan "jutaan", kualitas hook) + auto-rewrite bila skor < ambang. Tanpa gate ini, otonomi penuh = slop.
2. **Persistent memory wajib.** Agent harus ingat performa tiap video, jam upload, format, dan menyesuaikan — inilah yang membuat kita bukan sekadar workflow.
3. **Jadwal upload random Bos: benar.** Overposting berpola = pemicu flag nomor satu. Rekomendasi: 3–5 video/minggu dengan jitter jam, bukan 2–3/hari.
4. **Wajib disclosure konten sintetis** dan wajib "authorship signal": sudut pandang ZIYAN yang konsisten, data/analisis yang tidak bisa disintesis mesin (mis. hasil eksperimen agent kita sendiri — itu konten eksklusif yang tidak dimiliki channel lain).
5. **Hindari slideshow statis & gradient robotik** (sudah dilakukan Bos). Gunakan B-roll bergerak, screen recording, variasi grading per rubrik.
6. **Pipeline harus fail-loud + resumable + budget-capped** sejak hari pertama.
7. **Publish default sebagai Private/Unlisted**, lalu agent reviewer (atau Bos) mem-flip ke public. Ini juga memenuhi ekspektasi "human oversight" YouTube.
8. **Ukur yang benar sejak awal**: like rate, watch time, retention — bukan jumlah video. Target realistis 6 minggu pertama berdasarkan preseden: puluhan ribu views, subs masih dua digit. Jangan janjikan monetisasi cepat ke Bos.
9. **Manfaatkan CPM tinggi niche kita** (Tech/AI/Bisnis/Keuangan) — ini satu-satunya kesalahan terbesar (salah niche) yang secara struktural sudah kita hindari.

---

## 7. Daftar Sumber

1. dev.to — "I Let AI Agents Run My YouTube Channel for 6 Weeks. Here's What Actually Happened." (wcamon, 16 Feb 2026)
2. dev.to — "I Built This Entire YouTube Channel With AI — The Full Stack" (The Machine Pulse, 11 Mar 2026)
3. GitHub — `pranshu97/content-foundry` + channel `youtube.com/@TheCrackedEng`
4. Medium — "I Built a Fully Automated 'Top 10' YouTube Channel With n8n" (Mohammad Owais, Apr 2026)
5. Medium — "How I Built a YouTube Channel Using NotebookLM Video Overviews (And How to Monetize It)" (Nitin Gavhane, Jun 2026)
6. Medium/MoneyHive — "What I Learned After Failing My First Automated YouTube Channel" (The Growtharo, Jul 2025)
7. ScaleLab — "Why YouTube is Cracking Down on AI-Generated Content in 2026" (3 Apr 2026)
8. Hollywood Reporter via HN — "YouTube Cracks Down on AI Slop"
9. Hacker News threads: 45894359 (8 bulan, 50k subs, $200/bln), 45949988 (20 video → 47 subs), 43101593 (MoviePy + bot uploader)
10. GitHub/Chrome Web Store — `void-mckenzie/NotebookLM_Youtube_Automator`, `rumilog/notebooklm-automate`, "Video Automator for NotebookLM"

**Catatan keterbatasan:** Reddit diblokir (403) selama riset ini, jadi tidak ada data thread r/juststart & r/thesidehustle. Angka subscriber @TheCrackedEng tidak berhasil diverifikasi langsung. Beberapa artikel Medium terpotong paywall — poin yang dikutip di atas hanya dari bagian yang benar-benar terbaca.
