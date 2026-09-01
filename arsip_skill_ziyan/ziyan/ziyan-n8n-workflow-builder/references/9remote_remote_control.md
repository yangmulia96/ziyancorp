# 9Remote — Remote Control n8n UI dari Jauh

**Kapan pakai:** PITFALL #30 — browser tool agent GAGAL akses `localhost:5678`. Bos tidak pegang laptop → tidak bisa klik UI.

**Fakta (terbukti 2026-08-09):** 9Router punya fitur `9remote` (remote terminal/desktop dari mana saja). Bos sudah install di laptop.

## Cara jalanin (CLI, BUKAN app)
```bash
9remote start
```
TIDAK perlu bungkus background/audit — Bos bilang "tinggal ketik 9remote lalu enter".

**PENTING — 9Remote adalah CLI, bukan app di Start Menu.** JANGAN suruh Bos "Buka Start Menu → ketik 9Remote → klik app" (instruksi SALAH yang bikin Bos muter di sesi 08-09). Langsung `9remote start` di terminal.

Output:
- QR code (scan dari HP)
- App URL: https://9remote.cc/login
- One-Time Key: (6 huruf, expired 30 menit)
- Key permanen: sk-086...3b9b

Bos buka URL di HP → scan QR / masukkan OTK → kontrol penuh laptop → buka `localhost:5678` → klik node Telegram Trigger → pilih "ZiyanClipperBot" → Save → Activate.

## Gotcha
- `9remote start` exit diam → instance lama nyangkut (zombie port 2208 / pipe `9remote-pty`). Kill node nyangkut lalu start ulang.
- `9remote key` / `9remote otk` butuh server jalan dulu.
- Jangan loop `browser_navigate` localhost — sudah terbukti gagal (PITFALL #30). Langsung arahkan Bos ke 9remote.
- "Unlock PC remotely": ada di app GUI 9Remote (kalau Bos install versi GUI). Tapi kalau Bos bilang "gak ada app, install lewat terminal" → versi CLI-only. Cukup `9remote start` + remote HP, jangan paksa cari app.

## n8n "Set up owner" loop (related)
Kalau setelah remote jalan, UI n8n tetap minta "Set up owner" padahal user `mziyan266@gmail.com` ada di DB → root cause: `user.id=NULL` + `roleSlug='global:member'`. Fix di DB (PITFALL #33): `UPDATE user SET id='owner-ziyan', roleSlug='global:owner' WHERE email='mziyan266@gmail.com'` → restart n8n → UI langsung masuk dashboard.

## "Found credential with no ID" — root cause final
MUNCUL walau credential ada di DB `has_data=True` & node sudah `node.credentials={'telegramApi':'ziyan_clipperbot_cred'}`.
- Penyebab: n8n 2.33 hanya meregistrasi credential link lewat **UI session** (atau 9remote remote desktop). Set via DB/CLI/API `POST /api/v1/workflows` TIDAK persist (PITFALL #23/#27).
- Jalan satu-satunya tanpa pegang laptop: **9remote** → Bos klik UI. Atau edit DB + restart (PITFALL #19) — tapi Telegram Trigger butuh webhook registration, UI click lebih pasti.
- JANGAN usulkan delete user/settings DB untuk bypass auth (Bos deny, berbahaya — PITFALL #31).
