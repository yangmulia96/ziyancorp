# 9router Watchdog Script (0-token)

## Tujuan
Pastikan proxy 9router (`http://127.0.0.1:20128`) SELALU HIDUP agar sub-agent bisa pakai
Gemini/OpenRouter (TTS/image). Jika mati → restart otomatis via `9router --tray --no-browser`.

## Aturan mutlak
- **JANGAN** pakai cronjob agent-based untuk watchdog → tiap run membakar token LLM (288x/hari).
- Gunakan `no_agent=true` + script ini di `~/.hermes/scripts/`. Nol LLM call = 0 token.

## Script (simpan sebagai `ziyan_watchdog_9router.sh`)
```bash
#!/bin/bash
# 9router Watchdog - script-only (NO token consumption)
if curl -s --max-time 5 http://127.0.0.1:20128/v1/models >/dev/null 2>&1; then
  exit 0   # sehat, silent
fi

# MATI: bunuh zombi lalu nyalakan ulang pakai tray mode (stabil)
taskkill /F /IM 9router.exe >/dev/null 2>&1
sleep 1
cmd.exe /c "start \"\" 9router --tray --no-browser" >/dev/null 2>&1
sleep 6

if curl -s --max-time 5 http://127.0.0.1:20128/v1/models >/dev/null 2>&1; then
  echo "🔧 9router mati, di-restart otomatis oleh watchdog."
else
  echo "⚠️ 9router MATI, restart gagal. Perlu cek manual (jalankan: 9router --tray --no-browser)."
fi
```

## Pasang sebagai cronjob
```
cronjob create --name "9router Watchdog ZIYAN" --schedule "*/5 * * * *" --no_agent --script ziyan_watchdog_9router.sh
```
Script HARUS di `~/.hermes/scripts/` (cronjob no_agent hanya terima nama file relatif ke sana).

## Verifikasi
Kill 9router manual lalu tunggu 5 menit → cek `netstat -ano | grep 20128` harus hidup lagi.
