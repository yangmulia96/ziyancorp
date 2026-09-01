# Lokasi Tombol Terverifikasi di Console Web (jangan nebak!)

## X (Twitter) Developer Console
- **Delete App**: sidebar → Apps → klik app → tab **Settings** (icon gear, BUKAN "Authentication settings") → scroll bawah → tombol merah "Delete App". Ketik nama app → konfirmasi.
- **Connect ke Project** (fix API 403): dari halaman detail app → card "Project Access" kuning → klik **Manage** → pilih Default project → Connect.
- **Regenerate Token**: tab Keys & Tokens → tiap section ada tombol "Regenerate" / "Revoke".
- App `shopeeaffiliatee` = produksi (jangan hapus). App numerik `2082093644111073...` = sampah.

## Lynk.id
- **Add block**: tombol "+ Add new block" di bawah halaman.
- **Customize URL**: tombol "Customize URL" (ikon crown) di box My Lynkid.

## Catatan Sesi 2026-08-09
- Bos benci arahan UI yang muter-muter. Selalu riset (9Router chat) sebelum jawab "tombol X di mana".
- 9Router chat jalan: `curl -X POST 127.0.0.1:20128/v1/chat/completions -H "Authorization: Bearer $KEY" -d '{"model":"kr/claude-sonnet-4.5","messages":[...]}'` — parse stream per baris `data: `.
