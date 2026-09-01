# Distribution Agent — FINAL Spec (2026-08-16) + Token Reality

## FINAL DISTRIBUTION RULE (Bos revisi, OVERRIDES 8/77 menit & 6h-spacing)
- **Jadwal upload:** `08:57`, `12:34`, `16:08`, `20:13` (WIB, Asia/Jakarta) — 4x sehari, FIX.
- **Mekanisme:** 1 konten → **SEMUA platform sekaligus** (TG Channel, FB Page, IG @celineaurel99, YT Celine Aurel, Threads @celineaurel99) di jam tersebut. Bukan stagger.
- **Caption (FIX):**
  ```
  <Link Shopee>

  <Deskripsi natural: tema/ukuran/kegunaan — TANPA HARGA>

  <Link affiliate selain Shopee — kalau ada>
  #h1 #h2 #h3 #h4
  ```
  - JANGAN sebut harga. Link Shopee baris PALING ATAS. PERSIS 4 hashtag.
- **Sumber:** `ARSIP_MASTER` (tab PRODUCT_MASTER) atau `AFFILIATE.json` di `Celine Arsip/2026-08/PROD-*`.
- **Trigger:** cron di 4 jam (`57 8,12,16,20 * * *`) → ambil produk PENDING/terbaru → distribusikan.
- **Platform:** TG pasti jalan. FB/IG/YT/Threads auto-skip kalau token expired, lapor Bos.

## GOOGLE TOKEN EXPIRY — Manus's VERIFIED answer (2026-08-16)
Bos tanya "gak ada cara biar gak expired?" Manus jawab (SHARED_MEMORY.md, verified):
1. **OAuth Testing → Production:** hilangkan batas 7-hari refresh-token Testing, TAPI bukan abadi — tetap handle `invalid_grant`, minta re-auth kalau dicabut. Production != "auto-renew selamanya".
2. **Service Account (SA):** stabil untuk Drive/Sheets SAJA (server-to-server). Share folder My Drive ke email SA (role min). File tetap milik Bos. SA bukan berarti tak pernah expired (runtime token pendek, dibuat ulang otomatis; yang panjang = key).
3. **SA TIDAK bisa ganti OAuth YouTube** — YouTube Data API tidak support SA. YT tetap OAuth user.
4. **Verifikasi cron/PID:** jangan klaim "24/7 permanent" dari pesan agent. Acceptance (Windows):
   ```
   A. schtasks /Query /TN "<job>" /V /FO LIST  → jadwal 08:00, Last/Next Run
   B. log health-check → timestamp, exit code, Drive/Sheets auth, alert
   C. tasklist /FI "PID eq 8212" → PID milik bot
   D. restart test → bot hidup, 1 instance
   E. token test → Drive/Sheets OK, YT OAuth terpisah
   ```
- **Rekomendasi Manus:** migrasi Drive/Sheets ke SA (folder dibagikan) + pertahankan YT OAuth, bertahap.

## Cron yang sudah jalan
- `5df26507ece9` "ZiyanBot Health Check" — tiap hari 08:00 WIB, cek process + Google token + FB token, alert kalau expired (gak auto-fix).
- Distribusi agent BELUM dibuat saat ini — build pakai rule di atas saat Bos suruh.
