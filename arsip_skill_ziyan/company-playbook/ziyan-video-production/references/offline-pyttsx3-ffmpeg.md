# Offline video pipeline — pyttsx3 (SAPI5 lokal) + ffmpeg

Fallback saat 9router MATI (aplikasi desktop, tidak bisa di-restart via CLI) DAN/ATAU
edge-tts terblokir network (`speech.platform.bing.com:443` unreachable di host ini).
Pipeline 100% lokal, TANPA internet: `pyttsx3` (Windows SAPI5, sudah ada di disk) + `ffmpeg`.

## 1. PITFALL KRITIS — pyttsx3 gagal import di terminal hermes

**Symptom:** `import pyttsx3` crash dengan:
```
ModuleNotFoundError: No module named 'pywintypes'
```
driver `sapi5.py` melakukan `import pythoncom` → `import pywintypes`, gagal.

**Root cause (dua lapis):**
- Terminal hermes menyuntikkan venv `hermes-agent`
  (`C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Lib\site-packages`)
  ke `PYTHONPATH`. Venv itu memuat **stub `pythoncom.py` rusak** yang menutupi
  `pywin32` asli milik interpreter Python (Python 3.13 Windows Store).
- `pip install pyttsx3` menganggap `pywin32` "already satisfied" (melihat stub di
  venv hermes) → TIDAK memasang `pywin32` ke site-packages interpreter.
  Akibatnya `pyttsx3` ada tapi `pywin32` tidak ada untuk Python yang dipakai.

**FIX (wajib, dua bagian):**

(1) Pasang `pywin32` asli ke interpreter — jalankan DENGAN `PYTHONPATH=` dikosongkan
agar pip tidak melihat stub venv hermes:
```bat
PYTHONPATH= python3 -m pip install --force-reinstall --no-deps pywin32
```
(Jangan `python3 -m pip install pywin32` biasa — akan skip karena melihat stub.)

(2) Di dalam script Python, BERSIHKAN path venv asing SEBELUM `import pyttsx3`:
```python
import sys
_MARKERS = ("hermes-agent", r"hermes\hermes-agent")
sys.path[:] = [p for p in sys.path
               if not any(m.lower() in p.lower().replace("/", "\\") for m in _MARKERS)]
import pyttsx3  # aman setelah path asing dibuang
```
Ini membuat script aman di terminal hermes MAUPUN terminal biasa. Tanpa fix ini,
`render_short.py` (fallback pyttsx3) & skrip pyttsx3 apa pun akan crash di hermes.

## 2. pyttsx3 → MP3

`engine.save_to_file(text, path)` menulis **WAV** (bukan mp3 meski ekstensi .mp3).
Konversi ke mp3 asli:
```bat
ffmpeg -y -i out.wav -codec:a libmp3lame -b:a 128k out.mp3
```
- Sample rate SAPI5 default = 22050 Hz mono — cukup untuk voice-over.
- `engine.setProperty('rate', 160)` untuk kecepatan bicara.

## 3. Background video ffmpeg (tanpa asset eksternal)

Filter `gradients` (ffmpeg ≥ 5.0) untuk gradient animasi halus:
```bat
ffmpeg -y -f lavfi -i "gradients=size=540x960:rate=30:c0=0x0d1b3e:c1=0x1b998b:c2=0xfdca40:c3=0x0d1b3e:x0=0:y0=0:x1=540:y1=960:nb_colors=4:speed=0.02" ^
  -t DURASI -r 30 -vf scale=1080:1920:flags=bilinear ^
  -pix_fmt yuv420p -c:v libx264 -preset ultrafast -threads 0 bg.mp4
```
- **PERF:** jangan render `gradients` di 1080x1920 PENUH untuk klip panjang — CPU
  sangat berat & timeout (>60 dtk untuk klip 46 dtk di build gyan 8.1.1). Render
  SETENGAH resolusi (540x960) lalu `scale` ke 1080x1920. `pix_fmt yuv420p` wajib
  untuk kompatibilitas player.
- `DURASI` = durasi audio (didapat via ffprobe) + buffer kecil.

## 4. Mux audio + video → MP4 portrait (Shorts)

```bat
ffmpeg -y -i bg.mp4 -i audio.mp3 -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4
```

## 5. Verifikasi (ffprobe)

```bat
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,codec_name -of default=noprint_wrappers=1 out.mp4
```
Harus ada: stream video `h264` 1080x1920 + stream audio `aac`. Durasi ≈ durasi narasi.

## 6. Contoh script jadi

`C:\Users\arija\make_video_pipeline.py` — offline, tanpa internet. Proses semua `.txt`
di folder → 1 `.mp4` per naskah; flag `--one` untuk 1 naskah cepat; `--content` /
`--out` untuk override path. Sudah memuat guard import pyttsx3 (poin 1) & optimasi
gradients (poin 3).
