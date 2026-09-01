# Bot Ops Debugging — ZIYAN Archive Bot

Pitfalls & PowerShell commands untuk operasi bot Telegram→Drive/Sheets di Windows.
Penting: shell command line agent yang berisi string `ziyan_bot.bot` (grep/filter)
ikut ke-match jika pakai `LIKE '%ziyan_bot.bot%'` mentah — selalu filter `Name='python.exe'`.

## Hitung bot ASLI (bukan shell agent)
```powershell
# count real bot python processes
(Get-CimInstance Win32_Process -Filter "Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'").Count

# list dengan parent
Get-CimInstance Win32_Process -Filter "Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'" | Select-Object ProcessId,ParentProcessId | Format-Table

# kill SEMUA bot (aman — tidak sentuh hermes/9router)
Get-CimInstance Win32_Process -Filter "Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'" | ForEach-Object { taskkill /PID $_.ProcessId /F }
```

## Cari user ID pengirim (fix "Akses ditolak")
1. Patch `bot.py` `reject_if_unauthorized`:
```python
uid = update.effective_user.id if update.effective_user else "unknown"
logger.warning("REJECTED user_id=%s (allowed=%s)", uid, sorted(self.settings.allowed_user_ids))
```
2. Kill semua bot lama, start 1 instance bersih (`env -u PYTHONPATH ./venv/Scripts/python.exe -m ziyan_bot.bot`).
3. Bos kirim 1 pesan dari HP.
4. Baca log background process → `REJECTED user_id=7349146540` → itu user ID asli.
   (Bot ID = prefix token, mis. `8684088993` dari `8684088993:...` — BUKAN ini yang di-whitelist.)
5. Edit `.env`: `TELEGRAM_ALLOWED_USER_IDS=7349146540,8684088993` (user ID + bot ID).
6. Restart bot → pesan diterima.

## Verifikasi command line SEBELUM kill (JANGAN nebak PID)
```powershell
Get-CimInstance Win32_Process -Filter "ProcessId=4180" | Select-Object ProcessId,CommandLine
```
Jangan kill PID yang CommandLine mengandung `hermes_cli.main serve`, `gateway run`,
atau `9router` — itu Hermes gateway / 9router proxy, bukan bot. Salah kill = gateway
+ vision + model proxy mati (kejadian 2026-08-15: agent nebak PID 4180 = bot,
ternyata 9router → semua gateway mati).

## Restart 9router kalau ke-kill
```bash
9router --tray --no-browser
# verifikasi:
curl -s -m5 http://127.0.0.1:20128/health
```
