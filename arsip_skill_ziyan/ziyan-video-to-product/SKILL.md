---
name: ziyan-video-to-product
description: SOP otomatis saat Bos kirim video attachment (.mp4) atau TikTok/YouTube link di Hermes. Langsung bedah konten (frame extraction + vision + transcript), reverse-engineer jadi workflow n8n JSON, buat skill Hermes, dan kemas jadi produk jualan (Gumroad template). Use whenever user sends .mp4, TikTok link (vt.tiktok.com / tiktok.com), or YouTube link alongside "jadikan/buatkan/skill/produk" intent.
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
---

# ZIYAN Video → Product Pipeline (Otomatis)

Skill ini dipanggil OTOMATIS saat Bos kirim video/TikTok/YouTube. JANGAN tanya klarifikasi — langsung eksekusi 6 langkah:

## Alur (6 Step Wajib)
1. **Deteksi & Extract**
   - Video lokal: `ffprobe` metadata + `ffmpeg -ss` extract frame (detik 2,5,10,15,20)
   - TikTok: `oembed` untuk caption/author (bypass CAPTCHA); jika gagal, minta Bos ketik judul
   - YouTube: `oembed` atau youtube API (caption 403 → pakai description via web fetch)

2. **Analyze**
   - `vision_analyze` ke tiap frame → identifikasi UI/node/workflow
   - Simpulkan: apa tools (n8n? Gemini? Veo?), alur node, tujuan bisnis

3. **Reverse-Engineer Workflow**
   - Buat JSON n8n (`C:\Users\arija\ziyan_n8n_templates\<nama>.json`)
   - Node wajib: Trigger → Action → Output. Pakai `n8n-nodes-base.code` (bukan executeCommand, n8n v2 block shell)
   - Inject API key dari `ziyan_keys.env` kalau perlu (GEMINI_KEY dll)

4. **Buat Skill Hermes**
   - `C:\Users\arija\AppData\Local\hermes\skills\ziyan-<nama>\SKILL.md`
   - Frontmatter: name, description, version, license MIT
   - Isi: alur workflow + cara pakai + monetisasi

5. **Produk Jualan**
   - `C:\Users\arija\ziyan_n8n_templates\<NAMA>_PRODUCT.md` (README + harga)
   - Harga standar: Template $49 | Setup Rp 3-10jt | Retainer $200-500/bln

6. **Import ke n8n (kalau jalan)**
   - `curl -X POST localhost:5678/api/v1/workflows` dengan API key (line 44 ziyan_keys.env)
   - Activate: `POST /api/v1/workflows/{id}/activate`

## Tools
- `ffprobe`, `ffmpeg` (extract frame)
- `vision_analyze` (baca frame)
- `terminal` (curl oembed, import n8n)
- `write_file` (skill + workflow + produk)

## Pitfall
- TikTok/YouTube sering CAPTCHA → pakai oembed/description, jangan paksa transcript
- n8n v2 block `executeCommand` → pakai `code` node
- API key invalid/quota → catat, jangan retry mati-matian (video tadi Veo3 gagal 429)
- JANGAN spam/illegal (bobol wifi, hack) — etis ZIYAN

## Contoh yang sudah dibuat
- `affiliate_video_generator.json` (Veo3+NanoBanana) — dari @aichandre
- `cold_email_generator.json` (Sheets→Gemini→Gmail) — dari @aiwithhammad
- Skill: `ziyan-cold-email-automation`, `ziyan-computer-use-cli`, `ziyan-agent-skills`
