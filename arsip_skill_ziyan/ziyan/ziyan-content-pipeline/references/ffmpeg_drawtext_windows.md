# FFmpeg drawtext di Windows — Pitfalls (terbukti 2026-08-08)

Membuat video slide 9:16 dari foto + teks buat TikTok via `ffmpeg` di Windows. Berikut jebakan yang menghabiskan waktu:

## 1. FONT PATH butuh escape colon
- `fontfile='C:/Windows/Fonts/arial.ttf'` → ERROR "No option name near '/Windows/Fonts/arial.ttf'".
- FIX: escape colon jadi `C\:/Windows/Fonts/arial.ttf` (raw string di Python: `r"C\:/Windows/Fonts/arial.ttf"`).
- Di regular string Python `"C\\:/..."` salah (double-escape jadi `\\:`). Pakai `r"..."`.

## 2. SPASI di dalam text= memecah filter
- `text='Link di bio'` → ERROR "Invalid argument" (spasi bentrok dengan parser ffmpeg).
- FIX: ganti spasi dengan underscore `text='Link_di_bio'`, atau quote beda. Emoji (🔗) juga memecah → hindari di dalam filter drawtext.

## 3. Karakter `:` dan `+` di teks
- `text='2 WARNA: OLIVE + PASTEL'` → gagal parse (colon di tengah teks bentrok).
- FIX: pakai `text='OLIVE DAN PASTEL'` (hindari `:` dan `+` di dalam text=).

## 4. Tanpa fontfile = gagal
- `drawtext=text=...` tanpa `fontfile=` → error (fontconfig gak resolve di Windows build ini).
- Selalu sertakan `fontfile='C\:/Windows/Fonts/arial.ttf'`.

## RECIPE JALAN (1080x1920, 9 detik/foto, 2 foto, teks atas+bawah)
```python
FF = r"C:\Users\arija\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
FONT = r"C\:/Windows/Fonts/arial.ttf"
flt = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "drawtext=fontfile='" + FONT + "':text='JUDUL_ATAS':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=220:box=1:boxcolor=black@0.5:boxborderw=25,"
        "drawtext=fontfile='" + FONT + "':text='LINK_DI_BIO':fontcolor=yellow:fontsize=64:x=(w-text_w)/2:y=1720:box=1:boxcolor=black@0.5:boxborderw=25,"
        "fade=t=in:st=0:d=0.4[v]")
# loop 1 image -> -t 9 -r 30, lalu concat 2 part jadi 18 detik
```
- `-loop 1 -i img.jpg` wajib biar gambar jadi video.
- Concat: tulis `file 'p0.mp4'` + `file 'p1.mp4'` ke txt, lalu `ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4`.
- Cek hasil: `ffprobe -v error -show_entries format=duration:stream=width,height out.mp4`.

## Catatan
- ffmpeg full_build ada di WinGet Gyan path di atas. `which ffmpeg` di git-bash temukan path itu.
- Jangan pakai `execute_code` untuk loop FFmpeg berat — pakai script file + `terminal`.
