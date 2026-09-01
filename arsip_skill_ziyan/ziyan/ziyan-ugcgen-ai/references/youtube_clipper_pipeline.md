# YouTube Clipper Bot — Free Pipeline (Rp 0)

Terbukti jalan 2026-08-09. Replika gratis bot "Aden Studio AI" dari video Bos.

## Stack (semua gratis)
- `yt-dlp` — download YouTube (ada di `hermes-agent/venv/Scripts/`)
- `faster-whisper` — transkrip LOKAL (CPU, gratis, tanpa API)
- `9Router Sonnet 4.5` — pilih momen viral + caption (gratis via `kr/claude-sonnet-4.5`)
- `FFmpeg` — potong 9:16 + subtitle (ada di Winget)
- `python-telegram-bot` — interface Telegram

## Install (Windows, venv terisolasi)
```bash
cd C:\Users\arija\clip_test
uv venv .venv
uv pip install --python .venv/Scripts/python.exe faster-whisper
uv pip install --python .venv/Scripts/python.exe python-telegram-bot
# JANGAN --system (access denied C:\Python314)
```

## Pipeline code (inti)
```python
# 1. Download (GUNAKAN %(ext)s, jangan .mp4 mentah)
yt-dlp -f "bv[height<=480]+ba/best[height<=480]" -o "dl.%(ext)s" URL
vid = glob.glob("dl.*")[0]   # bisa .webm hasil merge

# 2. Transcribe (faster-whisper, base model)
WhisperModel('base', device='cpu', compute_type='int8')
# video 7 menit ≈ 1-2 menit di laptop 8GB

# 3. Sonnet pilih momen + caption (SSE parse)
curl -s http://localhost:20128/v1/chat/completions \
  -d '{"model":"kr/claude-sonnet-4.5","stream":true,...}'
# parse line: data: {json} -> delta.content (BUKAN JSON utuh)

# 4. FFmpeg potong 9:16
ffmpeg -i vid -t 45 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1" out.mp4
```

## Bot live
- `@Ziyanclipperbot` (token di `ziyan_keys.env`)
- Script: `C:\Users\arija\clip_test\bot.py`
- Jalankan: `.\.venv\Scripts\python.exe bot.py` (background)
- User kirim link YouTube → bot balas clip 9:16 + caption

## PITFALL
- `yt-dlp -o dl.mp4` → hasil `dl.mp4.webm` (merge) → `os.path.exists` gagal. PAKAI `%(ext)s` + glob.
- Whisper lambat CPU: model `base` cukup Indo, `tiny` kalau terlalu lambat.
- 9Router SSE: response stream `data: {...}` per baris, BUKAN JSON tunggal.
- Video Motion Transfer (Kling/Runway) = BERBAYAR → DIBUANG (Bos tolak).

## Monetisasi
- Jual token Rp35rb/10 clip, HPP Rp0 → margin 100%
- Midtrans untuk topup (belum dipasang)
- Open-source ref: NaufalRizqullah/opensource-clipping (58★), artbyjazi/autoclip (52★)
