# UGCGen AI — Asset Pointers (jangan duplikasi, baca file asli)

Semua file ada di `C:\Users\arija\`:
- `ziyan_prompt_ugcgen_ai.md` — full prompt build (Next.js + Supabase + HeyGen + ElevenLabs + Midtrans/Stripe)
- `ziyan_gemini_ugc_explain.md` — definisi UGC dari Gemini Pro share (UGC = human, bukan AI; hybrid = AI UGC-style)
- `ziyan_riset_ugc.md` — 10 permintaan pasar UGC + harga (Rp150k-1jt)
- `ziyan_bedah_celineaurel.md` — profil creator mikro (662 followers, bukan kompetitor, calon klien)
- `ziyan_bedah_konten_celineaurel.md` — bedah 498 video (64% OOTD, engagement 5.1%)
- `ziyan_bedah_creativestudios.md` — kompetitor lokal (Next.js, Rp249-549k, generic, no UGC/avatar)
- `ziyan_kode_ugcgen_analyzed.md` — analisis kode frontend Bos (React luminous, Nano Banana image, mock video)
- `ziyan_ugcgen_roadmap.md` — 3 fase production + data flow
- `ziyan_ugcgen_update.md` — diff versi 1 vs 2 frontend (via Sonnet 4.5)
- LIVE APP: dev `http://localhost:3000` (folder `ugcgen-ai`), prod `https://ugcgen-ai-gamma.vercel.app` (Vercel arizalkempo-9767). Recipe: `references/deploy_build.md`

## Protokol Baca Dokumen Bos
- PDF: `pdftotext` ada di `C:\mingw64\bin\` (Git bash). Perintah: `pdftotext file.pdf out.txt`
- DOC/JS: langsung `read_file` (text ASCII)
- JANGAN pakai execute_code untuk baca file (diblokir policy)

## Model untuk Build
- NOVA (Sonnet 4.5) = scaffold Next.js + pindah kode
- Sonnet 4.5 = riset/bedah (stabil di 9Router)
- JANGAN janjikan Gemini Pro lewat 9Router (gagal quota) — pakai app Antigravity langsung kalau perlu Pro
