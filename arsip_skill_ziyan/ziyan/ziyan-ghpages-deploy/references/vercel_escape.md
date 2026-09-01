# Vercel Escape Hatch — Fix GitHub Pages CDN Stale (User-Site)

**Kapan pakai:** CDN GitHub Pages user-site (`<user>.github.io`) serve hash JS/CSS LAMA yang SUDAH DIHAPUS di repo, meski raw GitHub benar. Rebuild/`.nojekyll`/disable-re-enable GAGAL bust cache (user-site lambat 15-30 mnt+, kadang stuck >1 jam).

**Fakta 2026-08-09:** `ziyancorp.github.io` serve `FcaNe1FH` (deleted), repo punya `CL0A7Jnx`. Setelah 2x rebuild + disable/re-enable + 30 mnt → TETAP stale. Migrasi Vercel = fix instan.

## Langkah

### 1. Deploy ke Vercel (butuh `vercel` CLI login)
```bash
cd zyn-aicorp-site
vercel --prod --yes --name zyn-aicorp
# Output: https://zyn-aicorp.vercel.app (auto-alias, cache-bust otomatis)
```
- Verifikasi: `curl -s https://zyn-aicorp.vercel.app/ | grep -oE 'index-[A-Za-z0-9]+\.js'` → harus hash TERBARU.
- Bos login: `arizalkempo-9767` (cek `vercel whoami`).

### 2. Redirect GitHub Pages lama → Vercel
Timpa `index.html` di repo GitHub Pages jadi:
```html
<!doctype html>
<html lang="id">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="refresh" content="0; url=https://zyn-aicorp.vercel.app/" />
    <link rel="canonical" href="https://zyn-aicorp.vercel.app/" />
    <title>ZYN AI Corp. — Mengalihkan...</title>
  </head>
  <body>
    <script>window.location.href = "https://zyn-aicorp.vercel.app/";</script>
    <p>Mengalihkan ke <a href="https://zyn-aicorp.vercel.app/">ZYN AI Corp</a>...</p>
  </body>
</html>
```
```bash
cd yangmulia96.github.io   # atau ziyancorp.github.io repo
git add -A && git commit -m "Redirect -> Vercel" && git push origin main
```
- Redirect HTML sederhana (tidak butuh asset JS) → langsung jalan meski CDN stale.
- Tunggu 1-2 mnt → buka `ziyancorp.github.io` otomatis ke Vercel.

### 3. Verifikasi akhir
```bash
curl -s "https://ziyancorp.github.io/" | grep -o "zyn-aicorp.vercel.app" && echo "REDIRECT OK"
curl -s "https://zyn-aicorp.vercel.app/" | grep -oE 'index-[A-Za-z0-9]+\.js'
```

## Pitfall
- JANGAN loop rebuild GitHub Pages setelah 15-30 mnt stale — langsung Vercel.
- Vercel free tier cukup untuk static site (Next.js/React/Vite).
- Domain custom (`ziyancorp.com`) = ~Rp150rb/tahun (opsional, belum perlu).
