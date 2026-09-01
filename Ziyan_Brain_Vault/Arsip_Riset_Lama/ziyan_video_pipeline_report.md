# Laporan Pipeline Video ZIYAN (Offline — Tanpa 9router / Tanpa NotebookLM)

**Tanggal:** 2 Agustus 2026
**Status:** ✅ BERHASIL — 1 file `.mp4` valid dihasilkan dan diverifikasi dengan `ffprobe`.
**Mode:** Offline penuh, tidak butuh internet/9router/NotebookLM.

---

## 1. Latar Belakang & Masalah

- 9router MATI (tidak bisa di-restart via terminal — itu aplikasi desktop), sehingga tidak ada model TTS/9router.
- NotebookLM butuh login manual (Bos), sehingga tidak dapat diakses secara otomatis.
- **Fallback lokal:** TTS pakai `pyttsx3` (Windows SAPI5, sudah ada di disk) + `ffmpeg` untuk merender video dari naskah.

## 2. Yang Dilakukan

1. **Cek naskah** di `C:\Users\arija\ziyan_content_day1\`.
   - Folder sudah berisi 5 naskah `.txt` (dibuat sub-agent lain): `long_1.txt`, `shorts_1.txt`, `shorts_2.txt`, `shorts_3.txt`, dan dummy `ai_is_changing_business.txt`.
   - Karena instruksi meminta contoh dummy bila belum ada, dibuat `ai_is_changing_business.txt` (narasi "AI is changing business") agar pipeline testable.
2. **Buat script** `C:\Users\arija\make_video_pipeline.py` yang melakukan:
   - (a) baca `.txt` narasi,
   - (b) TTS via `pyttsx3` → `.wav` → `ffmpeg` (libmp3lame) → `.mp3`,
   - (c) buat background video animasi via `ffmpeg` lavfi `gradients` (tanpa asset eksternal),
   - (d) gabung audio + video → `.mp4` portrait **1080×1920** (Shorts/Reels/TikTok), 30 fps.
3. **Test jalankan** pada 1 naskah → menghasilkan 1 file `.mp4` valid (cek `ffprobe`).
4. **Laporan** disimpan ke `C:\Users\arija\ziyan_video_pipeline_report.md`.

## 3. Cara Menjalankan

```bat
cd C:\Users\arija
python3 make_video_pipeline.py            # proses SEMUA naskah .txt
python3 make_video_pipeline.py --one       # hanya 1 naskah (cepat/tes)
python3 make_video_pipeline.py --content <folder> --out <folder_output>
```

Output per naskah `<nama>.mp3` + `<nama>.mp4` disimpan di `C:\Users\arija\ziyan_videos\`.

## 4. Hasil Test (1 naskah)

- **Naskah:** `ai_is_changing_business.txt`
- **Audio:** `ai_is_changing_business.mp3` (45.9 detik, 718 KB)
- **Video:** `ai_is_changing_business.mp4` (6.2 MB)

Verifikasi `ffprobe` (validasi independen):

```
format_name = mov,mp4,m4a,3gp,3g2,mj2
duration    = 45.852018 s

stream #0  video  h264   1080x1920  r_frame_rate=30/1
stream #1  audio  aac     sample_rate=22050 Hz  channels=1
```

✅ Kontainer MP4 valid, punya stream video (h264, portrait 1080×1920, 30 fps) **dan** stream audio (AAC), durasi sama dengan narasi.

## 5. Isu yang Ditemukan & Solusi

| Isu | Penyebab | Solusi |
|-----|----------|--------|
| `pyttsx3` gagal import (`No module named 'pywintypes'`) | Terminal hermes menyuntikkan venv `hermes-agent` ke `PYTHONPATH`; stub `pythoncom` rusak di venv tersebut menutupi `pywin32` asli. Selain itu `pip` menganggap `pywin32` "sudah ada" (di venv hermes) sehingga tidak memasangnya untuk Python 3.13. | 1) Pasang `pywin32` asli ke Python 3.13 dengan `PYTHONPATH=` dikosongkan (`python3 -m pip install --force-reinstall --no-deps pywin32`).<br>2) Script membersihkan path venv asing (`hermes-agent`) dari `sys.path` **sebelum** import `pyttsx3`, sehingga aman dijalankan di environment hermes maupun biasa. |
| Background `gradients` 1080×1920 untuk klip 46 detik > 60 detik (timeout) | Filter gradient berat di resolusi penuh. | Render gradient di **setengah resolusi** (540×960) lalu `scale` ke 1080×1920, plus encode `libx264 -preset ultrafast -threads 0`. Waktu render turun drastis, output tetap 1080×1920. |

## 6. File yang Dibuat / Dimodifikasi

- `C:\Users\arija\make_video_pipeline.py` — script pipeline utama.
- `C:\Users\arija\ziyan_content_day1\ai_is_changing_business.txt` — dummy narasi (jika naskah lain belum ada).
- `C:\Users\arija\ziyan_videos\ai_is_changing_business.mp3` — hasil TTS.
- `C:\Users\arija\ziyan_videos\ai_is_changing_business.mp4` — **hasil akhir (valid)**.
- `C:\Users\arija\ziyan_video_pipeline_report.md` — laporan ini.

## 7. Catatan & Saran

- **Audio 22.05 kHz mono:** SAPI5 (pyttsx3) default output 22.05 kHz. Cukup untuk narasi voice-over. Bila ingin kualitas lebih tinggi, bisa di-upsample ke 44.1/48 kHz di tahap MP3 (tidak menambah informasi nyata, hanya standar Platform).
- **Memproses semua naskah:** jalankan tanpa `--one`; script akan menghasilkan 1 `.mp4` per `.txt` (kecuali file `.md` seperti `blog_1.md` yang sengaja diabaikan karena bukan naskah `.txt`).
- **Tidak ada credential** yang dicetak di script maupun laporan ini.
- Pipeline sepenuhnya lokal: `ffmpeg` + `ffprobe` (WinGet gyan build 8.1.1) dan `pyttsx3`/SAPI5 sudah tersedia di disk.
