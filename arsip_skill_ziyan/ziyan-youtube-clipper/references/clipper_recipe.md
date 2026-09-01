# Clipper Recipe — Detail Command per Tahap

## 1. Download (yt-dlp)
```bash
cd C:\Users\arija\clip_test
yt-dlp --max-filesize 80M -f "bv[height<=480]+ba/best[height<=480]" \
  -o "dl.%(ext)s" "https://youtu.be/VIDEO_ID"
# File hasil: dl.webm (bukan dl.mp4!). Cari dengan glob("dl.*")
```

## 2. Transkrip (faster-whisper lokal)
```bash
uv venv .venv
uv pip install --python .venv/Scripts/python.exe faster-whisper
.venv/Scripts/python.exe -c "
import faster_whisper
m = faster_whisper.WhisperModel('base', device='cpu', compute_type='int8')
segs, _ = m.transcribe(r'C:\Users\arija\clip_test\dl.webm', beam_size=5, word_timestamps=True)
open(r'C:\Users\arija\clip_test\transcript.json','w',encoding='utf-8').write(
  json.dumps([{'start':s.start,'end':s.end,'text':s.text} for s in segs]))
"
# tiny model lebih cepat (~12 mnt untuk 12 mnt video), base ~20 mnt
```

## 3. Sonnet pilih momen + caption (9Router SSE)
```bash
KEY="$HERMES_CUSTOM_9ROUTER_API_KEY"
curl -s -m 40 http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" -H "Authorization: Bearer $KEY" \
  -d '{"model":"kr/claude-sonnet-4.5","messages":[{"role":"user","content":"Dari transcript ini pilih 1 momen viral max 45 detik + skor + caption TikTok"}],"temperature":0.7,"stream":true}'
# Parse line "data: {json}" → delta.content
```

## 4. FFmpeg potong 9:16 + subtitle burn-in (FIX Windows path)
```python
# Di Python, path subtitle HARUS diubah:
sub_fs = sub.replace("\\","/").replace(":","\\:")  # C:/Users/.../sub.srt → C\:/Users/.../sub.srt
vf = (f"scale=1080:1920:force_original_aspect_ratio=decrease,"
      f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,"
      f"subtitles='{sub_fs}':force_style='FontSize=28,PrimaryColour=&H00FFFF&,Outline=3,Alignment=2'")
# JANGAN pakai path Windows mentah → error "Unable to parse original_size"
```

## 5. Bot Telegram (timeout fix)
```python
from telegram.ext import ApplicationBuilder
app = ApplicationBuilder().token(TOKEN).read_timeout(120).connect_timeout(60).build()
# File >5MB sering TimedOut → kompres dulu: ffmpeg -b:v 1M -fs 45M
```

## 6. Verifikasi
```bash
ls -la bot_work/clip.mp4   # harus ada, size > 0
```
