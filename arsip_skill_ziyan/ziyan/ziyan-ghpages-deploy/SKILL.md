---
name: ziyan-ghpages-deploy
description: "Fix Vite base path & deploy GitHub Pages tanpa blank page."
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
platforms: [windows]
---

# ZIYAN GitHub Pages Deploy (Vite/React)

Sesi 2026-08-08: landing page `ziyancorp` blank white di HP. Root cause = **`base` path salah di `vite.config.js`** → asset JS/CSS 404 → React gak load.

## SIMPTOM
- Browser buka URL → **halaman putih kosong** (cuma `<div id="root">`, gak ada konten).
- `curl` HTML balikin `<script src="/zyn-aicorp-site/assets/xxx.js">` tapi `curl .../assets/xxx.js` → **404**.
- Artinya: path asset salah vs lokasi deploy.

## ATURAN BASE PATH (kritis)
| Tipe repo | URL | `base` di vite.config.js |
|---|---|---|
| **Project site** (`<user>.github.io/<repo>`) | `yangmulia96.github.io/ziyancorp/` | `base: '/ziyancorp/'` |
| **User site** (`<user>.github.io`) | `ziyancorp.github.io/` | `base: '/'` |

- Default Vite = `base: '/'`. Kalau deploy ke project site tapi base `/` → asset jadi `/assets/...` (404, seharusnya `/ziyancorp/assets/...`).
- Salah satu penyebab umum: `base: '/zyn-aicorp-site/'` (nama project lama/salah) → selalu 404.

## VERIFIKASI SEBELUM KLAIM BERHASIL
```bash
# 1. Cek path asset di HTML live
curl -s https://<url>/ | grep -oE '(src|href)="[^"]*assets[^"]*"'
# 2. Cek asset reachable (harus 200, bukan 404)
curl -s -o /dev/null -w "%{http_code}\n" https://<url>/assets/<file>.js
# 3. Tunggu propagasi GitHub Pages 1-5 menit, lalu cek ulang
```
JANGAN claim "live" kalau asset masih 404.

## USER SITE (root domain)
Buat repo khusus bernama **`<user>.github.io`** (bukan `<user>`):
```bash
gh repo create ziyancorp.github.io --public
git clone https://github.com/ziyancorp/ziyancorp.github.io.git
# build dengan base '/' lalu copy dist/* ke repo ini, commit, push main
```
- GitHub auto-enable Pages untuk repo `*.github.io` (branch main).
- **Efek ganti username:** kalau `yangmulia96` → `ziyancorp`, URL `yangmulia96.github.io/ziyancorp` jadi **404**. Harus deploy ulang ke `ziyancorp.github.io` (user site) DAN update base jadi `/`.

## WORKFLOW DEPLOY (terbukti)
```bash
cd ziyancorp
# edit vite.config.js base sesuai tabel
rm -rf dist
npm run build
npx gh-pages -d dist -m "deploy: fix base"
# atau kalau user-site: cp -r dist/* ../ziyancorp.github.io/ && git push
```
- `npx gh-pages` butuh install sekali (`npm warn ... will be installed`).
- Deploy ke user-site repo: `git clone` repo `*.github.io`, `cp dist/*`, `git add -A && commit && push -u origin main`.

## PITFALL
- **GitHub Pages propagasi lambat** (1-5 mnt project site, **15-30 mnt user site**). Cek live bisa masih nunjukkan versi lama → `sleep 45` lalu re-check.
- Jangan ganti username GitHub kalau gak mau repot redeploy (URL kebalik).
- `npm run build` di Windows: pakai `node` (v24 ok), `npm` (v11 ok). `npm install` sekali kalau `node_modules` kosong.
- Commit credential KE GitHub = bocor. Site statis (HTML/JS/CSS) aman, tapi jangan `git add` file `.env` / token.

## HAZARD: JANGAN TOGGLE build_type KE "workflow" SEMBARANGAN (2026-08-08)
Sesi ini agent salah panggil `gh api -X PUT /repos/<x>/pages -f build_type=workflow` untuk user-site `ziyancorp.github.io` → **site MATI**: semua curl balik 404 + API bilang *"The repository does not have a GitHub Pages site"* (403). CDN tetap serve bundle lama (cache nyangkut).
- **ROOT CAUSE:** untuk user-site, `build_type=legacy` + source `gh-pages/` adalah default yang benar. Memaksa `workflow` lewat API malah menghapus/unregister site.
- **FIX yang JALAN:** re-create site lewat `POST /repos/<x>/pages` (bukan PUT) dengan source branch `gh-pages`, lalu push manual ke `gh-pages`. Tunggu 5-15 mnt flush.
  ```bash
  gh api -X POST /repos/<user>/<repo>/pages -f "source[branch]=gh-pages" -f "source[path]=/"
  ```
- Kalau sudah pakai GitHub Actions (`deploy-pages@v4` + `upload-pages-artifact`), biarkan workflow yang deploy — jangan juga push manual ke `gh-pages` (tabrakan).
- **AMAN:** ubah isi App.jsx / rebuild / push `gh-pages` manual = OK. Yang BAHAYA = ganti `build_type` lewat API.

## REKOMENDASI ALUR DEPLOY USER-SITE (terbukti paling stabil)
1. `npm run build` (base '/') → hasil di `dist/`
2. `git checkout gh-pages` → `rm -rf assets index.html .nojekyll` → `cp dist/index.html ./ && cp -r dist/assets ./assets` → `touch .nojekyll`
3. `git add -A && git commit -m deploy && git push -f origin gh-pages`
4. `git checkout main`
5. Tunggu 5-15 mnt, verifikasi isi bundle (`grep` teks produk, bukan cuma HTTP 200).

## PITFALL LAIN: /assets DI ROOT = 404
GitHub Pages legacy sering gak serve folder `assets/` di root. Solusi: ganti `assetsDir` di `vite.config.js` ke `'static'` (atau rename pas deploy ke `files/`). Tapi sebenarnya di sesi ini setelah fix `gh-pages` manual, `/assets/` JALAN — jadi 404 tadi murni karena site mati (build_type), bukan nama folder. Uji dulu sebelum rename.

**Kesimpulan (REVISI 2026-08-08 malam — terbukti):** Kalau raw GitHub benar tapi CDN user-site TETAP serve file yang SUDAH DIHAPUS (contoh nyata: `FcaNe1FH.js` padahal repo punya `CL0A7Jnx.js`) meski sudah disable/re-enable/rebuild/`.nojekyll`/tunggu 30+ mnt → **JANGAN teruskan di GitHub Pages**. CDN user-site bisa stuck >1 jam bahkan serve deleted file. **DEFINITIF FIX: MIGRASI KE VERCEL** (`vercel --prod --yes` dari folder project → `https://<nama>.vercel.app`, hash-bust otomatis, TIDAK ada stale). Biar Bos tetap bisa buka URL lama: timpa `index.html` repo GitHub jadi meta-refresh + JS redirect ke Vercel. Lihat P12/P13 di `ziyan-saas-demo-deploy`.

**ATURAN BOSS (dari "Kau beres kan itu sampai jadi... Aku gak mau tau"):** kalau URL yang SUDAH Bos pakai rusak (stale/404), **bereskan di server** — pasang redirect atau perbaiki asset di URL lama, JANGAN suruh Bos buka URL lain / hard refresh sebagai solusi. Hard refresh = instruksi terakhir kalau yakin cache klien (setelah verifikasi curl server-side benar).

## STALE CDN CACHE (DEBUG PATH — 2026-08-08)
Sesi ini: setelah rebuild + push, repo raw GitHub benar (`Dic31el3`), tapi **CDN masih serve hash LAMA (`FcaNe1FH`) yang SUDAH DIHAPUS di repo** + `links.html` 404. Artinya CDN stale, bukan path salah.

**Verifikasi beda raw vs CDN (wajib sebelum claim fix):**
```bash
# raw (authoritative, apa yang ada di repo)
curl -sL "https://raw.githubusercontent.com/<user>/<repo>/main/index.html" | grep -oE 'index-[A-Za-z0-9]+\.(js|css)'
# CDN live (bisa stale)
curl -s "https://<user>.github.io/?$(date +%s)" | grep -oE 'index-[A-Za-z0-9]+\.(js|css)'
# kalau raw != CDN → CDN stale, bukan push gagal
```

**Recipe yang DICOBA (urutan):**
1. Rebuild Vite dengan `base:'/'` + copy `dist/*` ke repo + `git push`. → CDN TETAP stale.
2. Tambah `.nojekyll` + commit + push + trigger rebuild via API. → CDN TETAP stale.
3. **Disable + re-enable Pages via API** (`DELETE /repositories/{id}/pages` lalu `POST` sama). Status balik `building`→`built`, tapi CDN TETAP serve file yang sudah dihapus.
4. Hasil akhir: CDN butuh **propagasi lambat user-site (15-30 mnt)** — API rebuild TIDAK memaksa bust cache untuk user site.

**Kesimpulan:** Kalau raw GitHub sudah benar tapi CDN stale, **JANGAN loop rebuild berkali-kali** (rate-limit token "Bad credentials"). Biarkan 15-30 mnt, suruh Bos hard-refresh. CDN user-site lebih lambat dari project-site.

**Trigger rebuild (kalau mau, hati-hati rate-limit):**
```bash
GHT=$(grep -iE "github|ghp_" ziyan_keys.env | head -1 | cut -d'=' -f2-)
REPO_ID=1327208948   # ziyancorp.github.io — cek via GET /repos/<user>/<repo>
curl -sL -X POST -H "Authorization: Bearer $GHT" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repositories/$REPO_ID/pages/builds"
```
- Cek status: `GET .../pages/builds/latest` → field `status` (`queued`/`building`/`built`).
- Ganti username: repo `yangmulia96.github.io` redirect ke `ziyancorp/yangmulia96.github.io` (normal). URL benar = `ziyancorp.github.io` (user site baru).

**Build invocation (hindari false-positive "long-lived server"):**
- JANGAN `npx vite build` di foreground (Hermes salah deteksi sebagai dev server → error).
- Pakai `./node_modules/.bin/vite build --base=/` di **background** (`background=true`), lalu `process wait`.
- Atau `npm run build` (script di package.json = `vite build`, aman foreground).

Detail lengkap: `references/stale_cache_debug.md`.

## KREDENSIAL GH
- `gh auth status` → Bos = `yangmulia96` (GitHub redirect otomatis ke `ziyancorp` setelah rename, normal).
- Push lewat credential manager Windows (gak perlu token manual kalau sudah login).

## REFERENCES
- `references/stale_cache_debug.md` — recipe diagnosis & fix CDN stale user-site (raw vs CDN, rebuild gagal memaksa bust, tunggu 15-30 mnt).
