# Riset ZIYAN — 4 Produk Google & Akses AI Agent
Divisi Riset Mendalam · akses sumber: 1 Agustus 2026

## 0. Hasil Tes Nyata di 9router Bos (http://127.0.0.1:20128)

| Tes | Hasil |
|---|---|
| `GET /v1/models/image` | 15 model. Ada: `gemini/gemini-2.5-flash-image` (Nano Banana 1), `gemini/gemini-3.1-flash-image-preview` (Nano Banana 2), `gemini/gemini-3-pro-image-preview` (Nano Banana Pro), `ag/gemini-3.1-flash-image`, + 11 Cloudflare (flux-2-dev, flux-1-schnell, SDXL, lucid-origin, dll) |
| `GET /v1/models` | 115 model chat (kr/*, gemini/*, ag/*, kimi/*, cf/*, nvidia/*, openrouter/*) |
| POST generate `gemini/gemini-2.5-flash-image` | **GAGAL** — `400: API key not valid` (key channel `gemini/` upstream invalid/expired) |
| POST generate `gemini/gemini-3.1-flash-image-preview` | **GAGAL** — sama, key invalid |
| POST chat `gemini/gemini-3.6-flash` | **GAGAL** — `400 API key not valid` → seluruh channel `gemini/` mati |
| POST generate **`ag/gemini-3.1-flash-image`** | **BERHASIL HTTP 200**, b64 image 747.712 char (~560 KB PNG) |
| `gemini-omni-flash` / Veo / Flow di 9router | **TIDAK ADA** (tidak ada endpoint video sama sekali) |

**Kesimpulan operasional:** Nano Banana 2 BISA dipakai ZIYAN sekarang lewat channel **`ag/`**, bukan `gemini/`. Channel `gemini/` butuh key baru dari AI Studio.

## 1. Tabel Per Produk

| Nama | Apa | Status Akses | Bisa agent ZIYAN pakai? | Manfaat produktivitas |
|---|---|---|---|---|
| **Google Flow** (flow.google) | AI creative studio (film/video) Google Labs; frontend untuk Veo 3.1, Nano Banana, Gemini Omni | **Web UI saja**, butuh langganan Google AI (Pro/Ultra), 18+, region-limited. **Tidak ada API Flow** | ❌ Tidak via API. Hanya via `computer_use` (browser automation) seperti skill notebooklm-video | Storyboard→video panjang, scene extend, ingredients-to-video. Pakai manual/otomasi browser |
| **Google Labs** (labs.google) | Etalase eksperimen: Flow, Flow Music, Pomelli (marketing content), Stitch (UI dari prompt), NotebookLM, Literature Insights, Hypothesis Generation, Computational Discovery | Mayoritas **web UI gratis/beta**. Programatik hanya NotebookLM **Enterprise** (Cloud API) | ⚠️ Sebagian: NotebookLM Enterprise API butuh GCP billing. Sisanya browser-automation | Stitch = mockup UI instan; Pomelli = konten marketing on-brand; NotebookLM = riset→audio/video overview |
| **Gemini Omni Flash** | **Model VIDEO**, bukan penerus Gemini 3 Flash teks. Text/image→video, editing video percakapan | **Preview publik** di Gemini API: `gemini-omni-flash-preview` via **Interactions API** (GA). Input: teks/gambar/video ≤10s; output video 3–10s, 720p 24fps; context 1M | ⚠️ Belum ada di 9router. **Bisa** kalau Bos pasang Gemini API key valid + pakai Interactions API langsung | Video pendek otomatis untuk konten sosial ZIYAN, edit klip lewat perintah teks (tanpa editor) |
| **Nano Banana** | Nickname model image Google. NB1 = `gemini-2.5-flash-image`; **NB2 = `gemini-3.1-flash-image`** (0.5K–4K, image-search grounding, aspect 1:8–8:1, text rendering i18n makin bagus); NB Pro = `gemini-3-pro-image` (4K, layout kompleks) | **API publik GA/preview** di Gemini API + tersedia di 9router | ✅ **YA — terbukti jalan** via `ag/gemini-3.1-flash-image` (tes 200 OK) | Thumbnail YouTube, poster, carousel IG, mockup produk, batch konten — ini quick win terbesar |

## 2. Pengalaman Nyata Orang (sumber)

- **Flow/Veo praktis:** panduan lapangan "Guide to Generative Video with Google Veo 3 and Flow" — https://github.com/jgarzik/ai-video/blob/main/veo3-flow-guide.md (workflow prompt → klip 8 detik → chaining).
- **Keluhan nyata Flow/Veo:** thread HN "Google Is Scamming Users with VEO 3, While Delivering VEO 2 Instead" — https://news.ycombinator.com/item?id=44287666 (kredit habis cepat, model fallback diam-diam). **Kontra-bukti**: Flow bukan solusi murah/otomatis.
- **Update resmi Flow:** https://blog.google/technology/ai/veo-updates-flow/ dan https://blog.google/technology/ai/generative-media-models-io-2025/
- **Omni Flash rilis + dev notes:** https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/ · docs https://ai.google.dev/gemini-api/docs/omni · pihak ketiga sudah bungkus jadi produk: https://vivify.video/models/gemini-omni-flash
- **Nano Banana batch untuk konten:** UI batch API buatan dev (klaim 50% lebih murah) https://github.com/aaronkwhite/nanobanana-studio · pola batch arsitektur https://help.apiyi.com/en/nano-banana-pro-architecture-design-batch-image-generation-en.html · library prompt https://nbpro.org/
- **NotebookLM programatik:** https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks (Enterprise-only) · walkthrough https://www.communeify.com/en/blog/notebooklm-enterprise-api-programmatic-notes-workflow/
- **Katalog Labs:** https://labs.google/ · Flow: https://flow.google/about

**Grade keyakinan:** TINGGI untuk semua status akses (dokumen resmi Google + tes lokal). SEDANG untuk klaim hemat batch API pihak ketiga (1 sumber blog). Kontra ditemukan (thread HN Veo).

## 3. Lima Rekomendasi Konkret

1. **PAKAI SEKARANG — Nano Banana 2 via `ag/gemini-3.1-flash-image`.** Sudah terbukti 200 OK di 9router. Jadikan default image generator ZIYAN (thumbnail, poster, carousel). Simpan sebagai skill/helper script.
2. **PERBAIKI DULU — channel `gemini/` di 9router mati** (`API key not valid`). Bos perlu generate key baru di https://aistudio.google.com/apikey lalu update config 9router; ini membuka Nano Banana Pro 4K + Gemini 3.x chat.
3. **TUNGGU/EKSPERIMEN TERBATAS — Gemini Omni Flash.** Masih preview, output max 10 detik 720p, belum ada di 9router. Uji lewat Interactions API langsung setelah key valid; jangan dijadikan pipeline produksi dulu.
4. **JANGAN INTEGRASIKAN API — Google Flow.** Tidak ada API. Kalau butuh video panjang/sinematik, pakai jalur browser-automation (`computer_use`, mirip skill notebooklm-video) atau Veo API langsung, bukan Flow.
5. **QUICK WIN NON-API — Google Labs Stitch + Pomelli** untuk mockup UI & materi marketing; NotebookLM tetap via browser automation (API-nya Enterprise/berbayar GCP, belum worth untuk ZIYAN sekarang).

## 4. Ringkasan untuk Bos

Dari 4 produk, hanya **Nano Banana** yang benar-benar siap pakai agent ZIYAN hari ini — dan sudah saya buktikan dengan generate gambar sungguhan lewat `ag/gemini-3.1-flash-image` di 9router (HTTP 200, ~560 KB). Channel `gemini/` di proxy sedang mati total karena API key upstream invalid, jadi Nano Banana Pro 4K dan Gemini 3.6 Flash belum bisa dipakai sampai key diganti. **Gemini Omni Flash** ternyata bukan model teks melainkan model video preview (`gemini-omni-flash-preview`, output 3–10 detik 720p) yang hanya jalan lewat Interactions API dan belum ada di proxy. **Google Flow** tidak punya API sama sekali — cuma web UI berbayar, dan komunitas mengeluhkan kredit boros serta fallback model diam-diam, jadi lebih cocok dikerjakan lewat otomasi browser. **Google Labs** isinya eksperimen UI (Stitch, Pomelli, NotebookLM) yang berguna manual tapi programatiknya terkunci di NotebookLM Enterprise.

| Prioritas | Tindakan |
|---|---|
| 🟢 Sekarang | Standarkan image gen ZIYAN ke `ag/gemini-3.1-flash-image` |
| 🟢 Sekarang | Ganti Gemini API key di 9router → hidupkan channel `gemini/` |
| 🟡 Eksperimen | Omni Flash video 10 detik via Interactions API (setelah key valid) |
| 🟡 Manual | Stitch/Pomelli/NotebookLM lewat browser automation |
| 🔴 Tunda | Google Flow — no API, boros kredit |
