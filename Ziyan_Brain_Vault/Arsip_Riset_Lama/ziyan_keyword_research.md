# RISET KEYWORD ZIYAN — Niche Tech / AI / Bisnis / Keuangan
Tanggal riset: 2 Agustus 2026
Sumber data: Google Trends (pytrends, unofficial API) — timeframe `today 3-m`, geo Global (EN)
Metode: 16 seed keyword → tarik `related_queries` (top + rising) → ranking berdasarkan skor **rising**

---

## 1. Ringkasan Eksekusi

- Tool: `pytrends` diinstall di venv `~/.kwenv` (pip global bentrok Python 3.14 + urllib3 v2; solusi: venv `uv` dan **jangan pakai** parameter `retries=` karena error `method_whitelist`).
- 12 dari 16 seed berhasil ditarik. 4 seed kena rate-limit HTTP 429 (`freelance AI`, `AI agents`, `dividend investing`, `how to invest`) — sudah dicover secara tidak langsung lewat seed lain.
- Query rising yang jelas noise (nama orang, hymns, hotel, gardening, se7en, dll) sudah dibuang dari ranking.

---

## 2. Tabel Ranked — Keyword RISING (naik daun)

| # | Keyword Rising | Skor Rising | Seed Asal | Relevansi Niche |
|---|---|---|---|---|
| 1 | **ai tools you should know in 2026** | 6.350 | make money online | ⭐⭐⭐⭐⭐ AI + uang |
| 2 | **most useful chrome extensions** | 5.950 | passive income | ⭐⭐⭐⭐ Tech praktis |
| 3 | commonwealth bank passive income | 6.700 | passive income | ⭐⭐⭐ Keuangan (regional AU) |
| 4 | jnj passive income investment | 5.450 | passive income | ⭐⭐⭐ Saham dividen |
| 5 | **coca-cola dividend passive income** | 900 | passive income | ⭐⭐⭐⭐ Dividen brand terkenal |
| 6 | **best free apps for productivity** | 450 | make money online | ⭐⭐⭐⭐⭐ Tech mass-appeal |
| 7 | **best side hustles for students** | 400 | make money online | ⭐⭐⭐⭐⭐ Bisnis/uang |
| 8 | passive income hsbc shares | 400 | passive income | ⭐⭐⭐ Keuangan |
| 9 | telstra share passive income | 350 | passive income | ⭐⭐ Regional |
| 10 | **how to start a youtube channel** | 250 | make money online | ⭐⭐⭐⭐ Bisnis kreator |
| 11 | **stock market basics** | 250 | passive income | ⭐⭐⭐⭐⭐ Keuangan pemula |
| 12 | morning routine for success | 250 | make money online | ⭐⭐⭐ Self-improvement |
| 13 | **personal finance tips** | 110 | passive income | ⭐⭐⭐⭐⭐ Keuangan |
| 14 | **how to save money fast** | 70 | make money online | ⭐⭐⭐⭐⭐ Keuangan |
| 15 | ways to create passive income | 60 | passive income | ⭐⭐⭐⭐ Keuangan |
| 16 | **chatgpt image / images** | 60 / 50 | ChatGPT | ⭐⭐⭐⭐ AI visual |
| 17 | chatgpt prompt | 40 | ChatGPT | ⭐⭐⭐⭐ AI praktis |
| 18 | **ai automation specialist** | 40 | AI automation | ⭐⭐⭐⭐ Karier AI |
| 19 | chatgpt codex | 70 | ChatGPT | ⭐⭐ terlalu teknis |
| 20 | internal tools deepen ai | 50 | AI tools | ⭐ noise korporat |

## 3. Keyword TOP (volume stabil tinggi — bagus untuk SEO judul)

| Kategori | Keyword volume tinggi |
|---|---|
| AI Tools | best ai tools, free ai tools, top ai tools, ai marketing tools, ai study tools, google ai tools |
| ChatGPT | chatgpt free, chatgpt app, chatgpt login, chatgpt plus, chatgpt prompt |
| Uang Online | how to make money online, make money online free, ways to make money online |
| Passive Income | best passive income, passive income ideas, passive income online, what is passive income, passive income investment |
| AI Automation | what is ai automation, ai automation jobs, ai workflow automation, ai automation tools, ai automation agency, ai automation course |
| Side Hustle | best side hustle 2026, **ai side hustle**, side hustle ideas, online side hustle, side hustle jobs |
| Karier AI | ai automation jobs, ai engineer jobs, remote jobs |
| UMKM | ai for small business, how to start a small business |

**Insight kunci:** sinyal terkuat bukan "model AI apa yang baru", tapi **"AI dipakai untuk menghasilkan/menghemat uang"**. Kombinasi `AI × side hustle × passive income × pemula` = zona emas ZIYAN. Ini sekaligus mengonfirmasi penolakan Bos terhadap topik teknis seperti "71 free AI models".

---

## 4. 8 IDE TOPIK VIDEO (siap produksi)

### IDE 1 — "AI Tools You Should Know in 2026 (That Actually Make You Money)"
- **(a) Judul:** `5 AI Tools You Should Know in 2026 — #3 Pays Your Rent`
- **(b) Alasan demand:** query rising #1 absolut, skor 6.350, muncul dari seed "make money online" → penonton mencari AI *untuk uang*, bukan AI untuk ngoprek.
- **(c) Keyword:** ai tools you should know in 2026, best ai tools, free ai tools, ai side hustle
- **(d) Format:** **Short 60s EN** (5 tools, 10 detik masing-masing) + versi Long 8–10 menit "with real demos"

### IDE 2 — "AI Side Hustles for Students"
- **(a) Judul:** `4 AI Side Hustles for Students (Start With $0 in 2026)`
- **(b) Alasan demand:** "best side hustles for students" rising 400 + "ai side hustle" masuk TOP query. Audiens muda = retensi Shorts tertinggi.
- **(c) Keyword:** best side hustles for students, ai side hustle, side hustle ideas, best side hustle 2026, make money online free
- **(d) Format:** **Short 60s EN** (hook: "You're broke because you skipped this")

### IDE 3 — "Passive Income dari Saham Dividen Brand Terkenal"
- **(a) Judul:** `How Coca-Cola Pays Me Every 3 Months (Dividend Passive Income Explained)`
- **(b) Alasan demand:** klaster dividen sangat kuat (Coca-Cola 900, JNJ 5.450, HSBC 400, CBA 6.700). Brand terkenal = mudah dipahami non-investor.
- **(c) Keyword:** coca-cola dividend passive income, jnj passive income investment, passive income investment, best passive income
- **(d) Format:** **Explainer panjang 8–12 menit** + potong 1 Short ("$10.000 di Coca-Cola = berapa per bulan?")

### IDE 4 — "Stock Market Basics untuk Pemula Total"
- **(a) Judul:** `Stock Market Basics in 10 Minutes (Explained Like You're 5)`
- **(b) Alasan demand:** "stock market basics" rising 250 + evergreen. Pintu masuk audiens keuangan baru, cocok untuk channel 0 subs.
- **(c) Keyword:** stock market basics, how to invest, what is passive income, personal finance tips
- **(d) Format:** **Explainer panjang 10 menit** (animasi/screen-record sederhana)

### IDE 5 — "Chrome Extensions + Free Apps yang Bikin Kerja 3x Cepat"
- **(a) Judul:** `7 Free Chrome Extensions That Do Your Work For You`
- **(b) Alasan demand:** "most useful chrome extensions" rising 5.950 dan "best free apps for productivity" 450. Mass-appeal tech, nol jargon, CTR tinggi.
- **(c) Keyword:** most useful chrome extensions, best free apps for productivity, ai tools list, free ai tools
- **(d) Format:** **Short 60s EN** (7 klip cepat) + Long 6 menit "full tour"

### IDE 6 — "Cara Pakai ChatGPT untuk Bikin Gambar & Prompt yang Benar"
- **(a) Judul:** `Stop Writing Bad Prompts — 5 ChatGPT Prompts That Actually Work`
- **(b) Alasan demand:** chatgpt image (60), chatgpt images (50), chatgpt prompt (40) semuanya rising; ChatGPT = keyword volume raksasa dan sudah familiar publik.
- **(c) Keyword:** chatgpt prompt, chatgpt image, chatgpt free, chatgpt app
- **(d) Format:** **Short 60s EN** (before/after prompt) + Long 7 menit "prompt pack"

### IDE 7 — "AI Automation Jobs: Karier Baru Bergaji Besar Tanpa Coding"
- **(a) Judul:** `The $90k AI Job Nobody Talks About (No Coding Needed)`
- **(b) Alasan demand:** "ai automation specialist" rising 40; klaster TOP kuat: ai automation jobs, ai automation agency, ai automation course, ai engineer jobs. Motif karier = watch-time tinggi.
- **(c) Keyword:** ai automation jobs, ai automation specialist, what is ai automation, ai workflow automation, ai automation agency
- **(d) Format:** **Explainer panjang 8 menit** + Short "3 skill buat dapetin AI job"

### IDE 8 — "AI untuk Usaha Kecil (UMKM)"
- **(a) Judul:** `How Small Businesses Use AI to Save 10 Hours a Week`
- **(b) Alasan demand:** "ai for small business" = TOP query #1 pada seed small business AI; audiens pemilik usaha = CPM iklan tertinggi (bisnis/keuangan).
- **(c) Keyword:** ai for small business, ai marketing tools, ai marketing automation, how to start a small business
- **(d) Format:** **Explainer panjang 8 menit** + Short "3 tugas UMKM yang harusnya diserahkan ke AI"

### IDE 9 (bonus) — "Cara Mulai YouTube Channel di Era AI"
- **(a) Judul:** `Starting a YouTube Channel in 2026 (AI Does 80% of the Work)`
- **(b) Alasan demand:** "how to start a youtube channel" rising 250; nyambung dengan positioning ZIYAN sebagai channel yang dijalankan agent AI — konten meta yang otentik.
- **(c) Keyword:** how to start a youtube channel, make money online, ai tools you should know in 2026
- **(d) Format:** **Explainer panjang 9 menit** (dokumenter/behind-the-scenes) + Short teaser

---

## 5. Rekomendasi Prioritas Produksi

| Urutan | Ide | Format pertama | Alasan |
|---|---|---|---|
| 1 | IDE 1 (AI Tools 2026 for money) | Short 60s EN | Rising tertinggi, paling aman dari "terlalu teknis" |
| 2 | IDE 2 (AI side hustle students) | Short 60s EN | Audiens muda, viralitas Shorts |
| 3 | IDE 5 (Chrome extensions) | Short 60s EN | Volume besar, produksi termurah |
| 4 | IDE 3 (Coca-Cola dividend) | Long explainer | CPM keuangan tinggi |
| 5 | IDE 7 (AI automation jobs) | Long explainer | Watch-time & niat karier |

**Aturan konten ZIYAN (dari sinyal data):** selalu bingkai AI sebagai **uang, waktu, atau karier** — jangan pernah sebagai daftar model/spesifikasi teknis.

---

## 6. Catatan Teknis (untuk riset berikutnya)
- Venv: `~/.kwenv` (pytrends terinstall). Script: `~/kwresearch.py`, `~/kw2.py`. Data mentah: `~/kwdata.json`.
- Google Trends rate-limit (HTTP 429) sangat agresif: beri jeda ≥20–30 detik antar seed, maksimal ~8–10 seed per sesi.
- Jangan gunakan parameter `retries=`/`backoff_factor=` pada `TrendReq()` (incompatible dengan urllib3 ≥2).
