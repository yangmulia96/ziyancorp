# YouTube Clipper — CC-First Technique (terbukti 2026-08-09)

Bos punya bot `@Ziyanclipperbot` (Python, background). Awalnya pakai `faster-whisper base`
di CPU → **12 menit/video** → Telegram timeout + Bos marah "pusing/lambat".
Solusi yang BENER (cara orang bikin clipper): **pakai CC YouTube, bukan whisper**.

## TEKNIK: CC YouTube via yt-dlp (INSTAN, 0 detik)
Video YouTube banyak yang punya subtitle otomatis (CC). Extract langsung:
```bash
yt-dlp --write-auto-subs --sub-langs id,en --skip-download \
  -o "bot_work/cc_%(id)s" "https://youtu.be/VIDEO_ID"
# Hasil: bot_work/cc_<id>.id.vtt  (atau .en.vtt)
```
- Parse VTT: buang tag `<...>`, baris timestamp, header `WEBVTT`/`Kind:`/`Language:`.
- Loopam: kalau `429 Too Many Requests` (rate-limit sementara) → tunggu 20-30 detik, retry.
- CC tidak ada (video tanpa subtitle) → fallback ke whisper **tiny** (bukan base):
  `faster_whisper.WhisperModel('tiny', device='cpu', compute_type='int8')`
  → 3 menit video = ~1m23s (vs base 12 menit untuk 12 menit video).

## PIPELINE BOT (urutan benar)
1. Download video: `yt-dlp -f "bv[height<=480]+ba/best[height<=480]" -o dl.%(ext)s`
2. `get_transcript_ytid()`: cek CC dulu → kalau ada, parse VTT; kalau tidak, whisper tiny.
3. Sonnet/LLM pilih momen viral: request `model: "channel-researcher"` (combo 9Router, auto-fallback :free).
   Prompt: "Dari transcript, pilih 1 momen viral (max 45 dtk). Skor 0-100%. Caption TikTok/Reels."
4. `make_srt(segs)` → `cut_with_subs()`: ffmpeg scale 1080:1920 + burn subtitle.
   Filter: `subtitles='<path>:force_style='FontSize=28,PrimaryColour=&H00FFFF&,...'`
   Di Windows: path backslash→forwardslash, escape colon (`C\:/.../sub.srt`).
5. Compress: `ffmpeg -c:v libx264 -crf 30 -maxrate 1.5M -bufsize 3M -c:a aac -b:a 80k`.
6. Kirim Telegram: `send_video(..., read_timeout=120, write_timeout=120, connect_timeout=60)`.
   Caption MAKS 1024 char (potong kalau lewat). Fallback `send_document` kalau video gagal.

## ARSITEKTUR BOT (anti-timeout)
Handler `handle_message` JANGAN tunggu whisper. Langsung:
```python
await update.message.reply_text("⏳ Memproses... (3-12 menit)")
asyncio.create_task(process_video(chat_id, msg, context))
```
Jadi bot balas instant, proses di background.

## PITFALL
- Whisper base CPU = SALAH untuk produksi (terlalu lambat). Pakai CC atau tiny.
- Telegram caption >1024 char = error "Message caption is too long" → potong.
- Video >10MB = sering timeout → compress ke <10MB.
- `faster-whisper` di venv `clip_test/.venv` (bukan autoclip venv — autoclip gagal auth 9Router).
- JANGAN clone repo autoclip/opensource-clipping kalau alat sudah ada (langgar Rule #19 audit-first).
