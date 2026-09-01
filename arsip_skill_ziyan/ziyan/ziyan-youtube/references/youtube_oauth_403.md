# YouTube OAuth — Error 403 `access_denied` (app belum diverifikasi)

Error ini BEDA dari 400 `redirect_uri_mismatch` (lihat `youtube_oauth.md`). Ini muncul SETELAH client Desktop benar, saat minta persetujuan user.

## ERROR TEXT
```
Error 403: access_denied
OAuth client / agent youtube has not completed the Google verification process.
The app is currently being tested, and can only be accessed by developer-approved testers.
```

## PENYEBAB PASTI
OAuth app = **User Type External** + **Publishing status = Testing**. Di mode Testing, Google memblokir SEMUA user kecuali yang ada di daftar **Test users**. Email pemakai (`mziyan266@gmail.com`) belum masuk daftar -> 403. BUKAN salah tipe client, BUKAN salah redirect.

## SOLUSI #1 — Tambah Test User (TANPA publish/verifikasi)
Ini jalan resmi untuk pakai app sendiri tanpa ribet verifikasi:
1. GCP Console -> project `lofty-layout-504106-n4` -> **APIs & Services -> OAuth consent screen**.
2. Pastikan **User Type = External**, biarkan **Publishing status = Testing** (JANGAN ubah ke Production).
3. Scroll ke **Test users** -> **+ ADD USERS** -> isi `mziyan266@gmail.com` -> **ADD** -> **SAVE**.
4. **Hapus `token.json`/cache OAuth lama**, lalu jalankan script -> re-auth. Layar "Google hasn't verified this app" NORMAL -> klik *Advanced -> Go to (app) (unsafe)*.

Setelah itu error 403 hilang. ✅

## MASA BERLAKU REFRESH TOKEN (Testing mode)
- Refresh token di mode **Testing expire setelah 7 hari** (dokumentasi resmi Google).
- Mitigasi: jalankan dengan `access_type=offline`, simpan `token.json`; kalau upload gagal "token expired", hapus `token.json` & re-auth (cukup 1x tiap ~7 hari).
- Refresh token **permanen** hanya kalau app **dipublikasi + diverifikasi** (butuh domain & privacy policy). Untuk pemakaian pribadi 1-2 user, Test Users + re-auth berkala sudah cukup - TIDAK perlu verifikasi.

## ALTERNATIF (ditolak untuk kasus ini)
- **User Type Internal?** TIDAK BISA untuk Gmail biasa. Internal hanya untuk organisasi **Google Workspace / Cloud Identity** (sumber resmi OAuth 2.0 Policies). `mziyan266@gmail.com` = Gmail pribadi -> pakai External + Test Users.
- **API Key untuk upload?** TIDAK BISA. Upload wajib **OAuth 2.0** (menulis ke channel user = data privat). API key hanya untuk **read-only data publik** (sumber: YouTube v3 auth guide).

## METODOLOGI VERIFIKASI (reusable - environment ini TIDAK punya tool `web_search`)
Pakai `curl` via terminal (git-bash) + Python untuk strip HTML dari docs resmi:
```bash
curl -sL "https://support.google.com/cloud/answer/XXXX" | python3 -c "
import sys,re
t=sys.stdin.read()
t=re.sub(r'<script.*?</script>','',t,flags=re.S)
t=re.sub(r'<style.*?</style>','',t,flags=re.S)
t=re.sub(r'<[^>]+>',' ',t); t=re.sub(r'\s+',' ',t)
print(t[:4000])"
```
Sumber resmi yang dikonfirmasi:
- Google Cloud "Manage OAuth App Branding" - external+production = verification wajib.
- OAuth App Verification Help Center - scope sensitive/restricted (youtube.upload) butuh verifikasi kalau dipublikasi.
- OAuth 2.0 Policies - Internal = "restricted to people in your Google Workspace or Cloud Identity organization".
- YouTube Data API v3 Auth guide - upload wajib OAuth 2.0; API key read-only.
- Catatan: Google search (`google.com/search`) & beberapa help article (JS-rendered) gagal di-scrape -> langsung target URL docs resmi.

## CHECKLIST 5 LANGKAH (untuk Bos)
1. Console -> APIs & Services -> OAuth consent screen (project `lofty-layout-504106-n4`).
2. User Type = External, Publishing status = Testing (jangan publish).
3. Test users -> + ADD USERS -> `mziyan266@gmail.com` -> ADD -> SAVE.
4. Hapus `token.json` lama -> jalankan script -> re-auth (klik Advanced -> Go to app).
5. Upload test - 403 harus hilang. Re-auth ulang tiap ~7 hari (token Testing expire).
