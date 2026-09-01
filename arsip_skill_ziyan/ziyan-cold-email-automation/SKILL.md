---
name: ziyan-cold-email-automation
description: Panduan membuat workflow n8n Cold Sales Email Generator (CRM) — baca leads dari Google Sheets, generate email personalisasi via Gemini AI, kirim otomatis via Gmail. Use when Bos ingin bikin/jual template otomasi cold email B2B untuk UMKM/sales team.
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
---

# ZIYAN Cold Email Automation (n8n)

## Alur Workflow (8 node)
1. **Start** (Manual Trigger)
2. **Get Leads** — Google Sheets (read rows: nama, email, perusahaan, konteks)
3. **Generate Cold Email** — Gemini Chat Model + Structured Output Parser
   - Prompt: tulis email personalisasi dari data lead, hook 1 baris, CTA jelas
4. **Format Output** — rapikan teks (hapus markdown, signature)
5. **Update Sheet** — tandai status "sent" / simpan draft
6. **Send Cold Email** — Gmail node (send: message)

## Keunggulan
- Personalisasi massal tanpa manual
- Gemini free tier cukup untuk volume kecil
- Sheets = CRM murah UMKM

## Cara Pakai (ZIYAN)
- Import `cold_email_generator.json` ke n8n (ID workflow ZIYAN)
- Set credentials: Google Sheets OAuth, Gmail OAuth, Gemini API Key
- Isi Sheets: kolom `name | email | company | context`
- Klik Execute → email terkirim otomatis

## Monetisasi (Pillar 2: n8n Jasa)
- **Template**: $49 (Gumroad) — lifetime, update gratis
- **Setup jasa**: Rp 3-10jt (custom + training UMKM)
- **Retainer**: $200-500/bln (maintenance + optimasi prompt)

## Pitfall
- JANGAN spam (bisa kena block Gmail / UU ITE)
- Batasi 50-100 email/hari per akun
- Selalu ada unsubscribe/opt-out
- Test dulu ke 5 lead sendiri sebelum blast

## Referensi
- Video: @aiwithhammad TikTok "Cold Sales Email Generator"
- Stack: n8n + Google Sheets + Gemini + Gmail
