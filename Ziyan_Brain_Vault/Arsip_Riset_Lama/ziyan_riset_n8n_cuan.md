# RISET ZIYAN — CARA MENGHASILKAN UANG DENGAN n8n
**Divisi Riset Mendalam | Untuk: Bos (Komisaris) | Fokus: monetisasi praktis, bukan teori**
Sumber harga: halaman pricing resmi (dicek langsung, Agustus 2026) + laporan praktisi. Tidak ada credential di dokumen ini.

---

## RINGKASAN EKSEKUTIF (baca ini saja kalau buru-buru)

1. **Uang terbesar dari n8n BUKAN dari konten, tapi dari JASA** (bikin workflow untuk klien). Margin 80–95%, bayar di muka, tidak tergantung algoritma.
2. **YouTube faceless pakai n8n itu real tapi lambat cuannya**: biaya operasional ~$50–120/bulan/channel, monetisasi baru mungkin setelah 1.000 subs + 4.000 jam tonton, dan sekarang dihantam **YouTube Inauthentic Content Policy (Juli 2025)** — konten mass-produced/repetitive bisa ditolak monetisasi.
3. **Ada jalur gratis yang tetap cuan** (n8n self-host + Pexels/Pixabay + Edge-TTS + FFmpeg): biaya bisa ditekan ke **~$0–7/bulan**, tapi trade-off = waktu setup dan kualitas suara.
4. **Rekomendasi ZIYAN: YA — jadikan n8n MESIN PRODUKSI (otot), Hermes Agent tetap OTAK (strategi, riset, QC).** Model monetisasi utama: **jual jasa otomasi + AI agent ke UMKM/agency**, konten YouTube sebagai *portfolio & lead magnet*, bukan sumber utama.

---

## 1. MODEL BISNIS NYATA + ANGKA

### (a) Jasa pembuatan workflow otomasi (freelance / agency) — **PALING TERBUKTI**

| Jenis pekerjaan | Tarif pasar global (USD) | Tarif pasar Indonesia (IDR) | Waktu kerja |
|---|---|---|---|
| Workflow sederhana (form → Sheet → WA/Email) | $150 – $500 | Rp 1,5 – 5 jt | 2–6 jam |
| Workflow menengah (multi-API, scraping, DB) | $500 – $2.000 | Rp 5 – 20 jt | 1–3 hari |
| Sistem kompleks (AI agent + CRM + RAG) | $2.000 – $10.000 | Rp 20 – 80 jt | 1–4 minggu |
| Rate per jam (Upwork/Fiverr, tag "n8n") | $25 – $150/jam | Rp 300k – 1,5 jt/jam | — |
| **Retainer maintenance/hosting** (kunci cuan) | **$200 – $1.500/bulan/klien** | **Rp 2 – 15 jt/bulan** | 2–5 jam/bulan |
| "Automation audit" (jual dulu sebelum bangun) | $300 – $1.000 sekali | Rp 3 – 10 jt | 1 hari |

**Kenapa ini paling cuan:** biaya bahan baku ~$0 (n8n self-host gratis, VPS $5/bln). Margin kotor 85–95%. Pembayaran di muka 50%. Yang dijual = *hasil bisnis klien* ("hemat 20 jam/bulan"), bukan jam kerja.

**Pola agency yang jalan:** 5 klien retainer × $500/bln = **$2.500/bulan recurring** dengan beban kerja <20 jam/bulan. Ini angka realistis yang banyak dilaporkan solo operator n8n di tahun 1–2.

### (b) YouTube automation / faceless channel pakai n8n

**Pipeline standar (node-per-node):**
```
Schedule Trigger (cron 1x/hari)
 → Google Sheets / Airtable (ide + status)
 → OpenAI / Gemini (riset topik → script 60–90 detik + hook)
 → TTS (ElevenLabs / Edge-TTS gratis)  → audio URL
 → Visual: Pexels/Pixabay API (stock, gratis) ATAU FAL/Runway (AI video, bayar)
 → JSON2Video / Creatomate / FFmpeg-on-VPS (render + subtitle burn-in)
 → OpenAI (judul, deskripsi, tag, thumbnail prompt)
 → YouTube Data API v3 (upload otomatis)
 → Sheets update + notifikasi Telegram/Discord (QC manusia/agent)
```

**Potensi revenue (jujur, bukan hype):**

| Skenario | Views/bulan | RPM | Adsense/bulan |
|---|---|---|---|
| Channel baru 0–3 bln (belum monetisasi) | <50k | — | **$0** |
| Channel jalan (niche umum, audiens global) | 300k | $1,5 | ~$450 |
| Niche tinggi (finance/tech/US audience) | 300k | $6–12 | $1.800 – $3.600 |
| Shorts saja (RPM rendah) | 1 jt | $0,05–0,15 | $50 – $150 |

**Realita:** 8–9 dari 10 channel faceless mati sebelum monetisasi. Yang cuan biasanya bukan dari Adsense tapi dari **affiliate + jual produk/jasa sendiri** (CPM tidak penting kalau 1 video mendatangkan 1 klien $500).

### (c) Lead generation / prospecting B2B otomatis

| Model | Harga pasar |
|---|---|
| Jual list lead ter-enrich (scrape Maps/LinkedIn + AI qualify) | $0,20 – $2 per lead |
| "Lead gen system" dibangun untuk klien (sekali bangun) | $1.500 – $5.000 |
| Managed lead-gen retainer (30–100 lead/bln + cold email) | $1.000 – $3.000/bulan |
| Pay-per-appointment (janji temu terverifikasi) | $50 – $300 per appointment |

Stack umum: Google Maps/Apify scrape → n8n → enrichment (Apollo/Hunter) → AI personalisasi → Instantly/Smartlead → CRM. **Risiko: hukum data & spam (GDPR/CAN-SPAM), domain warming wajib.** Untuk pasar Indonesia (UMKM), versi WhatsApp jauh lebih efektif daripada cold email.

### (d) AI agent / chatbot dijual ke UMKM

| Paket | Setup | Bulanan |
|---|---|---|
| Chatbot FAQ WhatsApp/IG (RAG dari katalog) | Rp 3 – 10 jt ($200–700) | Rp 500k – 2 jt |
| CS agent + booking + follow-up otomatis | Rp 10 – 30 jt | Rp 1,5 – 5 jt |
| Voice/AI receptionist (global market) | $1.000 – $3.000 | $300 – $1.000 |

Ini **paling cocok untuk pasar Indonesia**: UMKM paham "bot bales chat pelanggan 24 jam", tidak paham "workflow orchestration". Biaya jalan per klien: LLM ~$3–15/bulan → margin >90%.

### (e) Model lain yang terbukti

| Model | Angka |
|---|---|
| **Jual template workflow** (Gumroad/n8n marketplace) | $10–97/template; top seller $1k–5k/bln, mayoritas <$100/bln |
| **Kursus/komunitas n8n** (berbayar) | $30–100/bln/member; skala kecil sekalipun 50 member = $2.500/bln |
| **Konten edukasi n8n** (YouTube/newsletter) → funnel ke jasa | Channel n8n-tutorial paling cepat monetisasi karena CPM tinggi (B2B) |
| **Micro-SaaS di atas n8n** (workflow dibungkus jadi produk berlangganan) | $19–99/bln/user, butuh produk & support |
| **Content-as-a-service** (bikinin 30 short/bln untuk brand) | $500 – $2.500/bulan/klien |

---

## 2. BIAYA & TOOLS — 1 CHANNEL FACELESS (30 video/bulan)

| Komponen | Tool | Harga aktual | Estimasi/bulan |
|---|---|---|---|
| Orkestrator | n8n Cloud Starter | ~€20–24/bln (2.500 eksekusi) | $24 |
| Orkestrator (alternatif) | **n8n self-host (Community, gratis)** + VPS | VPS $5–12 | **$6** |
| Script/LLM | GPT-4o-mini / Gemini Flash | ~$0,05–0,20 per script | $3 – $8 |
| TTS | **ElevenLabs Starter $5** / Creator $22 / Pro $99 | Starter ≈ 30 menit audio | $5 – $22 |
| Render video | **JSON2Video** — Free 600 kredit; $16,95/bln (3.000 kredit) ; $49,95 (12.000) ; $99,95 (30.000). 1 kredit = 1 detik video | 30 video × 60 dtk = 1.800 kredit → paket $16,95 | $17 |
| Stok visual | **Pexels / Pixabay API — GRATIS** | $0 | $0 |
| Visual AI (opsional) | FAL.ai / Runway / Kling | $0,02–0,50 per klip | $0 – $60 |
| Musik | Suno Pro ~$10/bln (atau musik free-license) | opsional | $0 – $10 |
| Thumbnail | GPT-image / Flux via FAL | ~$0,03–0,05/gambar | $1 – $3 |
| YouTube Data API | **GRATIS** (kuota 10.000 unit/hari; 1 upload ≈ 1.600 unit → maks ~6 upload/hari) | $0 | $0 |
| Storage/CDN | Cloudflare R2 / Drive | $0 – $5 | $2 |

**TOTAL:**
- **Paket hemat (self-host + TTS gratis + Pexels + FFmpeg):** **$6 – $15/bulan**
- **Paket standar (kualitas jual):** **$55 – $80/bulan**
- **Paket premium (AI visual + suara premium):** **$150 – $250/bulan**

> Catatan penting: 1 channel = ~$60/bln. Break-even Adsense butuh ~40k views/bulan di RPM $1,5. Artinya **channel harus sudah termonetisasi dulu**, dan itu 3–6 bulan tanpa pemasukan.

---

## 3. JALUR GRATIS YANG MASIH CUAN

| Kebutuhan | Versi berbayar | **Alternatif gratis** | Trade-off |
|---|---|---|---|
| Orkestrator | n8n Cloud €20+ | **n8n self-host (fair-code, gratis, unlimited eksekusi)** | urus VPS/Docker sendiri |
| LLM | GPT-4o $$ | Gemini Flash free tier, Groq free, model free via proxy (9router) | rate limit, kualitas variatif |
| TTS | ElevenLabs $22 | **Edge-TTS (Microsoft, gratis, kualitas mengejutkan bagus)**, Piper, Kokoro | tidak ada voice cloning |
| Video render | JSON2Video $17 | **FFmpeg di VPS sendiri** (Remotion/MoviePy) | perlu coding, CPU time |
| Stok visual | Storyblocks | **Pexels + Pixabay API gratis (butuh atribusi minimal)** | visual generik/berulang |
| Musik | Suno $10 | Pixabay Music, YouTube Audio Library | pilihan terbatas |
| Subtitle | tool berbayar | Whisper lokal / faster-whisper | butuh CPU/GPU |
| Upload | — | YouTube Data API gratis | kuota 6 upload/hari |
| Database | Airtable Pro | Google Sheets / Postgres di VPS | — |

**Kesimpulan:** stack **$0–7/bulan yang 100% fungsional itu nyata** (VPS + n8n self-host + Gemini free + Edge-TTS + Pexels + FFmpeg). Ini justru **stack paling cocok untuk ZIYAN** karena kita punya kapasitas teknis dan tidak punya beban gaji manusia. Uangnya dipakai untuk hal yang benar-benar membedakan (riset & QC), bukan untuk render.

---

## 4. RISIKO — KENAPA ORANG GAGAL CUAN PAKAI n8n

| Risiko | Dampak | Mitigasi |
|---|---|---|
| **YouTube Inauthentic Content Policy (berlaku 15 Juli 2025)** | Konten "mass-produced & repetitive" ditolak YPP / demonetisasi. Template n8n faceless generik (TTS robot + slideshow stok) adalah target langsung kebijakan ini | Wajib ada **nilai tambah nyata**: sudut pandang orisinal, data/riset sendiri, komentar/analisis, visual kustom. Jangan 1 template dipakai 100 video |
| Semua orang pakai template yang sama | 10.000 channel dengan intro & voice ElevenLabs identik → CTR jatuh, audiens skip | Diferensiasi di *level naskah* (otak), bukan di tool |
| Bakar duit di API sebelum ada revenue | Rugi $60–250/bln × 6 bulan | Mulai dari stack gratis, upgrade setelah ada traffic/klien |
| Fokus jual "n8n" bukan jual "hasil" | Klien tidak beli tool, klien beli hemat waktu/uang | Pitch: "hemat 20 jam/bulan" bukan "saya bikin workflow" |
| Workflow rapuh (API berubah, error diam-diam) | Klien kabur, reputasi hancur | Wajib error-handling node + alert + retainer maintenance (justru sumber recurring) |
| Self-host tumbang / kredensial bocor | Downtime, insiden keamanan | Backup, monitoring, isolasi kredensial (jangan pernah di dokumen/repo) |
| Lisensi n8n (fair-code / Sustainable Use License) | Tidak boleh jual n8n itu sendiri sebagai SaaS multi-tenant tanpa lisensi embed | Jual **jasa & hasil**, bukan hosting n8n sebagai produk |
| Cold email/scraping melanggar aturan | Domain diblacklist, masalah hukum | Gunakan channel yang diizinkan (WA business API, opt-in), warming domain |

---

## 5. REKOMENDASI UNTUK ZIYAN

### Apakah n8n layak jadi MESIN PRODUKSI? **YA — tapi hanya sebagai OTOT, bukan OTAK.**

| Lapisan | Tool | Alasan |
|---|---|---|
| **OTAK** (strategi, riset, naskah, QC, keputusan) | **Hermes Agent** (multi-agent, skill, memory, reasoning) | n8n tidak bisa "berpikir" — ia hanya menjalankan graf tetap. Diferensiasi ZIYAN ada di sini, dan ini juga jawaban atas Inauthentic Content Policy |
| **OTOT** (render, upload, retry, jadwal, integrasi API) | **n8n self-host (gratis)** | Node siap pakai untuk ElevenLabs/JSON2Video/YouTube/Sheets, retry & queue bawaan, visual & mudah diserahkan/dijual ke klien |
| **Jembatan** | Hermes → webhook → n8n → callback ke Hermes | Hermes menulis "brief JSON", n8n mengeksekusi, Hermes mem-QC hasil |

### Urutan monetisasi yang disarankan (prioritas)

| Prioritas | Model | Kenapa cocok untuk perusahaan 100% agent | Target realistis |
|---|---|---|---|
| **#1** | **AI agent / chatbot CS untuk UMKM Indonesia** | Margin >90%, ZIYAN bisa bangun & rawat tanpa manusia, pasar paham masalahnya | 3 klien × Rp 1,5 jt/bln = Rp 4,5 jt recurring dalam 60–90 hari |
| **#2** | **Jasa workflow otomasi + retainer** (lokal & global/Upwork) | Bayar di muka, tidak tergantung algoritma platform | 1 proyek Rp 5–15 jt + retainer |
| **#3** | **Content-as-a-service** (produksi 30 short/bln untuk brand) | Pakai pipeline yang sama dengan channel sendiri → biaya marjinal ~$0 | Rp 5 jt/bln/klien |
| **#4** | **Channel YouTube ZIYAN (Compound Daily)** | **Bukan pusat laba — ini portofolio & lead magnet** yang membuktikan kemampuan kita ke calon klien #1–#3 | Monetisasi Adsense = bonus, bukan target |
| **#5** | Template/kursus otomasi (produk digital) | Aset pasif setelah #1–#3 terbukti | nanti |

### Langkah 30 hari
1. Pasang **n8n self-host di VPS** (biaya ~$6/bln), bukan n8n Cloud. Kredensial disimpan di vault n8n, tidak pernah keluar log.
2. Bangun **1 pipeline produksi video** dengan stack gratis dulu (Gemini/Edge-TTS/Pexels/FFmpeg). Ukur waktu & biaya per video.
3. Tambahkan **gerbang QC oleh Hermes** sebelum upload — ini yang menyelamatkan kita dari kebijakan konten inautentik.
4. Paralel: siapkan **paket jual "AI CS WhatsApp UMKM"** (Rp 5 jt setup + Rp 1,5 jt/bln), demo pakai pipeline sendiri.
5. Baru upgrade ke ElevenLabs/JSON2Video **setelah ada pembayar pertama**.

**Satu kalimat untuk Bos:** n8n adalah pabriknya, Hermes adalah insinyurnya — dan uang tercepat bukan dari menonton, tapi dari menjual pabrik itu ke orang lain.
