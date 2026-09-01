# Production Roadmap: UGCGen AI

Sumber: Production_Roadmap.pdf (dari Bos)
Diambil: 2026-08-08

## Status Awal
Frontend 80% selesai (kode Ugc_ai.jsx yang Bos kirim). Tinggal jadi production Next.js + Supabase.

## Fase 1: Setup Infrastruktur & Database
1. Pindah kode ke Next.js App Router (app/page.tsx atau app/dashboard/page.tsx)
2. Supabase Auth: ganti hardcoded user pakai @supabase/auth-helpers-nextjs + Google OAuth
3. Migrasi DB: jalankan SQL (users + videos table) di Supabase

## Fase 2: Integrasi Pembayaran (Midtrans/Stripe)
- Credit system = urat nadi monetisasi
1. Endpoint: app/api/checkout/route.ts
2. Midtrans Snap: klik "Beli Paket" → snapToken → popup pembayaran
3. Webhook: app/api/webhook/midtrans → jika settlement, update credits_balance

## Fase 3: Integrasi Engine AI Video (HeyGen/D-ID)
Ganti mock setTimeout dengan API asli:
1. HEYGEN_API_KEY di .env (jangan di frontend)
2. handleGenerate() → fetch('/api/generate')
3. Server logic (app/api/generate/route.ts):
   - Validasi: credits_balance > 0
   - Kurangi 1 kredit
   - Tembak HeyGen API (script + avatar + voice)
   - Simpan status processing
4. Polling/Webhook: HeyGen 1-3 menit render → Supabase Realtime update UI

## Data Flow (Video Gen)
Frontend → Next.js Backend (cek saldo, potong kredit) → HeyGen API (render 3 menit) → Webhook → DB update completed + MP4 URL → UI live update

## Yang Perlu Ditambah (dari kode Bos)
- ❌ Supabase setup (auth + SQL)
- ❌ Midtrans endpoint + webhook
- ❌ HeyGen API integration (ganti Nano Banana image → video)
- ❌ .env management
- ❌ Supabase Realtime

## Action Plan ZIYAN
1. NOVA (Sonnet) setup Next.js project + pindah kode
2. Buat SQL schema (users, videos)
3. Integrasi Supabase Auth (Google OAuth)
4. Midtrans sandbox (atau Stripe test)
5. HeyGen API (butuh key — Bos punya?)
6. Deploy Vercel + Supabase

## Catatan
- Kode Bos pakai Nano Banana (image), roadmap minta HeyGen (video)
- Perlu pivot: image sudah jalan, video butuh HeyGen key
- Midtrans cocok untuk Indonesia (Stripe untuk internasional)
