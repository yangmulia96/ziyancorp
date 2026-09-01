# Ziyan Automation Systems (ZAS) — Enterprise n8n Workflow Engine

Selamat datang di **Ziyan Automation Systems (ZAS)**, divisi otomasi bisnis & AI B2B resmi milik **ZiyanCorp**.

Sistem ini dirancang khusus untuk membangun, menguji, dan mendistribusikan solusi otomasi alur kerja (*Workflow Automation*) berbasis **n8n** dan **AI Agents** untuk pasar B2B (UMKM, Toko Online, Klinik, Agensi, dan Korporat).

---

## 🛡️ Aturan Isolasi & Standar Perusahaan (Corporate Isolation Rule)
* Sistem ini beroperasi secara **independen dan terisolasi total** dari pipeline personal/kreator (seperti Celine Aurel atau Arijal Meutuwah).
* Menggunakan standar penamaan, kredensial korporat, dan struktur modular berstandar enterprise.

---

## 📂 Struktur Repositori

```text
ziyan_n8n_core/
├── config/
│   ├── .env.example                 # Template environment variables
│   └── settings.json                # Pengaturan engine & endpoint
├── workflows/                       # Workflow JSON Resmi yang Siap Diimpor ke n8n
│   ├── 01_whatsapp_ai_lead_qualifier.json
│   ├── 02_ecommerce_invoice_pdf_generator.json
│   ├── 03_b2b_lead_scraper_enricher.json
│   ├── 04_omnichannel_content_syndicator.json
│   └── 05_error_monitoring_and_healthcheck.json
├── templates/                       # Template kontrak, proposal & skema klien
│   ├── b2b_service_proposal_template.md
│   └── client_onboarding_checklist.md
├── scripts/                         # Skrip otomasi & deployment n8n
│   ├── n8n_client.py                # Python SDK wrapper untuk n8n REST API
│   ├── export_workflows.py          # Backup seluruh workflow dari n8n ke lokal
│   └── import_workflows.py          # Deploy workflow JSON dari lokal ke n8n instance
├── catalogs/
│   └── service_catalog_and_pricing.md # Katalog produk & daftar harga jasa
└── README.md
```

---

## 🚀 5 Solusi Unggulan (Core B2B Product Lines)

1. **WhatsApp AI Sales & Qualifier Bot** (`01_whatsapp_ai_lead_qualifier.json`)
   - Menjawab chat pelanggan 24/7, mengkualifikasi leads secara cerdas, dan mencatat data prospek otomatis ke Google Sheets / CRM.
2. **E-Commerce Automated Invoicing & Receipt Engine** (`02_ecommerce_invoice_pdf_generator.json`)
   - Menerima webhook pesanan toko online, men-generate PDF invoice profesional, mengarsipkan ke Google Drive, dan mengirimkan kwitansi instan ke WA/Email pelanggan.
3. **B2B Lead Scraper & Data Enricher** (`03_b2b_lead_scraper_enricher.json`)
   - Mengambil data calon klien potensial di kota target (Google Places), memvalidasi nomor telepon/email dengan AI, dan menyiapkan daftar kontak untuk tim sales.
4. **Omnichannel Headless Content Syndicator** (`04_omnichannel_content_syndicator.json`)
   - Mengambil 1 konten sumber dan otomatis mendistribusikannya ke seluruh media sosial brand klien dengan format yang disesuaikan per platform.
5. **Enterprise Error Monitoring & Telegram Sentinel** (`05_error_monitoring_and_healthcheck.json`)
   - Memantau kesehatan server & workflow 24/7. Mengirimkan alert darurat instan ke Telegram tim IT jika ada sistem yang mengalami error.

---

## 💼 Model Bisnis & Tangga Harga (Service Ladder)
* **Tier 1 — Quick Setup (Single Automation):** Rp 3.000.000 – Rp 5.000.000 (Setup 1x) + Rp 500.000/bln maintenance.
* **Tier 2 — Full Automation Suite (Sales + CRM + Invoicing):** Rp 8.000.000 – Rp 15.000.000 (Setup 1x) + Rp 1.500.000/bln maintenance.
* **Tier 3 — Custom Enterprise Engine:** Rp 20.000.000+ per implementasi.
