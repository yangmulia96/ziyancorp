# ZIYAN Archive Bot — Debug Recipe (terbukti 2026-08-16)

Bot arsip: `C:\Users\arija\ziyancorp\ziyan_archive_bot\` (module `ziyan_bot.bot`, token `@Zynarsipbot`).
Setup TERVERIFIKASI JALAN = 15 Agustus (2 produk masuk Sheet).

## A. Verifikasi "bot jalan" (jangan cuma poll PID)
```bash
cd /c/Users/arija/ziyancorp/ziyan_archive_bot
# 1. Process hidup?
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'\" | Select-Object ProcessId"
# 2. Token valid?
BT=$(grep '^TELEGRAM_BOT_TOKEN=' .env | cut -d= -f2- | tr -d '\r')
curl -s -m10 "https://api.telegram.org/bot$BT/getMe"
# 3. BOS di allowlist? (wajib ada 7349146540)
grep TELEGRAM_ALLOWED_USER_IDS .env
```

## B. Kenapa pesan Bos gak ke-arsip (root causes historis)
1. **REJECTED user_id=7349146540 (allowed=[...])** → ID Bos HILANG dari `.env`. Fix: tambah `7349146540` ke `TELEGRAM_ALLOWED_USER_IDS`, restart.
2. **Handler PM only** → `filters.PHOTO|VIDEO|DOCUMENT|CAPTION` = private chat. Channel butuh `filters.ChatType.CHANNEL & (...)`.
3. **Hardcode "15 detik"** di `save_pending` padahal `BATCH_WINDOW_SECONDS=120` → pakai `f"...{self.settings.batch_window_seconds} detik..."`.

## C. End-to-end test arsip (bukti nyata masuk Sheet)
```bash
cd /c/Users/arija/ziyancorp/ziyan_archive_bot
BT=$(grep '^TELEGRAM_BOT_TOKEN=' .env | cut -d= -f2- | tr -d '\r')
# Kirim 1 foto valid + caption link
curl -s -m15 "https://api.telegram.org/bot$BT/sendPhoto" -F "chat_id=7349146540" \
  -F "photo=@/path/ke/gambar_valid.png" \
  -F "caption=KAOS TEST https://s.shopee.co.id/1129piX7oq"
# TUNGGU 125 dtk (batch window 120) lalu baca Sheet:
python3 -c "from dotenv import load_dotenv; load_dotenv('.env'); from distributor import Settings,GoogleWorkspace; s=Settings.from_env(); gw=GoogleWorkspace(s.google_credentials_file,s.google_token_file,s.google_root_folder_id,s.google_spreadsheet_id); print(gw.sheets.spreadsheets().values().get(spreadsheetId=s.google_spreadsheet_id,range='PRODUCT_MASTER!A2:K').execute().get('values',[])[-1])"
```
- Pesan baru muncul di Sheet = SUKSES.
- `sendPhoto` error `IMAGE_PROCESS_FAILED` = file test PNG rusak (bukan bug bot). Pakai gambar valid.

## D. Revert-to-known-good 15 Agustus (langkah awal, bukan tujuan)
1. `on_media`: `if message.caption and session.mode=="new": session.draft = parse_caption(message.caption)`
2. `finalize_batch`: `if session.mode=="new" and not session.draft: await bot.send_message(... "kirim metadata..."); return`
3. Handler: PM only (`filters.PHOTO|VIDEO|DOCUMENT|CAPTION` + `filters.TEXT & ~COMMAND`).
4. Hapus scheduler + channel handler + `retry` field.
5. `TELEGRAM_ALLOWED_USER_IDS` pastikan `7349146540` ada.
6. **Setelah revert+restart: TES E2E (C) sebelum lapor "beres".**

## E. Kill+restart bot
```bash
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'\" | ForEach-Object { taskkill /PID \$_.ProcessId /F }"
# lalu jalankan background:
cd /c/Users/arija/ziyancorp/ziyan_archive_bot && FB_PAGE_TOKEN=$(bash /c/Users/arija/bin/token_vault.sh get fb_page_token 2>/dev/null | tr -d '\n') CHANNEL_CELINE="-1004373452633" GOOGLE_CREDENTIALS_FILE=client_secret.json HERMES_CUSTOM_9ROUTER_API_KEY="$HERMES_CUSTOM_9ROUTER_API_KEY" env -u PYTHONPATH ./venv/Scripts/python.exe -m ziyan_bot.bot
```

## F. NEW failure modes ditemukan 2026-08-16 (sesi "kau perbaiki sampai bisa")

Sesi ini bot TERBUKTI GAGAL arsip padahal process hidup + token valid. Akar berlapis:

### F1. `filters.Caption` (class) CRASH dispatcher → bot gak process update sama sekali
- Symptom: `getUpdates` 200 OK rutin, tapi GAK ADA log handler (`REJECT_CHECK`/`ON_MEDIA` hilang), `process_update` manual jalan tapi live `run_polling` gak dispatch.
- Root: `MessageHandler(filters.PHOTO | ... | filters.Caption, ...)` — `filters.Caption` di PTB 22.x adalah **class, bukan instance** → `MessageFilter.check_update() missing 1 required positional argument: 'update'` saat dispatcher cek handler → seluruh update di-drop.
- FIX: pakai `filters.CAPTION` (konstanta). Selalu `hasattr(filters,'CAPTION')` vs `hasattr(filters,'Caption')` sebelum pakai.

### F2. `archive.upload_file` butuh `Path`, dikasih `str` → crash saat arsip
- Symptom: test `archive_new_product` langsung gagal `AttributeError: 'str' object has no attribute 'name'` di `google_workspace.py:103`.
- Root: `archive.py` line ~93 panggil `self.google.upload_file(local_file.path, ...)` padahal `upload_file(path: Path, ...)` butuh Path object, tapi `LocalFile.path` disimpan sebagai string.
- FIX: wrap `Path(local_file.path)`.

### F3. Drive upload timeout di koneksi lambat → produk gak masuk Sheet
- Symptom: handler JALAN (Google API calls muncul di log) lalu `TimeoutError: The read operation timed out` → produk gak tersimpan.
- FIX: `MediaFileUpload(..., resumable=False)` + `timeout=300` di `.execute()`. (Resumable buka multiple HTTP requests, tiap pakai default shorter timeout.)

### F4. MULTIPLE ORPHAN BOT INSTANCES → `getUpdates` conflict → `[]`
- Symptom: `getUpdates` return `[]` terus padahal foto terkirim (`sendPhoto` ok). `check_updates.py` manual juga `0 update`.
- Root: tiap restart cuma kill 1 PID, tapi **orphan instances numpuk** (bash wrapper + python.exe x3). Mereka berebut `getUpdates` → Telegram beri `[]` ke semua. `Conflict: terminated by other getUpdates` muncul kalau 2 jalan bareng.
- FIX: sebelum start instance baru, **KILL SEMUA** process yg commandline mengandung `ziyan_bot.bot`:
```powershell
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*ziyan_bot.bot*' } | ForEach-Object { taskkill /PID $_.ProcessId /F }"
```
- Verifikasi sisa: `Select-Object ProcessId` HARUS KOSONG sebelum start.

### F5. TEST METHODOLOGY SALAH (penyebab sesi muter 2 jam)
- `bot{BT}/sendPhoto` via requests = **bot kirim KE Bos** (outgoing), BUKAN Bos kirim KE bot (incoming). Jadi bot gak receive → `[]`. Ini SALAH simulasi, bukan bot rusak.
- Benar simulasi incoming: **Buka @Zynarsipbot di HP Bos → kirim foto+caption**, lalu cek Sheet 120dtk kemudian. Atau `app.process_update(Update.de_json(fake_update, app.bot))` untuk isolasi handler (terbukti jalan, tapi gak test receiver polling).
- `getUpdates` manual via curl `return []` = bot (atau orphan) sudah consume, BUKAN bukti gak ada update.

## G. Deterministik debug order (pakai ini, jangan tebak)
1. Kill ALL orphan (`F4`) → verify 0 instance.
2. Cek `TELEGRAM_ALLOWED_USER_IDS` ada `7349146540` (B).
3. `python -c "import telegram; print(telegram.__version__)"` — kalau 22.6 pastikan handler pakai `filters.CAPTION` bukan `.Caption` (F1).
4. `process_update` manual dulu (isolasi handler). Jalan = handler ok.
5. Start 1 instance, **Bos kirim foto via HP**, tunggu 125dtk, baca Sheet (F5+E).
6. Kalau masih `[]` di `getUpdates` log → cek orphan lagi (F4) atau Drive timeout (F3).

## H. JANGAN SALAHKAN BOS / JANGAN CLAIM "JALAN" DARI PID
- `process.running` / `getMe 200` / `getUpdates 200` ≠ task sukses. Bukti = **baris baru di Sheet** (F5/E).
- Saat Bos lapor "gak masuk", cari bug di code/state DULU (allowlist, filter, upload, orphan) — jangan tuduh cara Bos kirim.
- Revert-to-known-good (15 Agustus) adalah LANGKAH AWAL, bukan tujuan. Bos mau E2E jalan.
