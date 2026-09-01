# SPEC: Sistem 2 - AI Influencer Content Engine
# Trigger: Telegram bot (@Employeezynbot) - Bos kirim topik/produk
# Output: Full paket konten affiliate (script, caption SOP, visual prompt, asset prompt)

## ARSITEKTUR
Telegram Bot → n8n Workflow → 9Router (LLM) → Google Sheet (tracking) → Output files

## INPUT FORMAT (dari Bos via Telegram)
- Text: "topik: [nama produk/niche], link: [affiliate link], deskripsi: [deskripsi singkat]"
- Atau: forward message dari channel/grup
- Atau: photo + caption

## PROCESSING PIPELINE

### Node 1: Parse Input
- Extract: topic, affiliate_link, description, media_files[]
- Validate: link wajib ada, deskripsi optional

### Node 2: Generate Persona Context
- Load persona config (wajah, style, voice, niche) dari Sheet/JSON
- Consistent character: nama, usia, gaya, background

### Node 3: Content Strategy (3 Format dari Riset)
Format A: Reply-to-comment Demo
- Hook: "User tanya: [pertanyaan]"
- Demo: Screen-record workflow/automation
- CTA: "Coba link di bio"

Format B: Milestone Celebratory
- Hook: "Alhamdulillah [pencapaian]"
- Proof: Screenshot revenue/asset
- Story: Journey singkat
- CTA: "Mau juga? Link di bio"

Format C: Value-First Help
- Hook: "Lagi bantu [adik/teman] cari [lowongan/tool]"
- Value: Rekomendasi spesifik + reasoning
- CTA: "Tracking saya di Sheet, link di bio"

### Node 4: Generate Assets per Format
Per format generate:
- **Video Script** (hook, body, CTA, timing)
- **Caption SOP Bos** (link awal + harga + ≤5 hashtag kreatif)
- **Visual Prompts** (3-5 varian: portrait, lifestyle, flatlay, in-hand, ASMR)
- **Image Generation Prompts** (untuk 9Router/Gemini/Fooocus)
- **Video Generation Prompts** (untuk Veo/Runway/Sora)

### Node 5: Save to Tracking Sheet
Columns: timestamp, topic, format, affiliate_link, script, caption, visual_prompts, status, posted_links

### Node 6: Return to Telegram
- Send: Script + Caption + Visual Prompts (copy-paste ready)
- Optional: Generate sample image via 9Router image endpoint

## PERSONA CONFIG (default ZIYAN)
- Nama: "Celine" / "Mama Potato" / custom
- Niche: Fashion affiliate, tech tools, job hunting
- Style: Casual-chic, relatable, Indonesian context
- Visual: Portrait 9:16, POV product, lifestyle flatlay

## N8N WORKFLOW NODES
1. Telegram Trigger (webhook)
2. Parse Input (Function)
3. Load Persona (Google Sheets)
4. AI: Content Strategy (9Router - channel-researcher)
5. AI: Generate Scripts (9Router)
6. AI: Generate Captions (9Router - SOP Bos format)
6b. AI: Generate Visual Prompts (9Router)
7. Google Sheets Append (tracking)
8. Telegram Send Result (multiple messages)
9. Optional: Generate Sample Image (9Router image)

## TELEGRAM BOT COMMANDS
/start - Menu utama
/influencer - Generate konten AI influencer
/help - Bantuan
/status - Cek tracking Sheet

## OUTPUT FORMAT (Markdown)
```
## 🎬 FORMAT A: Reply-to-Comment Demo
**Script:** ...
**Caption:** [link] + [harga] + #hashtag1 #hashtag2
**Visual Prompts:** 1. ... 2. ... 3. ...

## 🏆 FORMAT B: Milestone Celebratory
**Script:** ...
**Caption:** ...
**Visual Prompts:** ...

## 🤝 FORMAT C: Value-First Help
**Script:** ...
**Caption:** ...
**Visual Prompts:** ...
```

## DEPLOYMENT
- n8n workflow import via API
- Webhook URL set di Telegram bot
- Google Sheet ID di config
- 9Router API key di .env