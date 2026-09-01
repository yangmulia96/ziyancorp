# SPEC: Sistem 3 - Value-First Help + Systematic Tracking
# Trigger: Telegram bot (@Employeezynbot) - User tanya butuh bantuan
# Output: Jawaban bantu + Update tracking Sheet otomatis

## ARSITEKTUR
Telegram Bot → n8n Workflow → 9Router (LLM) → Google Sheet (tracking database) → Response ke User

## INPUT FORMAT (dari User via Telegram)
- Text: pertanyaan/tanya bantuan
- Contoh: "cari lowongan Network Engineer Jakarta", "rekomendasi VPS murah worth it", "bantu bikin CV"

## PROCESSING PIPELINE

### Node 1: Classify Intent
Kategori bantuan:
- **Job Search**: cari lowongan, filter, apply
- **Tool Recommendation**: VPS, hosting, software, AI tools
- **Content Help**: bikin CV, portfolio, script video
- **Technical**: debug, setup, config
- **General**: info, motivasi, arahan

### Node 2: Execute Help (per kategori)

#### Job Search
- Search via API (Indeed, LinkedIn, Kalibrr, Glints) atau scraping
- Filter: lokasi, gaji, remote/WFH, skill match
- Return: Top 3-5 lowongan dengan reasoning

#### Tool Recommendation
- Knowledge base: VPS (DigitalOcean, Vultr, Linode, Contabo), Hosting, AI tools
- Match: budget, use case, spec butuh
- Return: Rekomendasi + pros/cons + referral link (affiliate)

#### Content Help
- Generate: CV template, portfolio structure, script video
- Review: CV user (kalau kirim file), kasih feedback
- Output: File/template siap pakai

#### Technical
- Debug: baca error log, kasih solusi
- Setup: step-by-step guide
- Config: generate config file

### Node 3: Systematic Tracking (Google Sheet)
Columns:
- timestamp, user_id, username, kategori, query, response_summary
- items_found (JSON), ratings (1-10), reasoning, status (open/closed/helpful)
- follow_up_needed (boolean), affiliate_links_used

Rating system:
- 10 = solved completely
- 7-9 = partial help
- 4-6 = info given tapi butuh follow up
- 1-3 = gagal bantu

### Node 4: Generate Response
Format response:
- **Jawaban langsung** (solusi/actionable)
- **Detail items** (lowongan/tool/CV template)
- **Reasoning** (kenapa rekomendasi ini)
- **Next steps** (user lakukan apa)
- **Tracking ID** (buat follow up)

### Node 5: Update Sheet + Reply Telegram
- Append ke Sheet
- Kirim response ke user (Markdown formatted)

## GOOGLE SHEET STRUCTURE
Tab 1: "Help_Log" - semua interaksi
Tab 2: "Job_Listings" - cache lowongan (dedup)
Tab 3: "Tool_DB" - database rekomendasi tool
Tab 4: "User_Profile" - preferensi user (budget, lokasi, skill)

## TELEGRAM BOT COMMANDS
/bantuan - Menu bantuan kategori
/cari_kerja [posisi] [lokasi] - Job search
/rekomendasi_tool [kebutuhan] [budget] - Tool recommendation
/bikin_cv - Generate CV template
/debug [error] - Technical help
/status [tracking_id] - Cek status bantuan sebelumnya

## KNOWLEDGE BASE (untuk 9Router context)
- VPS providers: specs, harga, referral codes
- Job boards: API endpoints, selectors
- CV templates: format ATS-friendly
- Common tech issues & solutions
- Affiliate links tracking

## AUTOMATION RULES
- Auto-dedup job listings (by company+position+link)
- Auto-rate response quality (user feedback: 👍/👎)
- Weekly summary report ke Bos (top queries, success rate)
- Escalation: kalau rating < 4 → flag ke Bos

## OUTPUT FORMAT (Response ke User)
```
## 🤝 Bantuan: [Kategori]

**Solusi:**
[Jawaban singkat actionable]

**Detail:**
1. [Item 1] - [Reasoning] - ⭐[Rating]
2. [Item 2] - [Reasoning] - ⭐[Rating]
3. [Item 3] - [Reasoning] - ⭐[Rating]

**Next Steps:**
[Langkah konkret user]

**Tracking ID:** `#HL-20260810-001`
(Balas "👍" kalau membantu, "👎" kalau kurang)
```

## DEPLOYMENT
- n8n workflow import
- Google Sheet template (4 tab)
- 9Router context injection (knowledge base)
- Telegram webhook