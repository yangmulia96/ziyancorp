# Fix Error 403 OAuth YouTube — `access_denied` (app belum diverifikasi)

**Project:** `lofty-layout-504106-n4` (Google Cloud, OAuth Desktop client milik sendiri)
**Gejala:** Saat script Python upload YouTube, muncul:
`Error 403: access_denied — agent youtube has not completed the Google verification process. The app is currently being tested, and can only be accessed by developer-approved testers.`

---

## 1. Penyebab PASTI error ini

App OAuth kamu punya **User Type = External** dan **Publishing status = Testing** (belum dipublikasikan/diverifikasi). Di mode ini, Google **memblokir semua user kecuali yang sudah masuk daftar "Test users"**. Email yang menjalankan script (`mziyan266@gmail.com`) **belum masuk daftar test user**, makanya ditolak dengan 403.

Fakta resmi dari Google:
- App dengan *external* user type yang berstatus *production* **wajib** verifikasi (butuh domain, privacy policy, dll). *(sumber: Google Cloud branding help — "If your application is external and has the publishing status of production, your app will go through the verification process")*
- Scope YouTube upload (`youtube.upload`) termasuk kategori **sensitive/restricted**, sehingga jika dipublikasikan memang butuh verifikasi. *(sumber: OAuth App Verification Help Center)*
- **Tapi** selama masih di mode *Testing*, verifikasi TIDAK wajib — asal user yang pakai sudah jadi test user.

**Kesimpulan:** Kamu TIDAK perlu publish/verifikasi. Cukup daftarkan email pemakai sebagai Test User.

---

## 2. Solusi #1 (Test Users) — langkah berurutan

Ini cara paling simpel & resmi untuk pakai app sendiri tanpa verifikasi:

1. Buka **Google Cloud Console** → https://console.cloud.google.com/
2. Pastikan project aktif = `lofty-layout-504106-n4` (cek dropdown di atas).
3. Di kiri, buka **APIs & Services → OAuth consent screen**.
4. Di bagian **User Type**, pastikan = **External** (biarkan tetap Testing, JANGAN ubah ke Production).
5. Scroll ke bawah ke bagian **Test users** → klik **+ ADD USERS**.
6. Ketik email `mziyan266@gmail.com` → klik **ADD**.
7. Klik **SAVE** (kiri atas / bawah).
8. **Penting:** Jalankan ulang flow OAuth di script Python supaya minta persetujuan baru (hapus `token.json`/cache token lama dulu, lalu re-auth). User yang di-add sebagai test user akan melihat layar "Google hasn't verified this app" — itu **normal**, tinggal klik *Advanced → Go to (app) (unsafe)* untuk lanjut.

Setelah email masuk Test Users, error 403 hilang. ✅

---

## 3. Catatan masa berlaku REFRESH TOKEN di Testing mode

- Di mode **Testing**, **refresh token kedaluwarsa setelah 7 hari** (dokumentasi resmi Google). Setelah 7 hari, upload akan gagal karena token tidak bisa di-refresh otomatis.
- **Cara ampuh biar token awet:** setelah add test user, lakukan re-authorization **sekali lagi setiap kali mau upload rutin**, ATAU jalankan script dengan `access_type=offline` dan simpan `token.json` — lalu kalau error "Token expired", hapus `token.json` dan re-auth (cukup 1x tiap 7 hari).
- Kalau Bos mau refresh token **permanen (tidak expire 7 hari)**, satu-satunya jalan resmi adalah **publikasi + verifikasi app** (ribet, butuh domain & privacy policy). Untuk pemakaian pribadi, cukup re-auth tiap 7 hari — tidak perlu verifikasi.

---

## 4. Alternatif / klarifikasi lain

### A. Ganti User Type jadi "Internal"? — TIDAK BISA untuk Gmail biasa
- User Type **Internal** hanya bisa dipakai kalau project punya organisasi **Google Workspace / Cloud Identity** (bukan akun Gmail pribadi). *(sumber resmi OAuth 2.0 Policies: Internal = "restricted to people in your Google Workspace or Cloud Identity organization")*
- `mziyan266@gmail.com` adalah **Gmail biasa** → tidak memenuhi syarat Internal. **Jadi pakai External + Test Users saja.** Ini jalan yang benar untuk kasus kamu.

### B. Pakai API Key saja untuk upload? — TIDAK BISA
- Upload video wajib **OAuth 2.0** karena menulis ke channel user (data privat). *(sumber resmi YouTube auth: "an application can use OAuth 2.0 to obtain permission to upload videos to a user's YouTube channel")*
- **API key hanya untuk baca data publik (read-only)** — tidak bisa upload. Jadi API key bukan solusi untuk error 403 ini.

### C. Kalau Test Users masih kurang (mis. butuh >100 tester / butuh token permanen)
- Satu-satunya opsi resmi: **Publish + Verify app** (isi app domain, privacy policy, submit verification). Ini yang Bos hindari. Untuk 1–2 user pribadi, Test Users sudah cukup.

---

## 5. Checklist 5 langkah untuk Bos (di Console)

1. **Console → APIs & Services → OAuth consent screen** (project `lofty-layout-504106-n4`).
2. **User Type = External**, biarkan **Publishing status = Testing** (jangan publish/verify).
3. **Test users → + ADD USERS** → isi `mziyan266@gmail.com` → **ADD** → **SAVE**.
4. **Hapus `token.json`/cache OAuth lama**, lalu **jalankan script Python** untuk re-auth (klik *Advanced → Go to app (unsafe)* saat layar unverified muncul).
5. **Upload test** — error 403 harus hilang. *Ingat: ulangi re-auth tiap ~7 hari karena refresh token Testing mode expire.*

---

### Ringkasan
Error 403 itu muncul karena app OAuth external kamu masih di mode **Testing** dan email `mziyan266@gmail.com` belum masuk daftar **Test Users** — Google memang memblokir semua user di luar daftar itu tanpa verifikasi. Solusinya bukan publish/verifikasi (ribet), tapi cukup tambahkan email pemakai ke **OAuth consent screen → Test users** di Google Cloud Console, lalu re-auth script. Gmail biasa tidak bisa pakai User Type Internal (butuh Google Workspace), dan upload tidak bisa pakai API key (wajib OAuth). Di mode Testing refresh token kedaluwarsa tiap 7 hari, jadi cukup lakukan re-auth berkala — tidak perlu verifikasi sama sekali untuk pemakaian pribadi.

### Sumber resmi
- Google Cloud — Manage OAuth App Branding (external+production = verification)
- OAuth App Verification Help Center (sensitive/restricted scope butuh verifikasi)
- OAuth 2.0 Policies (Internal = Google Workspace/Cloud Identity only)
- YouTube Data API v3 — Authentication guide (upload wajib OAuth 2.0)
- Google Cloud OAuth consent screen (Testing: test users only, refresh token 7 hari)
