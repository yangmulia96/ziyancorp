# ZIYAN_ASET_INVENTORY.md (auto-log oleh Orchestrator)

## ASET 7: YouTube Clipper Bot (Telegram AI Wrapper — GRATIS)
Tanggal: 2026-08-09
Status: **PRODUCTION-READY (v2)** — @Ziyanclipperbot (online)

### Fitur (v2 - setelah upgrade):
- ✅ Download YouTube (yt-dlp)
- ✅ Transkrip + word-timestamp (faster-whisper base, lokal)
- ✅ AI pilih momen viral + caption + skor (9Router Sonnet 4.5)
- ✅ Virality score parsing (otomatis baca % dari Sonnet)
- ✅ Subtitle burn-in ke video (SRT + FFmpeg, style cyan)
- ✅ Potong 9:16 (FFmpeg scale+pad)
- ✅ Error handling + cleanup file
- ✅ Caption Telegram: "🔥 Potensi Viral: XX%"

### Pipeline:
User → Telegram @Ziyanclipperbot → bot.py
  → yt-dlp download
  → faster-whisper transkrip (word timestamps)
  → Sonnet 4.5 pilih clip + caption + skor
  → FFmpeg: subtitle burn-in + potong 9:16
  → Kirim balik ke Telegram (video + caption)

### Modal: Rp 0 (laptop + 9Router + whisper lokal)
### Monetisasi:
- Jual token: Rp 35rb/10 clip
- HPP: Rp 0 → margin 100%
- Payment: Midtrans QRIS (belum dipasang)

### File:
- C:\Users\arija\clip_test\bot.py (TELEGRAM BOT v2)
- C:\Users\arija\clip_test\test_v2.py (test script)
- Token: ziyan_keys.env (TELEGRAM_BOT_TOKEN)
- Repo bedah: opensource-clipping (58★), autoclip (52★), chopify (3★)

### Cara jalanin:
cd C:\Users\arija\clip_test
$env:TELEGRAM_BOT_TOKEN="8984029406:AAHDxG9NZbag9xIVuDKKrG16SQZtLpZaR8c"
.\.venv\Scripts\python.exe bot.py

### TODO (optional):
1. Midtrans webhook (topup token)
2. MediaPipe face-tracking (presisi reframing)
3. Deploy ke VPS (24/7 tanpa laptop)
