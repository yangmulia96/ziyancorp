---
name: ziyan-n8n-monetisasi
description: "ZIYAN n8n revenue: template/jasa sebagai otot, Hermes otak."
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
platforms: [windows, linux, macos]
---

# Monetisasi n8n untuk ZIYAN

n8n = **OTOT** (mesin produksi/no-code workflow), Hermes Agent = **OTAK** (riset, naskah, strategi,
QC). ZIYAN pakai n8n untuk cuan NYATA, bukan cuma teori.

## Kapan pakai
- Bos: "cari cara cuan", "template n8n", "jual workflow", "buat jasa otomasi".
- Bangun divisi penjualan template / jasa n8n (revenue cepat, sebelum YouTube monetisasi).

## FAKTA PASAR (riset 2026-08-02, `ziyan_riset_n8n_cuan.md` + `ziyan_riset_template_n8n.md`)
- **Uang terbesar = JASA, BUKAN konten.** Workflow $150–2.000/proyek, retainer $200–1.500/klien/bln
  (margin 85–95%). Channel YouTube sendiri cuma lead magnet, bukan pusat laba.
- Faceless YouTube: $6–15/bln (gratis) s.d $150–250/bln (premium API). Adsense butuh 3–6 bln pertama.
- AI CS UMKM (Indonesia): Rp 3–10 jt setup + Rp 500k–2 jt/bln.
- **Gratis TETAP cuan**: n8n self-host (Docker Community $0) + Gemini free + Edge-TTS + Pexels/Pixabay + FFmpeg + YouTube API.

## CELAH PASAR (supply rendah, demand tinggi)
- Customer Support template: cuma 70 di n8n.io, tapi top template 43.454 views.
- Lead Generation template: 57, demand tinggi.
- WhatsApp chatbot: 71K / 46K / 43K views (paling laku).
- Video AI multi-platform: 214K views (paling laku, tapi ramai juga supply).

## 3 TEMPLATE PERTAMA (rekomendasi, paling cepat cuan)
| # | Nama | Alur node | API (gratis dulu) | Harga |
|---|------|-----------|-------------------|-------|
| 1 | WA CS Auto-Reply UMKM | webhook → AI Agent (Gemini via 9router) → baca Sheets → balas WhatsApp Cloud API | Gemini/9router, Google Sheets, WhatsApp Cloud API | $39 |
| 2 | Lead Gen Google Maps | HTTP Maps → enrich Gemini → simpan Sheets → draft outreach | Google Maps, Gemini/9router, Sheets | $49 |
| 3 | Faceless Content Engine | trigger → naskah → TTS (9router) → compose (Pexels/FFmpeg) → output | 9router TTS, Pexels, FFmpeg | $59–99 |

- Produksi: self-host **npm langsung** (Docker TIDAK wajib, lihat bawah). Skill inti: HTTP Request node + Code node JS + AI Agent node.
  1 template = 1–3 jam (simpel) s.d 1–3 hari (kompleks) + 2–4 jam packaging.

## INSTALL n8n — TANPA DOCKER (utamakan ini di laptop 8GB)
Laptop Bos RAM 8GB → **jangan pakai Docker** (Docker Desktop makan 2–3GB + WSL2 overhead, bikin sesak).
```
npm install -g n8n      # butuh Node.js v18+ (laptop v24 ✅)
n8n start               # http://localhost:5678
```
- Tanpa Docker jalan normal 100%. n8n log bilang "running outside container deprecated, future
  require Docker" — masih bisa dipakai sekarang, bukan blocker.
- Docker cuma opsi kalau ada server terpisah / butuh isolasi production.

## TEMPLATE 4 (baru): IG Automation (gratis)
- Alur: Schedule/Webhook → naskah (NotebookLM/Hermes) → HTTP Request ke Meta Graph API
  (`POST https://graph.facebook.com/v18.0/{ig-user-id}/media`) → publish photo/video.
- Butuh: IG Business account + Meta App + token (gratis daftar; review Meta kalau fitur penuh).
- Gratis selama pakai akun sendiri + token Meta (tidak butuh n8n Cloud berbayar).
- **Gunakan placeholder `{{API_KEY}}` di JSON, JANGAN hardcode credential asli.**

## TEMPAT & CARA JUAL
- Marketplace: Gumroad (rating nyata, $19–180), n8n.io templates (gratis/berbayar $199+), ProductHunt,
  X/Twitter, grup FB, komunitas Discord n8n.
- **Lead magnet terbukti**: "100+ Premium n8n Templates" gratis → 265 rating → funnel ke jasa berbayar.
- Strategi: template $5–50 (pasif, repeat-sell) + jasa $150–2.000 (custom). Gratis buat tarik prospek.

## ALUR EKSEKUSI ZIYAN (agent handle)
1. Riset demand (sudah: `ziyan_riset_template_n8n.md`).
2. Agent divisi buat DRAF JSON per template (`C:\Users\arija\ziyan_n8n_templates\`).
3. Test import di n8n self-host (Docker) sebelum jual — validasi node jalan.
4. Listing Gumroad + README cara jual (`README_jual.md`).
5. **BELUM jual tanpa perintah Bos.** (Pola: siapkan dulu, Bos setuju baru publish.)

## PITFALL
- Jangan jual template "template" kosong → kena Inauthentic Content Policy mentalitas. Beri nilai
  tambah nyata (naskah lokal, QC). Sama seperti video YouTube kita.
- n8n self-host: **npm langsung** (Docker tidak wajib, apalagi di laptop 8GB). Cek Node.js ada.
- WhatsApp Cloud API butuh Meta Business verify (tidak instan) — sertakan panduan di README.
- Jangan hardcode key di JSON template (kebocoran). Pakai env/credential node n8n.
- **DISTRIBUSI TWITTER/X: JANGAN AUTO-POST TANPA APPROVAL BOS.** Correction 2026-08-07:
  Bos bilang "ngabisin saldo aja gak jelas postingan nya" → semua akses X dimatikan
  (`~/.x_credentials` dikosongkan, token dihapus dari `ziyan_keys.env`). Channel lain
  (YouTube/Telegram/Blog) aman. Lihat `references/n8n_v233_operations.md` untuk detail.
- **n8n v2.33 API quirk:** `executeCommand` node DEPRECATED (pakai Code node + child_process),
  activate lewat `POST /workflows/{id}/activate` (bukan PATCH/PUT). Detail di references.

## Referensi
- `references/n8n_v233_operations.md` — install, import, activate via API, node restrictions v2.33,
  cara cari API key tanpa hardcode line, template ZIYAN sudah ada.
- `ziyan_riset_n8n_cuan.md` — model bisnis & angka nyata.
- `ziyan_riset_template_n8n.md` — demand, tempat jual, 3 template lengkap (alur node + API).
- `ziyan_n8n_templates/` — draf JSON + README_jual.md (hasil agent divisi).
