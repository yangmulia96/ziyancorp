# Project Handoff: UGCGen AI (dari Gemini chat Bos)

Sumber: PDF `Tolong_uraikan_riwayat_percakapan_ini...pdf` (Bos forward dari Gemini share)
Diambil: 2026-08-08

## Konteks
UGCGen AI = SaaS AI Content Generator. Video UGC (Avatar+Voice) + Visual (Carousel/AI Influencer).
Monetisasi: Image Gen = GRATIS (loss leader), Video Gen = BAYAR (kredit).

## TAHAP 1: FRONTEND (SUDAH SELESAI - sudah Bos buat & saya deploy)
- Responsive Mobile-First (Hamburger + Sidebar)
- Dashboard & Billing (credit indicator, pricing, video library)
- Video Studio (Paid, 1 Credit): Wizard 4 step, rasio 9:16/16:9, Dynamic AI Captions, URL-to-Script Extractor
- Image & Carousel Studio (Free): 3 mode (Influencer/Carousel/Product), Aspect Ratio, Templates, AI Copywriter
- Luminous Dark Mode + Glassmorphism

## TAHAP 2: BACKEND (TUGAS AGENT = SAYA)
Semua masih mockup client-side. Migrasi ke production:

### 1. Framework & Auth
- Pindah ke Next.js App Router (SUDAH SAYA LAKUKAN - app/page.tsx)
- Supabase: tabel users (credits_balance, tier) + videos/images
- Supabase Auth (Google OAuth)

### 2. Payment (Stripe/Midtrans)
- Route handler checkout
- Webhook listener → update credits_balance saat settled

### 3. AI Engine (Server Actions)
- API wajib di server (sembunyikan key)
- Video: HeyGen + ElevenLabs (cek kredit >0, potong 1, tembak API)
- Image: Gemini 2.5 Flash / Flux / Midjourney API
- AI Copywriter: caption generator
- URL Extractor: Cheerio + LLM (Shopee/TikTok → script)

### 4. Polling/Webhook
- HeyGen 1-3 menit render
- Polling atau Supabase Realtime → status processing → completed (UI live)

## Pesan Strategis
"Fokus: sambungkan kabel (backend hookup). UI/UX sudah divalidasi. Mulai Supabase, amankan API key, bangun endpoint Next.js untuk potong kredit sebelum tembak API AI."

## Status Eksekusi Saya (sudah dilakukan hari ini)
- ✅ Next.js App Router setup (app/page.tsx dari kode Bos)
- ✅ Build success
- ✅ Deploy Vercel: https://ugcgen-ai-gamma.vercel.app (LIVE untuk uji coba kawan)
- ⏳ Supabase (belum)
- ⏳ Midtrans/Stripe (belum)
- ⏳ HeyGen/ElevenLabs (belum - mock)
- ⏳ Gemini key di server (belum - client kosong)

## STATUS DEMO LIVE (2026-08-08, malam)
- ✅ URL live: https://ugcgen-ai-gamma.vercel.app (Vercel, bisa dikasih ke kawan)
- ✅ Fix: Video Studio (form avatar/voice/script, mock), Avatar "P" klik→Settings, URL-to-Script Extractor (9Router Sonnet), dark force luminous
- ⚠️ BLOCKER: Semua Gemini image key Bos 429 quota (GEMINI_KEY lama, GOOGLE_KEY baru AIza..., GEMINI_KEYB2 AQ.Ab8...LFTg). Image gen pakai fallback placeholder (banner merah "Demo mode").
- ✅ Key baru sudah disimpan di ziyan_keys.env (GOOGLE_KEY + GEMINI_KEYB2) untuk pasang kalau quota reset.

## Next Action (sesuai pesan strategis)
1. Setup Supabase project + SQL schema
2. Supabase Auth Google OAuth
3. Midtrans sandbox endpoint
4. HeyGen API (butuh key)
5. Deploy ulang ke Vercel
6. Ganti Gemini key di page.tsx line 265 kalau quota image reset
