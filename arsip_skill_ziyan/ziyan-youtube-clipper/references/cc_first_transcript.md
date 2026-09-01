# CC-First Transcript Recipe (Cara Orang Bikin Clipper yang Benar)

**Pelajaran 2026-08-09**: Bos marah bot lambat ("12 menit cuma balas Memproses").
Root cause: whisper BASE di CPU = 12 menit/video. Cara BENAR (orang bikin):
**Coba YouTube CC dulu (instan, 0 detik), fallback whisper TINY kalau tidak ada CC.**

## Benchmark (laptop Bos: i5-8265U no-CUDA)
- whisper base, video 12 menit → ~12 menit (SALAH, timeout Telegram)
- whisper tiny, video 3 menit → 1m23s (3x lebih cepat per menit)
- **CC extraction (yt-dlp --write-auto-subs) → 0 detik (instan)**

## Step 1: Cek & extract CC (jalankan SEBELUM whisper)
```bash
yt-dlp --write-auto-subs --sub-langs id,en --skip-download \
  -o "bot_work/cc_%(id)s" "https://youtu.be/VIDEOID"
# Hasil: bot_work/cc_XXXX.id.vtt (atau .en.vtt)
```
- YouTube bisa 429 rate-limit sementara → tunggu 20-30 detik lalu retry
- Banyak video ID sudah punya CC → extract langsung tanpa download video

## Step 2: Parse VTT → plain text
```python
import re
def parse_vtt(path):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = re.sub(r"\d{2}:\d{2}:\d{2}\.\d+ -->.*", "", txt)
    lines = [l.strip() for l in txt.splitlines()
             if l.strip() and l.strip() != "WEBVTT"
             and not l.startswith("Kind:") and not l.startswith("Language:")]
    return " ".join(lines)
```

## Step 3: Fallback whisper TINY (hanya kalau CC gagal)
```python
# JANGAN base — terlalu lambat. Pakai tiny.
model = faster_whisper.WhisperModel('tiny', device='cpu', compute_type='int8')
segs, _ = model.transcribe(path, beam_size=5, word_timestamps=True)
```

## Integrasi di bot.py (proven 2026-08-09)
```python
def get_transcript_ytid(url):
    vid = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url).group(1)
    cc = os.path.join(WORK, f"cc_{vid}")
    subprocess.run(["yt-dlp","--write-auto-subs","--sub-langs","id,en",
                    "--skip-download","-o",cc,f"https://youtu.be/{vid}"],
                   capture_output=True, text=True)
    for lang in ["id","en"]:
        p = f"{cc}.{lang}.vtt"
        if os.path.exists(p):
            return parse_vtt(p), "cc"
    return None, ""
# Di process_video: txt,src = get_transcript_ytid(msg); if not txt: segs=transcribe(vid)
```

## Hasil akhir
Bot @Ziyanclipperbot dengan CC-first: video 12 menit → transkrip 0 detik (CC) →
Sonnet pilih momen → ffmpeg potong 9:16 → KIRIM ke Telegram (terbukti: "VIDEO SENT").
Tidak lagi timeout.
