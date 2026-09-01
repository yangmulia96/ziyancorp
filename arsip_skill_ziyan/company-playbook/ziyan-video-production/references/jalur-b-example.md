# Contoh Script Jalur B (Gratis, Tanpa API Key)

Simpan sebagai `make_ziyan_video.py` lalu jalankan:
`uv run --with edge-tts --with imageio-ffmpeg --with pillow python make_ziyan_video.py`

```python
import asyncio, subprocess
from pathlib import Path
import edge_tts
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

OUT = Path(r"C:\Users\arija\ziyan_test_video.mp4")
AUDIO = Path(r"C:\Users\arija\ziyan_audio.mp3")
BG = Path(r"C:\Users\arija\ziyan_bg.png")

SCRIPT = (
    "ZIYAN, perusahaan kecerdasan buatan yang seluruhnya berjalan otomatis. "
    "Tanpa biaya operasional, tanpa tim manual. "
    "Tiga jalur pendapatan: jasa AI, perangkat lunak berlangganan, dan media konten. "
    "Bulan keenam, target lebih dari seratus lima puluh juta rupiah per bulan. "
    "Ini bukan masa depan. Ini sedang berjalan."
)

async def amain():
    c = edge_tts.Communicate(SCRIPT, voice="id-ID-ArdiNeural")
    await c.save(str(AUDIO))
asyncio.run(amain())

W, H = 1280, 720
img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    for x in range(W):
        r = int(10 + x / W * 30)
        g = int(10 + y / H * 20)
        b = int(40 + (x + y) / (W + H) * 90)
        px[x, y] = (r, g, b)
d = ImageDraw.Draw(img)
try:
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 110)
except Exception:
    f = ImageFont.load_default()
d.text((W // 2, H // 2 - 40), "ZIYAN", fill=(255, 255, 255), font=f, anchor="mm")
d.text((W // 2, H // 2 + 70), "Perusahaan AI 100% Otomatis", fill=(200, 220, 255),
       font=ImageFont.load_default(), anchor="mm")
img.save(BG)

ff = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [ff, "-y", "-loop", "1", "-i", str(BG), "-i", str(AUDIO),
       "-vf", "scale=1280:720",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
       "-shortest", "-t", "20", str(OUT)]
subprocess.run(cmd, check=True)
print("DONE", str(OUT), OUT.stat().st_size)
```

## Hasil teruji
- File: `ziyan_test_video.mp4` (269 KB), durasi tepat 20 dtk, 1280x720, H.264 + AAC.
- Tools: edge-tts + Pillow + FFmpeg (imageio-ffmpeg), semua gratis tanpa API key.
- Voice alternatif jika gagal network: `id-ID-GadisNeural`.

## Pitfall
- Di git-bash, path `C:\Users\...` di dalam Python bisa ter-escape (backslash jadi escape). Gunakan path relatif dari cwd `/c/Users/arija` atau raw string `r"..."`.
- Biar jadi animasi (bukan statis), perlu tahap ekstra: Manim/Python frame-by-frame atau edit transisi di CapCut (sudah terinstall di Brave Bos).
