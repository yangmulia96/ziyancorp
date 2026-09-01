# RISET PASAR TEMPLATE n8n — untuk ZIYAN
Tanggal riset: data live diambil dari API resmi n8n (`api.n8n.io/templates/search`) + marketplace Gumroad (halaman discover "n8n template").
Semua angka di bawah = angka nyata hasil query, bukan estimasi. Tidak ada credential di dokumen ini.

---

## 1. TEMPLATE PALING DICARI (bukti demand = views di n8n.io + harga jual di Gumroad)

### 1a. Ukuran pasar per kategori (jumlah template terdaftar di n8n.io = indikator kompetisi & minat)

| Kategori (kata kunci) | Jumlah template di n8n.io | Catatan |
|---|---|---|
| AI agent | 3.862 | kategori terbesar, tapi sangat ramai |
| Email / inbox | 1.455 | evergreen, permintaan bisnis stabil |
| Telegram | 1.425 | murah dibangun, banyak pemakai |
| LinkedIn | 478 | lead gen + content, kelas menengah |
| WhatsApp | 388 | **paling relevan untuk pasar Indonesia/UMKM** |
| YouTube | 347 | faceless/shorts pipeline lagi panas |
| RAG | 220 | knowledge base bot |
| SEO | 217 | konten otomatis |
| Instagram | 210 | auto-post video/reels |
| Chatbot | 194 | CS otomatis |
| Social media (multi-platform) | 144 | template view tertinggi ada di sini |
| Scraping | 73 | niche, tapi selalu dibutuhkan lead gen |
| Customer support | 70 | **supply paling sedikit vs demand tinggi = celah** |
| Lead generation (exact) | 57 | supply sangat tipis, celah besar |

**Insight:** yang laku bukan yang paling banyak supply-nya. Rasio terbaik (demand tinggi, supply rendah) = **Customer Support / WhatsApp bot**, **Lead generation**, **Scraping**.

### 1b. 10 template spesifik dengan bukti demand (views nyata di n8n.io)

| # | Template | Views | Kategori | Kenapa laku |
|---|---|---|---|---|
| 1 | Automate Multi-Platform Social Media Content Creation with AI | **205.470** | social auto-post | 1 konten → semua platform |
| 2 | Generate AI Viral Videos with Seedance → TikTok/YouTube/IG | **214.907** | faceless video | pipeline konten AI end-to-end |
| 3 | Build Your First AI Agent | **99.862** | AI agent (starter) | pemula cari titik masuk |
| 4 | AI-Powered WhatsApp Chatbot (teks, voice, gambar, PDF) + memory | **71.396** | chatbot UMKM | WA = kanal utama UMKM |
| 5 | Generate & Auto-post AI Videos to Social Media (Veo3 + Blotato) | **71.279** | social + video | |
| 6 | AI-Powered WhatsApp Chatbot with RAG | **46.989** | RAG + WA | jawab dari dokumen sendiri |
| 7 | AI Customer Support Assistant · WhatsApp Ready · Any Business | **43.454** | CS otomatis | dijual sebagai "cocok semua bisnis" |
| 8 | Automate Product Training & Customer Support via WhatsApp + GPT-4 | **32.249** | CS + training | |
| 9 | Local Chatbot with RAG | **28.717** | RAG self-host | privasi/gratis |
| 10 | AI-Generated LinkedIn Posts + Google Sheets + Email Approval | **27.869** | personal branding | |
| 11 | Create & Upload AI-Generated ASMR YouTube Shorts (Seedance/Fal) | **24.339** | YouTube faceless | |
| 12 | Automated YouTube Video Scheduling & AI Metadata | **17.926** | YouTube ops | |
| 13 | Automate Business Lead Scraping (Apify → Google Sheets) | **17.005** | lead gen/scraping | langsung uang buat agency |
| 14 | Customer Support WhatsApp Bot + Google Docs KB + Gemini | **15.425** | UMKM | Gemini = API gratis |
| 15 | Lead Generation System: Google Maps → Email Scraper → Sheets | 2.412 | lead gen lokal | favorit agency lokal |

### 1c. Bukti "orang benar-benar bayar" (Gumroad, harga live)

| Produk di Gumroad | Harga | Bukti sosial |
|---|---|---|
| 100+ Premium n8n Templates | **$0+** (freemium) | rating 4.9, **265 rating** → bukti model gratis = lead magnet raksasa |
| MY AI AGENTS 2.0 COLLECTION | **$60+** | 4.5 (8 rating) |
| 10.000+ N8N Template Automation Bundle | **$20+** | bundle massal |
| AI DEVELOPER VAULT (template library) | **$299** | 5.0 (8), stok dibatasi "76 left" |
| n8n template: AI Technical Analyst (LLM Vision) | **$25+** | template tunggal |
| Youtube Long Form Playlist n8n Workflow | **$139** | template tunggal niche |
| Shopify Abandoned Cart Recovery Automation | **$70** | ROI jelas → harga naik |
| Telegram→Odoo AI Agent workflow | **$150** | integrasi ERP = premium |
| SEO Pharmacy Blog Automation | **€180** | niche + industri = harga tertinggi |
| Trending SEO Article Writer | $49 | |
| Content Farming v4 (WordPress+Twitter) | $19 | 5.0 (4) |
| Lifetime Membership AI automation | $1.500 (dari $4.999) | model membership |

**Pola harga jelas:** template generic $19–60 · template niche/industri spesifik $70–180 · library/vault $250–300 · membership $1.500+.

---

## 2. TEMPAT & CARA JUAL

| Platform | Model | Biaya | Kelebihan | Kekurangan |
|---|---|---|---|---|
| **n8n.io/workflows** (Creator Hub) | Gratis publish; ada field `price`/`purchaseUrl` (contoh live: "AI Sales Agent WhatsApp/FB/IG" **$199**, "AI Real Estate Agent" **$249**) | 0 | Traffic organik terbesar di dunia n8n, SEO kuat, gratis | Mayoritas template gratis → dipakai sebagai etalase/lead magnet |
| **Gumroad** | Jual langsung file JSON + PDF panduan | ~10% fee | Paling ramai untuk template n8n, checkout instan, bisa $0+ (pay-what-you-want) | Butuh traffic sendiri |
| **Lemon Squeezy / Payhip** | Sama, merchant of record (pajak diurus) | 5–10% | Alternatif Gumroad | Traffic 0 |
| **Product Hunt** | Launch bundle/tool | 0 | Spike traffic 1 hari | Sekali pakai |
| **X/Twitter + LinkedIn** | Konten "build in public" → link Gumroad | 0 | Konversi tertinggi untuk niche AI automation | Butuh konsistensi harian |
| **YouTube** | Tutorial + "template gratis di deskripsi" | 0 | Mesin lead paling awet | Butuh produksi video (ZIYAN sudah punya pipeline) |
| **Grup FB / WA / Telegram Indonesia** | Jual langsung ke UMKM & freelancer | 0 | Pasar lokal minim kompetisi, bisa Rupiah | Harga lebih rendah (Rp50rb–500rb) |
| **Fiverr/Upwork** | Template jadi portofolio → upsell jasa | 20%/10% | Konversi ke proyek $150–2000 | Fee besar |

### Strategi harga rekomendasi ZIYAN
| Produk | Harga | Fungsi |
|---|---|---|
| Template tunggal (starter) | **GRATIS** di n8n.io + email capture di Gumroad ($0+) | Lead magnet — terbukti: 265 rating dari produk $0+ |
| Template niche siap pakai (WA CS bot UMKM) | **$29–49** (Rp199rb–499rb lokal) | Volume |
| Bundle 5–10 template 1 industri | **$99–149** | AOV naik |
| Vault/library + update | **$199–299** | Anchor price |
| Setup + kustomisasi (jasa) | **$150–2.000** | Uang terbesar |
| Retainer maintenance | **$200–1.500/bln** | Cashflow |

**Jawaban soal lead magnet: YA.** Publish gratis di n8n.io = mesin SEO + bukti kredibilitas; template $0+ di Gumroad = mesin email list; monetisasi nyata terjadi di **jasa setup & kustomisasi**. Template = tiket masuk, jasa = kasir.

---

## 3. CARA MEMBUAT

### Skill yang dibutuhkan (urut prioritas)
1. **n8n canvas / drag-drop + koneksi node** — dasar, 1–2 hari belajar.
2. **HTTP Request node** — kunci utama; 80% integrasi "tidak ada node resmi" diselesaikan di sini (REST, header, auth, pagination).
3. **Set / Edit Fields, IF, Switch, Loop Over Items, Merge** — logika alur.
4. **Code node (JavaScript)** — parsing JSON, format tanggal, dedup. Python juga didukung (Pyodide) tapi JS lebih cepat.
5. **AI Agent node + LLM Chat Model + Tools + Memory + Vector Store** — untuk RAG/agent.
6. **Webhook & Trigger** (Webhook, Schedule, Gmail, Telegram, WhatsApp Cloud API).
7. **Error handling + dokumentasi** — pembeda template gratis vs template layak dijual: sticky notes, penamaan node rapi, PDF setup guide.

### Waktu bikin 1 template
| Level | Contoh | Waktu (agent-assisted) |
|---|---|---|
| Sederhana (5–10 node) | RSS → AI ringkas → Telegram | 1–3 jam |
| Menengah (15–25 node) | WA CS bot + Google Sheets KB | 4–8 jam |
| Kompleks (30+ node, RAG/multi-agent) | Faceless YouTube pipeline end-to-end | 1–3 hari |
| + Packaging (PDF guide, screenshot, demo video, listing) | — | +2–4 jam per produk |

### Self-host vs Cloud
| Opsi | Biaya | Rekomendasi |
|---|---|---|
| **Self-host Docker (Community Edition)** | **$0** (VPS $5–6/bln, atau lokal 0) | **PILIH INI.** Eksekusi unlimited, bisa Code node bebas, cocok untuk produksi template massal |
| n8n Cloud Starter | ~$20–24/bln (kuota eksekusi) | Hanya kalau perlu demo cepat/webhook publik tanpa VPS |
| Lisensi | Sustainable Use License: bebas dipakai internal & bikin/jual template JSON; yang dilarang = jual n8n itu sendiri sebagai SaaS | Aman untuk model bisnis kita |

Ekspor template = tombol **Download** → file `.json`. Itulah produk yang dijual. Wajib: hapus semua credential sebelum ekspor (n8n memang tidak mengekspor isi credential, tapi cek ulang field URL/ID).

---

## 4. REKOMENDASI: 3 TEMPLATE PERTAMA ZIYAN

Kriteria: demand terbukti, supply rendah, API gratis, bisa dikerjakan agent tanpa manusia.

### 🥇 Template #1 — "WA CS Auto-Reply UMKM (Knowledge Base Google Sheets)"
- **Demand:** kategori customer support cuma 70 template padahal top template-nya 43.454 & 32.249 views. WhatsApp = kanal #1 UMKM Indonesia.
- **Alur node:** `Webhook (WhatsApp Cloud API)` → `Switch` (teks/gambar/voice) → `Google Sheets` (ambil FAQ/produk) → `AI Agent` (Gemini + Simple Memory) → `IF` (butuh manusia? escalate) → `HTTP Request` (kirim balasan WA) → `Google Sheets` (log chat + lead).
- **API gratis:** Google Gemini API (free tier), Google Sheets (gratis), WhatsApp Cloud API (Meta, gratis 1.000 percakapan/bln), n8n self-host.
- **Target pembeli:** UMKM/toko online Indonesia, klinik, agen properti, freelancer yang jualan lewat WA. Juga agency luar negeri.
- **Harga:** $39 / Rp299rb · upsell setup $150–400.

### 🥈 Template #2 — "Lead Gen Google Maps → Enrich AI → Google Sheets → Email Outreach"
- **Demand:** kategori lead generation hanya 57 template (supply paling tipis); template scraping Apify 17.005 views, Maps→Email 2.412 views. Pembelinya agency = daya beli tinggi.
- **Alur node:** `Form/Schedule Trigger` (kata kunci + kota) → `HTTP Request` (Google Maps/Places atau Apify actor) → `Loop Over Items` → `Code node` (ekstrak email/website, dedup) → `AI Agent` (tulis email personal per lead) → `Google Sheets` (database lead) → `Gmail` (kirim/draft, delay antar kirim).
- **API gratis:** Google Places API (kredit gratis bulanan), Gemini free tier, Gmail, Sheets. Apify opsional (free tier $5 kredit).
- **Target pembeli:** agency digital, sales B2B, freelancer, konsultan. Bahasa Inggris → jual global $49–99.
- **Harga:** $49 · upsell "done-for-you lead list + setup" $300–800.

### 🥉 Template #3 — "Faceless Content Engine: 1 Ide → Video AI → Auto-post YouTube/TikTok/IG"
- **Demand:** view tertinggi seluruh riset — 214.907 & 205.470 & 71.279. ZIYAN sudah punya aset produksi video, jadi biaya marjinal ~0.
- **Alur node:** `Schedule Trigger` → `Google Sheets` (antrian ide) → `AI Agent` (script + hook + judul + hashtag) → `HTTP Request` (TTS/video gen) → `Wait/Poll` (cek status render) → `Google Drive` (simpan) → `YouTube node` (upload + metadata SEO) → `HTTP Request` (post ke IG/TikTok via Blotato/Postiz) → `Sheets` (log + status).
- **API gratis:** Gemini (script), YouTube Data API (gratis, kuota harian), Google Drive/Sheets. Video/TTS pakai free tier dulu (mis. edge-tts lokal / Pexels stok) sebelum upgrade.
- **Target pembeli:** kreator konten, agensi social media, pemilik brand personal, pemain faceless channel.
- **Harga:** $59–99 (paling kompleks) · upsell "channel setup + 30 video" $500–1.500.

### Urutan eksekusi yang disarankan
1. Minggu 1: bangun #1 → publish **gratis** di n8n.io (etalase + SEO) → versi Pro berbayar di Gumroad ($0+ untuk email capture).
2. Minggu 2: bangun #2 → jual $49, promosi di X/LinkedIn + grup agency.
3. Minggu 3: bangun #3 → jadikan demo publik YouTube ZIYAN (video = iklan sekaligus produk).
4. Minggu 4: bundle ketiganya $99–149, dan pasang CTA "butuh custom? mulai $150" di setiap PDF panduan → jalur ke jasa yang nilainya jauh lebih besar.

---

## Catatan risiko
- Kompetisi bundle murah ($20 untuk 10.000 template) menekan harga produk generic → **jangan jual generic, jual niche + panduan + support**.
- Nilai tambah nyata = dokumentasi rapi, video setup 5 menit, dan support 7 hari. Itu yang bikin template $49 laku vs bundle $20 yang tak terpakai.
- Verifikasi ulang view count tiap kuartal; tren video AI berubah cepat (nama model/tool bisa usang).
