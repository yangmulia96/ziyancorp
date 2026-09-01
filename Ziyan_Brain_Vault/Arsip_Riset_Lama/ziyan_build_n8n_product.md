# Build Plan: Produk #1 — n8n Workflow Automation untuk UMKM

Tanggal: 2026-08-08 | Riset: 9Router Sonnet 4.5

## A. KEBUTUHAN PASAR (Use-Case Paling Laku)
1. **WhatsApp Business Automation** — auto-reply, notif order, broadcast, follow-up (PALING LAKU)
2. **E-commerce Order Management** — sync Shopee/Tokopedia → Sheet, status kirim, stok, laporan
3. **Lead Gen & CRM Sederhana** — form → Sheet/Notion, auto-follow-up, scoring
4. **Social Media Management** — posting terjadwal, compile mention, auto-DM
5. **Invoice & Payment Reminder** — generate invoice, reminder H-3/H-1/H+1, rekonsiliasi

## B. YANG HARUS DISIAPKAN (Tech Stack)
- n8n (self-host VPS atau n8n.cloud)
- Database: Supabase/PostgreSQL (free tier)
- API: WhatsApp Business (Fonnte/Wablas third-party, lebih murah dari WABA official)
- Integrasi: Google Workspace, Marketplace API
- VPS: Niagahoster/DigitalOcean ($6-12/bulan)

**Skill:** HTTP/REST, webhook, JSON, troubleshooting — TIDAK perlu coding berat
**Deliverable:** Workflow tested + dokumentasi + video tutorial 5-10m + 2 minggu support + SOP maintenance

## C. PRICING (Indonesia UMKM)
- Basic (1 workflow): Rp 2-3 jt
- Standard (2-3 workflow): Rp 5-7 jt
- Premium (multi-platform): Rp 10-15 jt
- Maintenance: Rp 300-500 rb/bulan

## D. KOMPETITOR (Indonesia)
- n8n Indonesia (komunitas Telegram) — edukasi, konsultasi
- Automation Indonesia (FB/Telegram) — Make/Zapier
- Freelancer Fiverr/Upwork — Rp 500k-3jt, no long-term support
- Agensi SaaS lokal — Rp 5-20jt, mahal, slow

**KELEMAHAN KOMPETITOR (ZIYAN ambil):**
1. Tidak fokus UMKM (target enterprise)
2. Harga tidak transparan
3. Onboarding lemah (UMKM butuh edukasi)
4. Maintenance mahal/tidak ada
5. Dokumentasi bahasa Inggris (UMKM bingung)
6. TikTok masih jarang dipakai kompetitor → PELUANG ZIYAN

## E. BUILD PLAN ZIYAN (Produk #1)
### Fase 1: Template Workflow (NOVA + FAZA)
- [ ] WA Auto-Reply + Order Notif (Fonnte API)
- [ ] Shopee Order → Google Sheet Sync
- [ ] Lead Form → Sheet + Auto WA Follow-up
- [ ] Invoice Generator + Reminder

### Fase 2: Packaging & Harga
- [ ] Buat 3 paket (Basic/Standard/Premium) di Link-in-Bio
- [ ] Dokumentasi + video tutorial (Bahasa Indonesia)
- [ ] SOP maintenance

### Fase 3: Marketing (FAZA + PANDA)
- [ ] Carousel TikTok/IG (style @ngoprek.ai): "WA auto-reply gratis? salah, ini cara bener"
- [ ] Landing page di ziyancorp.github.io/automation
- [ ] Cold email outbound (workflow sudah ada)

### Fase 4: Channel & CS (PANDA + ORION)
- [ ] Link-in-Bio + Website sebagai order page
- [ ] Telegram bot CS
- [ ] Closing: ORION draft, Bos approve

## F. AGENT ASSIGNMENT
| Tugas | Agent | Model |
|---|---|---|
| Build workflow n8n | NOVA | Sonnet 4.5 |
| Konten carousel/video | FAZA | Haiku 4.5 |
| Distribusi & CS | PANDA | Flash Lite |
| Riset & pricing | RISA | Sonnet 4.5 |
| Closing & keputusan | ORION | Sonnet 4.5 |
