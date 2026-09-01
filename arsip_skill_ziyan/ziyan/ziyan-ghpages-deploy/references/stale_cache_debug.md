# Stale CDN Cache Debug — GitHub Pages (user site)

Skenario 2026-08-08: website ZIYAN (`ziyancorp.github.io`, user site) blank setelah ganti
username GitHub (`yangmulia96` → `ziyancorp`). Setelah rebuild + push, CDN tetap serve
asset hash LAMA (`FcaNe1FH.js`) yang SUDAH DIHAPUS di repo, + `links.html` 404.

## Root cause terbukti
Bukan path salah, bukan push gagal — **CDN user-site stale, propagasi lambat (15-30 mnt)**.
API rebuild / disable+re-enable Pages TIDAK memaksa bust cache untuk user site.

## Step-by-step diagnosis (reproduce)
```
GHT=$(grep -iE "github|ghp_" ziyan_keys.env | head -1 | cut -d'=' -f2-)

# 1. Apa yang ADA di repo (authoritative)?
curl -sL -H "Authorization: Bearer $GHT" "https://raw.githubusercontent.com/ziyancorp/yangmulia96.github.io/main/index.html" \
  | grep -oE 'index-[A-Za-z0-9]+\.(js|css)'
# -> Dic31el3 (benar)

# 2. Apa yang CDN serve (bisa stale)?
curl -s "https://ziyancorp.github.io/?$(date +%s)" | grep -oE 'index-[A-Za-z0-9]+\.(js|css)'
# -> FcaNe1FH (lama, sudah dihapus) = STALE

# 3. Asset lama masih reachable di raw? (harus 404 kalau beneran dihapus)
curl -sL -o /dev/null -w "%{http_code}\n" "https://raw.githubusercontent.com/ziyancorp/yangmulia96.github.io/main/assets/index-FcaNe1FH.js"
# -> 404  (dibuktikan repo sudah benar, CDN yang bohong)
```

## Fix yang GAGAL memaksa bust (dicatat biar tidak diulang)
- Rebuild Vite base:'/' + copy dist + push -> CDN tetap stale
- Tambah .nojekyll + push + API rebuild -> CDN tetap stale
- DELETE + POST /pages (disable/re-enable) -> building->built, CDN tetap serve file terhapus
- Loop rebuild -> token "Bad credentials" (rate-limit) -> JANGAN diulang

## Fix yang BENERAN (tinggal tunggu)
1. Pastikan repo raw benar (hash cocok, links.html 200 di raw).
2. Biarkan 15-30 mnt propagasi user-site.
3. Suruh Bos hard-refresh (Brave: tahan reload -> Hard Reload, atau incognito).

## Repo ID lookup
GET /repos/<user>/<repo> -> field id (ziyancorp.github.io = 1327208948).
Ganti username: yangmulia96.github.io auto-redirect ke ziyancorp/yangmulia96.github.io.
URL user site BARU = https://ziyancorp.github.io/
