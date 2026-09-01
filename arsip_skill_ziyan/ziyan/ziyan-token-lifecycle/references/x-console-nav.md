# X Developer Console — Navigasi Praktis (Berdasar sesi 2026-08-09)

## Struktur Halaman
URL: `console.x.com/accounts/<ID>`

Tab di detail app:
1. **Keys & Tokens** (default) — lihat/generate token
2. **Subscriptions**
3. **Webhooks**
4. **Streaming rules**
5. **Connections**
6. **Settings** (icon gear) — TEMPAT TOMBOL DELETE

## Cara Hapus App (Bos pernah marah arahan salah)
1. Sidebar kiri → **Apps** (highlight)
2. Klik nama app → masuk detail
3. Klik tab **Settings** (gear icon, sebelah Keys & Tokens)
4. **Scroll ke paling bawah** → tombol merah **"Delete App"**
5. Ketik nama app persis (case-sensitive) → konfirmasi

TOMBOL DELETE TIDAK ADA DI:
- Tab Keys & Tokens
- Sub-page "Authentication settings" (settings app/permission)
- Apps list (hanya menampilkan row, gak ada delete langsung)

## Project Access (Penyebab API 403)
- Card "Project Access" status **Not connected** (kuning) → API v2 = 403 client-not-enrolled
- Klik **Manage** → pilih **Default project** → Connect → status hijau "Connected"
- Setelah connect, API v2 (post tweet) jalan

## Regenerate Token (Penyebab API 401)
- Tab Keys & Tokens → tiap section ada tombol **Revoke** + **Regenerate**
- Bearer Token, OAuth1a (Consumer/Access), OAuth2.0 (Client ID/Secret)
- Kalau ganti akun (username di cred beda), regenerate semua untuk akun baru

## Catatan
- App `shopeeaffiliatee` = produksi (jangan hapus)
- App numerik `2082093644111073280AgenticsID` = bisa dihapus kalau Bos yakin
- Akses token mencantumkan "@username Read and write and Direct message"
