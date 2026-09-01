# Video Analysis Pipeline (terverifikasi 2026-08-10)

## Pola yang JALAN
**Input:** 3 video MP4 (13MB, 4MB, 15MB) dari Telegram
**Proses:**
1. `ffmpeg -y -ss {t} -i "video.mp4" -frames:v 1 -q:v 2 "C:/tmp/frame_{t}.jpg"` untuk t=0,5,10 detik
2. Copy frame ke `AppData/Local/hermes/cache/images/` (HARUS path ini, C:/tmp gagal 404)
3. `vision_analyze` per frame dengan pertanyaan spesifik
4. Sintesis hasil → simpan ke `REFERENSI_ASSET.md`

## Commands
```bash
# Extract frames (Windows)
for v in ab0d88e9d29f bd14e770417c f3693b6c7145; do
  for t in 0 5 10; do
    ffmpeg -y -ss $t -i "AppData/Local/hermes/cache/videos/video_${v}.mp4" \
      -frames:v 1 -q:v 2 "C:/tmp/${v}_$t.jpg" 2>/dev/null
  done
done
cp C:/tmp/*.jpg AppData/Local/hermes/cache/images/
```

## Vision Analyze
```python
vision_analyze(
    image_url=r"C:\Users\arija\AppData\Local\hermes\cache\images\frame.jpg",
    question="Apa isi video ini? Jelaskan visual, orang, produk, teks, aktivitas. Bahasa Indonesia."
)
```

## Output
- Ringkasan per video (tema, format, key insight)
- Pola konten yang bisa diadopsi ZIYAN
- Tersimpan permanen di `ZIYAN_TEMPLATES/REFERENSI_ASSET.md`

## Rate Limit
- 6 vision call beruntun → success
- Bila 429 → tunggu 20s
- Bisa delegate_task riset video massal jika butuh skala