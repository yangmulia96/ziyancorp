# GitHub Pages Deploy Pitfalls (ZIYAN site ziyancorp.github.io)

Dipelajari 2026-08-08 saat rewrite website jadi produk nyata. Site user-page: `ziyancorp.github.io` = repo `ziyancorp/ziyancorp` (redirect dari `yangmulia96/ziyancorp`).

## FAKTA PENTING
- User-site (`*.github.io`) baca dari **branch `gh-pages`** secara default (cek: `gh api repos/ziyancorp/ziyancorp/pages` -> `source.branch`). Push ke `main` SAJA tidak otomatis live.
- `gh pages build_type` bisa `legacy` (branch) atau `workflow` (GitHub Actions). **JANGAN toggle ke `workflow` kalau tidak yakin** — `gh api -X PUT /pages -f build_type=workflow` bisa MEMATIKAN site ("repository does not have a GitHub Pages site", 403).
- Setelah mati, POST ulang: `gh api -X POST /repos/ziyancorp/ziyancorp/pages -f "source[branch]=gh-pages" -f "source[path]=/"`. Kalau POST gagal (scope), Bos harus buka Settings -> Pages -> pilih branch di web.

## BUG: folder `/assets/` di root = 404
- Build Vite default `dist/assets/*` -> kalau di-copy ke root `gh-pages` sebagai `/assets/`, GitHub Pages **serve 404** (legacy Jekyll / reserved handling).
- FIX: rename output ke folder lain. Di `vite.config.js`: `assetsDir: 'files'` (bukan `assets`). Atau pas deploy: `cp -r dist/assets ./files && sed -i 's#/assets/#/files/#g' index.html`.
- Selalu verifikasi: `curl -s -o /dev/null -w "%{http_code}" https://ziyancorp.github.io/files/index-XXX.js` harus 200.

## CARA DEPLOY YANG JALAN (manual gh-pages)
```
cd ziyancorp
npm run build
git checkout -B gh-pages
rm -rf assets files index.html .nojekyll
cp dist/index.html ./
cp -r dist/files ./files      # bukan assets/
touch .nojekyll
git add -A && git commit -m "deploy" && git push -f origin gh-pages
git checkout main
```
Tunggu 1-3 menit propagasi. CDN user-site lambat flush (bisa 5-10 mnt).

## CARA DEPLOY YANG JALAN (GitHub Actions)
- `.github/workflows/deploy.yml`: build -> `actions/upload-pages-artifact@v3` (path: dist) -> `actions/deploy-pages@v4`.
- BUTUH `build_type: workflow` aktif. Kalau masih `legacy`, Actions sukses tapi site tetap serve snapshot lama.
- `gh workflow run deploy.yml` untuk trigger manual.

## VERIFIKASI KONTEN (bukan cuma HTTP 200)
- Root 200 tapi JS 404 = asset gak load -> site blank/broken.
- Cek isi bundle: `curl -s https://ziyancorp.github.io/ASSET.js | grep -oE "ProdukKita|DummyXYZ"` -> pastikan gak ada teks dummy (Nexus Cap, GlobalNet, dll).
- Raw GitHub bypass CDN: `curl -s https://raw.githubusercontent.com/ziyancorp/ziyancorp/gh-pages/index.html` (200 = file ada, berarti masalah CDN/cache).

## PITFALL LAIN
- Jangan `cp -r ZIYAN_TEMPLATES ./ZIYAN_TEMPLATES` dari dalam repo yang sudah ada folder itu -> nested folder. Hapus `ZIYAN_TEMPLATES/ZIYAN_TEMPLATES/` setelahnya.
- `npm ci` di Actions butuh `package-lock.json` (ada sejak npm install lokal). Log build: cari "vite v5.x building" + "built in".
- Theme toggle (light/dark) selalu ada di nav desktop — kalau Bos bilang "hilang", biasanya CDN belum flush, bukan hilang dari source.
