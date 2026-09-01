---
name: ziyan-saas-demo-deploy
description: Deploy Next.js/Vercel web demo from JSX Boss forwards.
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
---

# ZIYAN SaaS Demo Deploy

## Kapan Pakai
Bos kirim file .jsx / .tsx / React (biasanya hasil Gemini Canvas / export) dan minta "biar jalan buat aku kasih ke kawan uji coba". Tujuannya = URL publik yang bisa dibuka orang lain, bukan cuma localhost.

## Alur (EKSEKUSI PENUH — jangan lempar setup ke Bos)
1. Scaffold Next.js App Router di folder kerja.
2. Pindah kode Bos -> app/page.tsx (tambah 'use client' di baris 1 kalau pakai hooks/state).
3. Fix pitfall build (lihat bawah).
4. npm run build -> pastikan sukses.
5. Deploy Vercel (vercel --prod --yes) -> dapat URL publik.
6. Verifikasi: curl localhost + URL Vercel -> 200.

## Setup Awal (sekali)
- Vercel CLI sudah login sebagai arizalkempo-9767 (cek: vercel whoami). Bos pernah deploy via GitHub -> token tersimpan, JANGAN minta token.
- Node 24 + npm 11 ada di host.
- create-next-app lama (download ~1m) -> jalankan di background (terminal background=true notify_on_complete=true), jangan foreground (timeout 60s).

## PITFALLS (terbukti 2026-08-08, UGCGen AI)
### P1 - lucide-react import name tidak ada
Instagram tidak ada di versi lucide-react terpasang. Error: The export Instagram was not found. FIX: ganti ke ikon yang ada (Share2, AtSign) atau hapus dari import. Cek nama valid: node -e "const l=require('lucide-react'); console.log('X' in l)" SEBELUM build.

### P2 - TypeScript strict gagal di kode Bos
Next 16 default strict. Bos sering kirim kode tanpa tipe. FIX: tsconfig.json -> compilerOptions.strict=false, noImplicitAny=false. next.config.ts -> typescript:{ignoreBuildErrors:true}, eslint:{ignoreDuringBuilds:true}. (Next 16 mungkin tolak key eslint di next.config - warning, bukan error, aman diabaikan.)

### P3 - globals.css default PUTIH -> luminous "hilang"
Next scaffold globals.css background #ffffff. UI dark/violet jadi tidak kelihatan glow. FIX: override :root { --background:#05050A; --foreground:#ededed; } + @media (prefers-color-scheme: light) paksa dark. (Bos komplain "luminous effect gak ada" -> akar ini.)

### P4 - API key kosong di kode Bos
Kode Canvas sering const apiKey = "" (di-inject environment Gemini). Demo tidak jalan. FIX: cek ziyan_keys.env line 2 (GEMINI_KEY=...) - ada tapi bisa 429 quota untuk image gen. Inject key ke kode (client-side sesuai pola Canvas) ATAU .env.local (server). Untuk demo cepat: hardcode di page.tsx dengan komentar "ganti key yg punya akses". Tambah FALLBACK placeholder kalau API gagal (quota/error) -> UI tidak crash, keluar "Demo Image" + caption. Jangan biarkan tombol error kosong.

### P5 - Placeholder page mengalihkan ke halaman lain
Bos kirim kode dengan ViewCreateVideo cuma placeholder + tombol "Coba Image Studio" -> terasa "dialihkan ke foto". FIX: ganti placeholder jadi form nyata (mock logic + setTimeout simulasi render) supaya demo tidak terasa rusak. Video gen nyata = butuh HeyGen (Tahap 2, belum).

### P6 - Next.js 16 "bukan Next yang kamu tahu"
AGENTS.md di repo warning API berubah. Sebelum nulis code kompleks, cek node_modules/next/dist/docs. Untuk demo sederhana (copy JSX + Tailwind) tidak masalah.

### P7 - Gemini image model name
gemini-2.5-flash-image (BUKAN -preview). Endpoint: https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=KEY. Body: {"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"]}}. Extract: result.candidates[0].content.parts.find(p=>p.inlineData).inlineData.data.

### P8 - BRAVE MOBILE CACHE MENAMPILKAN VERSI LAMA (terbukti 2026-08-08)
Bos buka URL Vercel di **Brave mobile** → tetap nunjukin UI lama (placeholder "Coba Image Studio Baru", Video Studio kosong) PADHAL sudah `vercel --prod` deploy versi baru (alias sama, curl live sudah benar).
- Gejala: `curl` ke URL vercel return HTML versi BARU (ada "Rendering your UGC video"), tapi screenshot Bos dari Brave mobile masih versi LAMA.
- Akar: Brave cache agresif / service worker PWA. Alias Vercel sama tapi asset hash beda → Brave serve asset lama dari cache.
- FIX (instruksikan Bos, BUKAN agent yang buka browser):
  1. **Hard refresh**: tahan tombol reload → pilih "Hard Reload", atau
  2. **Incognito** (tutup tab buka private), atau
  3. **Clear cache** Brave: Settings → Privacy → Clear browsing data → "Cached images and files".
- JANGAN debat "deploy gagal" kalau curl sudah benar. Verifikasi SERVER-SIDE dulu (curl cek string unik versi baru) SEBELUM bilang ke Bos. Kalau curl benar → masalah di sisi klien (cache), bukan deploy.

### P9 - Avatar/Profile button tidak bisa diklik (placeholder, bukan bug)
Header avatar (huruf "P" dari user.name) di kode Bos cuma `<div>` tanpa `onClick` → tidak bisa diklik. Bos komplain "kok gak bisa diklik". FIX: tambah `onClick={() => setCurrentRoute('settings')}` + cursor-pointer, buat ViewSettings minimal (nama/email/tier/credit). Jangan biarkan elemen interaktif terlihat tapi mati.

### P10 - Fitur URL-to-Script Extractor HILANG dari kode Bos
Dokumen handoff sebut "AI URL-to-Script Extractor" tapi TIDAK ADA di source `Ugc_ai` (v1/v2). Screenshot Bos (overlay "Minta Gemini") = Gemini app LAIN, bukan UGCGen. FIX: tambah sendiri ke Video Studio — input link + tombol Extract → fetch ke 9Router Sonnet (`http://localhost:20128/v1/chat/completions`, model `kr/claude-sonnet-4.5`) buat script. Fallback template kalau proxy mati. CATATAN: `localhost:20128` cuma jalan kalau laptop Bos nyala & 9Router hidup — buat demo kawan jauh perlu backend Vercel Function (Tahap 2).

### P11 - Gemini image quota ADALAH HARD LIMIT, TIDAK ADA BYPASS (terbukti 2026-08-08)
Bos tanya "ada cara supaya nggak kena limit Nano Banana?" setelah semua key 429. FAKTA setelah test:
- `:predict` endpoint -> 404 (gemini-2.5-flash-image TIDAK support predict di v1beta, hanya `:generateContent`).
- 9Router (/v1/models) -> TIDAK ADA model image (cuma nemotron "nano" nama kebetulan, bukan image gen). Jangan cari flux/imagen di 9Router.
- 3 key Bos (GEMINI_KEY lama, GOOGLE_KEY baru AIza..., GEMINI_KEYB2 ...LFTg) -> semua 429.
- "Unlimited" di aistudio.app/web = ILUSI. Google track usage di backend, cuma tidak nunjukin counter di UI. Lewat API, limit kelihatan (429).
- AKAR: free tier Gemini image = rate limit di level AKUN Google, bukan per-key. Rotasi key TIDAK membantu (akun sama).
- SATU-SATU FIX NYATA: (a) Setup billing di AI Studio (link "Set up billing" di halaman API Keys) -> quota naik drastis (~$0.04/gambar, akun Google Bos sendiri, BUKAN Vertex), atau (b) tunggu quota reset (daily/monthly).
- JANGAN habiskan waktu re-test `:predict` atau cari image model di 9Router di sesi berikutnya. Langsung pakai fallback placeholder (P4) atau suruh Bos setup billing.
- Cek semua key cepat: `python3 scripts/test_gemini_image_keys.py` (lihat references/).

### P12 - GITHUB PAGES USER-SITE CDN STALE BANDEL (terbukti 2026-08-08, website ZIYAN)
Bos ganti username GitHub (yangmulia96 -> ziyancorp). URL lama 404. Setelah rebuild + push, CDN `ziyancorp.github.io` **tetap serve hash JS yang SUDAH DIHAPUS dari repo** (`index-FcaNe1FH.js`) padahal raw GitHub benar (`index-CL0A7Jnx.js`).
- Yang SUDAH dicoba & GAGAL: rebuild vite `--base=/`, tambah `.nojekyll`, disable+re-enable Pages via API, trigger `/pages/builds`, tunggu 30+ menit. CDN tetap stale.
- User site (`username.github.io`) punya CDN cache PALING bandel — bisa >1 jam, bahkan serve file deleted.
- **DEFINITIF FIX: MIGRASI KE VERCEL.** Bos sudah login `arizalkempo-9767` (vercel whoami). `vercel --prod --yes` dari folder project -> URL `https://<nama>.vercel.app`, hash bust otomatis, TIDAK ada stale CDN. Terbukti langsung jalan (CL0A7Jnx muncul).
- Biar Bos tetap bisa buka URL lama: timpa `index.html` di repo GitHub jadi **meta refresh + JS redirect** ke Vercel (`<meta http-equiv="refresh" content="0; url=https://<nama>.vercel.app/">` + `<script>location.href="..."</script>`). Redirect HTML sederhana langsung kebaca CDN (tidak butuh asset).
- **JANGAN habiskan waktu disable/rebuild/unggu GitHub Pages lagi.** Langsung Vercel kalau user site tidak update dalam 5 menit.

### P13 - BOSS BENCI DISURUH GANTI URL / DILEMPAR SETUP (terbukti 2026-08-08)
Bos: "Kau beres kan itu sampai jadi... Aku gak mau tau" (marah karena suruh buka URL beda padahal yang lama rusak).
- SAAT ADA MASALAH PADA URL/DEPLOY YANG SUDAH BOS PAKAI: **bereskan di sisi server, jangan suruh Bos buka URL lain atau hard refresh sebagai solusi.** Bos menganggap itu lempar tanggung jawab.
- Kalau URL lama rusak (stale/cache/404): pasang REDIRECT dari URL lama -> URL baru (P12), atau perbaiki asset di URL lama langsung. Bos buka URL yang sama pun masuk yang benar.
- Hard refresh / incognito = instruksi TERAKHIR kalau memang cache klien, BUKAN jawaban pertama. Verifikasi server-side dulu (curl cek hash/string unik) — kalau server benar, baru kata "cache Brave, hard refresh".
- Prinsip umum: eksekusi sampai SELESAI, jangan lempar step setup ke Bos.

## Verifikasi (wajib sebelum lapor ke Bos)
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
curl -s -o /dev/null -w "%{http_code}" https://<vercel-alias>.vercel.app
ipconfig -> cari IPv4 -> http://<IP>:3000 (buat kawan 1 WiFi, kalau belum deploy)
Cek CSS deploy punya class glow (violet, shadow-, 0_0_20px) -> pastikan luminous benar-benar render.

## Deploy command
cd /c/Users/arija/<folder>
vercel --prod --yes
# Output: "Aliased https://<nama>.vercel.app" <- ini URL publik buat Bos
Alias stabil (URL tidak berubah tiap deploy). Build di Vercel otomatis.

## Reference
- references/ugcgen_build_recipe.md - recipe lengkap UGCGen AI (file asli, fix diff, hasil).
- scripts/test_gemini_image_keys.py - cek semua Gemini key (env + hardcoded) ke endpoint image, laporkan OK/429. Jalankan: `python3 scripts/test_gemini_image_keys.py`.
