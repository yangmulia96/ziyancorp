---
name: ziyan-youtube-clipper
description: "YouTube→Shorts AI Wrapper gratis tanpa modal."
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
platforms: [windows]
---

# ZIYAN YouTube Clipper (AI Wrapper Gratis)

Bos lihat video demo bot Telegram "bungkus" API berbayar (Kling/Opus Clip). Kita bikin **versi GRATIS** (Rp 0) untuk YouTube Clipper + Caption. Motion Transfer (Kling/Luma) DIBUANG (berbayar).

## KAPABILITAS (terbukti 2026-08-09)
1. Download YouTube → `yt-dlp` 2. Transkrip → `faster-whisper` lokal
3. Pilih momen viral + caption → `9Router nemotron-3-ultra-550b:free` (GRATIS) 4. Potong 9:16 → `ffmpeg`
5. Output: video pendek siap TikTok/Reels

## STACK & PATH
- `yt-dlp`: `C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\yt-dlp`
- `ffmpeg`: di PATH (WinGet)
- `faster-whisper`: `uv venv` + `uv pip install --python .venv/Scripts/python.exe faster-whisper` (JANGAN `--system`)
- `9Router`: `http://localhost:20128/v1/chat/completions` model **`openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`** (SSE stream, **GRATIS $0**). JANGAN pakai `kr/claude-sonnet-4.5` — itu BERBAYAR (potong saldo OpenRouter cloud). Lihat `ziyan-orchestrator-discipline` Rule #9g.

## WORKFLOW
```
Telegram → n8n → yt-dlp → faster-whisper → Sonnet 4.5 → FFmpeg → Telegram
```

## MONETISASI
- Jual token Rp 35rb/10 clip, HPP Rp 0 → margin 100%
- Midtrans QRIS (gratis daftar)

## PITFALL (terbukti 2026-08-09)
- `uv pip install --system` GAGAL (Access Denied) → `uv venv` + `--python`
- 9Router = SSE → pakai `curl` parse `data: `, bukan `urllib`
- `yt-dlp` Windows: quote `-o "test.mp4"` (jangan `()`)
- 9Router flaky malam → retry 1x
- Motion Transfer = BAYAR → jangan janjikan
- **Bot Telegram balas "Memproses..." lalu "❌ Error: Timed out" (ROOT CAUSE & FIX)**: Bukan cuma `read_timeout`. Penyebab sebenarnya = handler `handle_message` menunggu whisper+ffmpeg SELESAI di dalam handler → Telegram `run_polling` timeout ~20-30 detik → bot error sebelum video jadi. FIX BENER (terbukti 2026-08-09): (1) handler LANGSUNG `reply_text` lalu `asyncio.create_task(process_video(...))` — jangan `await` proses berat di handler; (2) di `process_video` compress ke <10MB (`ffmpeg -crf 30 -maxrate 1.5M -fs 10M`); (3) kirim pakai `reply_video(..., read_timeout=120, write_timeout=120, connect_timeout=60)`; (4) `except` timeout → fallback `reply_document`. Tanpa (1), (2)+(3) tetap gagal.
- **Caption Telegram >1024 char GAGAL** ("Message caption is too long"): Sonnet sering kasih analisis panjang. FIX: potong caption ke `base_cap[:900] + analysis[:900]` lalu `if len(cap)>1024: cap=cap[:1020]+"..."`. Selalu trim sebelum `reply_video`. (Terjadi 2026-08-09 setelah fix timeout — bot balas "Memproses... Estimasi 3-12 menit" tapi video gagal kirim karena caption 78% analysis terlalu panjang.)
- **FULL PIPELINE TERBUKTI (2026-08-09)**: CC-first + whisper tiny fallback + background task + compress + caption-trim = bot @Ziyanclipperbot kirim video beneran ke Telegram ("VIDEO SENT caption: 🔥 Potensi Viral: 78%"). Ini STATE PRODUCTION. Jangan rollback ke whisper base atau hapus background task.
- **yt-dlp hasilkan `.webm` bukan `.mp4`** (merge). Jangan cek `os.path.exists("dl.mp4")` — cari `glob("dl.*")` sebagai vid_path.
- **AUDIT-FIRST (pelajaran Bos 2026-08-09)**: Bos marah "teliti dulu baik-baik dari tadi" + "pelajari tutorialnya di YouTube". JANGAN langsung clone repo baru (autoclip) atau tebak spek laptop. SEBELUM bikin/perbaiki: (1) cek tools SUDAH ada di laptop (`faster-whisper` di `clip_test/.venv`, `ffmpeg`, `yt-dlp`, `gemini` CLI, `laptop_operator/`, `dassi/`, `learnings/`, `@JengkriBot`); (2) cek spek nyata via `powershell Get-CimInstance` (laptop Bos: i5-8265U 4c/8t RAM7.8GB no-CUDA — VPS KVM4 TIDAK lebih kencang); (3) suruh sub-agent cari tutorial NYATA (YouTube transcript / blog) bukan nebak. Clone repo hanya kalau alat belum ada.
- **Transkrip CEPAT (CARA ORANG BENAR — WAJIB CC-FIRST)**: Banyak video YouTube SUDAH punya CC/auto-subtitle → extract instan via `yt-dlp --write-auto-subs --sub-langs id,en --skip-download` (hasil `.vtt`, 0 detik, tidak butuh CPU). Cek dulu ada CC sebelum jalankan whisper. YouTube bisa 429 rate-limit sementara → tunggu 20-30 detik lalu retry. Kalau CC gagal baru pakai whisper **TINY** (bukan base — base 12 menit/video = timeout Telegram). Benchmark: tiny 3 menit = 1m23s, base 12 menit = ~12 menit. **Ini root fix bot lambat** (Bos marah "12 menit cuma balas Memproses"). Recipe lengkap + parse VTT + integrasi bot.py: `references/cc_first_transcript.md`.

## AUTOCLIP REPO (alternatif opensource)
- `git clone https://github.com/artbyjazi/autoclip` — local-first, caption karaoke, face-track (MediaPipe), virality score objektif.
- **Butuh Python 3.11** (bukan 3.13, MediaPipe gak ada wheel). Laptop Bos = 3.11.15.
- Install: `uv venv --python 3.11 .venv` lalu `uv pip install --python .venv/Scripts/python.exe -e .` (dari ROOT, bukan backend/).
- **Supports 9Router sebagai OpenAI-compatible**: `config.json` → `provider: openai`, `base_url: http://localhost:20128/v1`, `model: openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`, `api_key: <9ROUTER_KEY>` (bukan "dummy" — 9Router tolak dummy, error "endpoint rejected the API key"). JANGAN pakai `kr/claude-sonnet-4.5` (BAYAR).
- CLI: `python -m autoclip.cli clip <URL> -p openai -s karaoke -r 9:16 -n 1 --centre-crop --whisper-model tiny`
- Kelemahan: whisper CPU sama lambat. Kelebihan: caption + scoring lebih bagus dari bot kita.
- **Keputusan Boss**: pakai autoclip sebagai reference, bot production tetap pipeline kita (simpel, Rp 0).

## ATURAN BOSS
- "Kau beres kan itu sampai jadi... Aku gak mau tau" → selesaikan eksekusi, JANGAN lempar step ke Boss (URL rusak = pasang redirect di server, jangan suruh Bos ganti URL/hard refresh).
- Bot harus KIRIM video (terbukti Bos terima di Telegram), bukan cuma balas "Memproses...".

## NEXT
Telegram bot (bot.py) → Midtrans → Queue → inventarisasi `ZIYAN_ASET_INVENTORY.md`
- Bot kita: `C:\Users\arija\clip_test\bot.py` (9Router `nemotron-3-ultra-550b:free` + faster-whisper + ffmpeg)
- Bot autoclip: `C:\Users\arija\clip_test\bot_autoclip.py` (wrapper CLI)

## REFERENCES
- `references/clipper_recipe.md` — working script bot.py + test_full.py
- `references/cc_first_transcript.md` — **WAJIB BACA**: CC-first transcript recipe (cara orang bikin clipper cepat, bukan whisper base lambat) + benchmark + parse VTT + integrasi bot.py
