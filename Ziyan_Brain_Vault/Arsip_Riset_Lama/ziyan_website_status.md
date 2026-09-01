# Website ZIYAN — Status (2026-08-08 malam)

## URL Live (FINAL — migrate ke Vercel karena GitHub Pages CDN stale)
- **https://zyn-aicorp.vercel.app** ← INI YANG DIPAKAI (Vercel, tema UGCGen baru, no cache issue)
- ~~https://ziyancorp.github.io/~~ (GitHub Pages user site, CDN stale bandel, abandon)
- Repo source: github.com/ziyancorp/yangmulia96.github.io (sudah benar tapi CDN ga update)

## Root Cause Masalah Sebelumnya
- index.html refer ke /zyn-aicorp-site/assets/ (salah path) → React blank
- Username GitHub ganti (yangmulia96 → ziyancorp) → URL lama 404

## Fix Yang Dilakukan
1. Rebuild Vite dengan --base=/ (user site root)
2. Copy dist/* ke repo + push
3. Tambah .nojekyll (cegah Jekyll)
4. Disable + re-enable Pages (force rebuild)
5. Rewrite App.jsx → tema UGCGen AI (bukan investasi)
   - Hero, 3 Fitur (Video/Extractor/Image), Live Demo (Cloud Run link), Jasa Konten (3 paket)
6. Rebuild + push (hash CL0A7Jnx) + trigger Pages build

## Known Issue
- GitHub Pages CDN user site LAMBAT propagasi (~15-30 menit stale cache)
- Setelah tunggu, CDN auto-update ke hash terbaru (terbukti tadi)
- Bos cukup hard refresh setelah 15-30 menit

## Source
- Project: C:\Users\arija\zyn-aicorp-site (src/App.jsx = 519→rewrite UGCGen)
- Deploy: C:\Users\arija\yangmulia96.github.io (git push main)

## UGCGen App (Gemini)
- Cloud Run: https://ais-pre-4nmfr4c5j7bgnrmewyu6u-609615837790.asia-east1.run.app
- Image gen unlimited (session Google Bos)
- TIDAK bisa dijual (lock-in Google), hanya alat uji
