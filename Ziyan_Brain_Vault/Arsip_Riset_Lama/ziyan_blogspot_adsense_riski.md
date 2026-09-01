# Riset: Blogspot/Blogger + AdSense dengan Konten FULL-AI (ZIYAN, 2026)

Sumber: dokumentasi resmi Google (diambil langsung via curl, Feb 2026).
- support.google.com/adsense/answer/9724 (Eligibility requirements)
- support.google.com/adsense/answer/9335564 & /1348688 (Google Publisher Policies)
- developers.google.com/search/docs/essentials/spam-policies (Spam Policies — wajib dipatuhi publisher AdSense)
- developers.google.com/search/docs/fundamentals/creating-helpful-content
- developers.google.com/blogger/docs/3.0/using + reference/posts/insert (Blogger API v3)

---

## 1. Ringkasan Temuan Kunci (kutipan resmi)

**AdSense eligibility (2026, halaman masih live):**
> "If you have your own content that meets our policies and you're 18 or over, you can sign up for AdSense."
> "Your content must be **high-quality, original, and attract an audience**."
> "If you use an AdSense **host partner (like Blogger)**, you can sign up for a **hosted AdSense account**... you must meet certain eligibility requirements."

→ **Blogger tetap host partner resmi AdSense di 2026.** Jalur hosted account masih ada.

**Google Publisher Policies — pasal yang paling mematikan untuk blog AI massal:**
> "Google-served ads on screens **without publisher-content or with low-value content**" = dilarang (Inventory value).
> "You must not place Google-served ads on screens that violate the **Spam policies for Google web search**." ← ini yang mengikat AdSense ke spam policy Search.

**Spam Policies for Google Web Search — "Scaled content abuse":**
> "Scaled content abuse is when many pages are generated for the primary purpose of manipulating search rankings and not helping users... creating large amounts of **unoriginal content that provides little to no value to users, no matter how it's created**."
> Contoh: "**Using generative AI tools or other similar tools to generate many pages without adding value for users**"; scraping feed/hasil pencarian; automated transformations (synonymizing/translating/obfuscation); stitching konten.

**Creating Helpful Content (update 2025-12-10) — sisi yang MEMBOLEHKAN AI:**
> "Many types of content may have a 'How' component... That can include **automated, AI-generated, and AI-assisted content**."
> Pertanyaan wajib: apakah penggunaan AI **self-evident lewat disclosure**? apakah dijelaskan kenapa AI dipakai?
> "If you use automation, including AI-generation, to produce content **for the primary purpose of manipulating search rankings, that's a violation of our spam policies**."

→ **Kesimpulan hukum-kebijakan: Google TIDAK melarang AI-generated content per se. Yang dilarang adalah SKALA + TANPA NILAI TAMBAH + niat manipulasi ranking.** Bedanya bukan "siapa yang menulis" tapi "apakah ada nilai orisinal & audiens nyata".

**Kata kunci pemicu penolakan/disable:** *low value content*, *scaled content abuse*, *unoriginal content*, *no added value*, *content primarily for search engines*, *misrepresentative content* (menyembunyikan siapa pembuat konten), *thin/duplicate*, *auto-spin/synonymized/translated scrape*, *site without publisher content*.

**Blogger API v3 (teknis):**
- `POST https://www.googleapis.com/blogger/v3/blogs/{blogId}/posts` — "Adds a post. Requires authorization."
- Scope: `https://www.googleapis.com/auth/blogger`. OAuth 2.0 wajib untuk data privat (API key hanya untuk baca publik).
- **Gratis** (tidak ada biaya API), kuota default Google API standar (ribuan request/hari) — jauh di atas kebutuhan autopost.
- Refresh token bisa disimpan → agent Hermes bisa post 24/7 tanpa manusia. **Feasibility teknis: 100% BISA.**

---

## 2. Tabel Utama

| Aspek | Fakta Resmi / 2026 | Risiko | Rekomendasi |
|---|---|---|---|
| **Daftar AdSense via Blogspot** | Masih bisa. Blogger = AdSense **host partner**; jalur *hosted account* aktif (answer/9724, live 2026). Syarat: 18+, konten orisinal & berkualitas, punya audiens | Approval makin ketat; blog domain `.blogspot.com` baru + konten tipis sering ditolak berulang ("low value content") | Boleh dicoba, tapi **jangan andalkan** subdomain blogspot; siapkan 20–30 artikel benar-benar berguna sebelum apply |
| **Kebijakan AI content** | AI **tidak dilarang**. Yang dilarang: *scaled content abuse* — "generative AI... to generate many pages without adding value" | Autopost 5–20 artikel/hari hasil LLM tanpa data orisinal = definisi harfiah scaled content abuse | Boleh AI-assisted, **wajib** ada data/analisis orisinal + disclosure AI. Batasi 1–2 post/hari |
| **Deteksi & sanksi** | Publisher Policies: ads dilarang di screen "low-value content"; wajib patuh Spam Policies Search. Sanksi: blokir iklan → suspend → terminate | Disable akun AdSense = **ban Google account level**, bisa merembet ke jalur monetisasi lain (YouTube AdSense pakai payment profile yang sama) | **Jangan pakai akun Google utama ZIYAN** yang juga dipakai YouTube/OAuth produksi |
| **Teknis autopost** | Blogger API v3 `posts.insert`, scope `auth/blogger`, OAuth2 refresh token, gratis | Rendah (teknis). Risikonya bukan API, tapi policy | Bangun skill autopost, tapi pasang **gate kualitas** (bukan volume) |
| **Ekonomi RPM** | AdSense display blog niche tech/AI umumnya **$1–8 RPM** (tech rendah, finance/insurance tinggi); traffic organik blog baru anjlok pasca core update 2024–2025 + AI Overviews memotong klik | Blog baru 2026 realistis <1.000 pageview/bulan di 6 bulan pertama → pendapatan ~$0–5/bln | **Bukan** kanal revenue utama. ROI per jam agent jauh di bawah YouTube/produk |
| **AI-content flooding** | Google merilis kebijakan *scaled content abuse* (Mar 2024) & *site reputation abuse* justru karena banjir konten AI; ribuan situs AI ter-deindex | Kompetisi konten AI = CPC/RPM tertekan + risiko deindex | Kalau tetap jalan: pilih niche sempit + data orisinal (benchmark, harga, hasil eksperimen agent) |
| **Kasus disable nyata** | Data forum tidak bisa diverifikasi otomatis (Reddit/DDG memblokir scraping dari host ini) — **tidak diklaim sebagai fakta**. Yang terverifikasi: kebijakan Google eksplisit menyasar pola ini dan menyebut sanksi terminate | Bukti anekdot tidak terkumpul; risiko kebijakan tetap tinggi & terdokumentasi resmi | Perlakukan sebagai **risiko tinggi terdokumentasi**, bukan rumor |

*Catatan kejujuran data: angka RPM di atas adalah rentang industri umum, bukan kutipan dokumen Google. Google tidak mempublikasikan RPM. Klaim "berapa banyak akun disable" TIDAK dapat saya verifikasi — akses Reddit/DDG diblokir dari host ini.*

---

## 3. 5 Rekomendasi Konkret untuk ZIYAN

1. **JANGAN jadikan Blogspot+AdSense full-AI sebagai jalur revenue utama.** Ekspektasi realistis 6 bulan pertama: <$10/bulan. Effort agent lebih bernilai di YouTube/produk digital.
2. **HINDARI mode "full-AI autopost volume tinggi" (≥3 post/hari, artikel generik).** Itu persis definisi *scaled content abuse* di dokumen resmi Google → jalur cepat ke penolakan/terminate.
3. **BOLEH jalan sebagai eksperimen berbiaya nol, dengan pagar:** akun Google **terpisah** (bukan akun YouTube/produksi ZIYAN), 1 post/hari maksimal, tiap post wajib memuat **data orisinal** yang cuma ZIYAN punya (hasil benchmark model 9router, log eksperimen agent, perbandingan harga API) + disclosure "ditulis dengan bantuan AI, diverifikasi oleh …".
4. **Apply AdSense hanya setelah 25–30 artikel + trafik organik nyata (>500 sesi/bln).** Apply terlalu dini = rejection loop "low value content" yang mencemari histori akun.
5. **Bangun asetnya tetap, tapi outputnya diarahkan ulang:** blog dipakai sebagai *SEO landing + arsip* untuk konten YouTube ZIYAN dan katalog produk, bukan sebagai mesin AdSense. Monetisasi via affiliate/produk sendiri tidak punya risiko ban seperti AdSense.

**Verdict: HINDARI mode full-AI murni untuk AdSense. Jalankan versi "AI-generated + data orisinal + volume rendah + akun terisolasi" saja, sebagai side-asset, bukan pilar revenue.**
