---
name: ziyan-content-pipeline
description: "ZIYAN faceless content pipeline."
version: 1.0.0
author: ZIYAN Orchestrator
license: MIT
platforms: [windows, linux, macos]
---

# ZIYAN Content Pipeline (Faceless Tech/AI Channel)

Orchestrator (Parent/nous) + 4 sub-agent (RISA riset, NOVA notebooklm, FAZA video/upload,
PANDA distribusi). Semua operasi NotebookLM lewat **CLI `notebooklm-py`**, bukan klik UI.

## HARD RULES (dari koreksi Bos — jangan langgar)
1. **Agent yang CARI topik trending**, bukan Bos kasih keyword. RISA riset X/HN/arxiv →
   pilih 1 topik hot (bukti engagement nyata, bukan halu).
2. **JANGAN crop video.** NotebookLM CLI hanya bikin explainer 16:9. Short 9:16 native cuma
   ada di **mobile app / HP Bos** — Bos yang generate, agent tidak crop dari long.
3. **JANGAN computer_use klik UI NotebookLM** — Google blokir "browser not secure".
   Pakai `notebooklm-py` + `storage_state.json` (sudah terbukti).
4. **Free tier = MAX 3 Video + 3 Audio Overview / HARI.** Scale butuh Google AI Ultra/Workspace.
   Prioritas kualitas, bukan volume.
5. **Autonomous execution** — Bos benci ditanya izin mid-task. Jalankan sampai selesai
   (upload+schedule), lapor di akhir. Hanya minta persetujuan untuk hal berat/baru.

## ALUR WAJIB (tiap konten)
1. RISA: riset topik trending X/HN → pilih 1 (bukti URL valid)
2. RISA: kumpul **10 URL sumber valid** (kompetitor top organic, Bing/DuckDuckGo fetch
   langsung — JANGAN google.com yang keblokir recaptcha). Verifikasi tiap URL dgn `curl -o /dev/null -w %{http_code}`.
3. NOVA: `notebooklm create` → `source add --type url` (10x, delay 2s, agar tidak rate-limit)
4. NOVA: `generate` 8 artefak:
   - `video` (explainer 16:9, LONG only — jangan minta format short, tidak ada di CLI)
   - `audio`, `slide-deck`, `infographic`, `report` (Markdown draft), `data-table`,
     `mind-map --kind interactive`, `quiz`
5. NOVA: `artifact wait` + `download` ke `ziyan_artifacts/<topik>/`
6. FAZA: upload YouTube (private dulu, schedule besok). Guard: cek `channels?mine=true`
   sebelum upload (akun Compound Daily = UCzWib2-2CPkWo315fzucaUw).
7. PANDA: Blog (Blogger ZYN AI corp), Telegram, LinkedIn, Twitter/X, monetisasi Gumroad.

## NOTEBOOKLM CLI REFERENCE (venv Hermes)
```
VENV="C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
$VENV -m notebooklm list
$VENV -m notebooklm create "ZIYAN_Topik_YYYY-MM-DD"
$VENV -m notebooklm source add --type url -n <NB> "<url>"
$VENV -m notebooklm generate video -n <NB> "prompt"
$VENV -m notebooklm generate audio -n <NB> "prompt"
$VENV -m notebooklm generate slide-deck -n <NB> "title"
$VENV -m notebooklm generate mind-map -n <NB> --kind interactive
$VENV -m notebooklm artifact wait <id> -n <NB> --timeout 120
$VENV -m notebooklm download report -n <NB> "<out.md>"
```
- Auth: `storage_state.json` di `OneDrive/ziyan_pending`. Re-auth: export cookie Chrome
  (Netscape .txt, domain google.com+notebooklm.google.com) → convert ke storage_state.json.
- Rate-limit: inject source beri jeda 2s; kalau "Rate limiting" muncul, tunggu beberapa menit.

## BLOG SOP (embed aset)
- Cover: Infografis PNG (alt text SEO)
- Tengah: Mind Map (JSON → teks tree di MD)
- Audio: embed YouTube video (SoundCloud belum ada akun)
- Upload via Blogger token `youtube_token_ziyanmalik.json` + client `youtube_desktop_client.json`
  (scope sudah include blogger). Blog ID ZYN AI corp = 598320500315317650.

## MONETISASI
- Utama: JASA n8n ($39–149) >> Adsense. Paket PPTX+CSV+Quiz ke Gumroad/Fiverr.
- Etik: bangun portofolio dulu, jangan janjikan cuan sebelum ada buki.

## CAROUSEL / STATIC GRAPHIC (IG/LinkedIn/TikTok)
Untuk bikin carousel edukasi (bukan video), jangan pakai 9Router text-to-image (teks sering typo). Pakai **HTML → PNG via Chrome headless**:
1. Tulis HTML (1080x1080 per slide, style copy dari referensi Bos, mis. cream bg + navy text + yellow badge ala @ngoprek.ai).
2. Render per-slide: split tiap `.slide` div jadi file HTML sendiri, lalu screenshot.
3. **Chrome headless command (Windows, PATH pakai backslash):**
```
CHROME="C:\Program Files\Google\Chrome\Application\chrome.exe"
"$CHROME" --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage --screenshot="C:\Users\arija\out\slide_01.png" --window-size=1080,1080 --virtual-time-budget=3000 "file:///C:/Users/arija/slide_01.html"
```
- Path screenshot HARUS backslash (`C:\...`), bukan `/c/Users/...` (Chrome Windows tidak kenal).
- `--no-sandbox` wajib di Windows. Tanpa itu error write file.
- Playwright di venv Hermes RUSAK (greenlet missing) → jangan pakai, langsung Chrome CLI.
- Loop 8 slide via Python `subprocess` (bukan `execute_code` yg diblokir cron).

## TIKTOK AFFILIATE (tambahan 2026-08-08)
- TikTok GAK bisa auto-upload (gak ada API gratis). Agent generate video 9:16 siap post, Bos upload manual.
- Rating kreator = poin kedaluwarsa (idle = -5~8/mgg). Harus post 2x/hari. Hook 3 detik, durasi 15-21 dtk, CTA "link di bio".
- Fakta + recipe: `references/tiktok_affiliate_playbook.md`.
- Generate video slide dari foto: `references/ffmpeg_drawtext_windows.md` (escape colon `C\:/...`, hindari spasi/emoji/`+`/`:` di text=).

## PITFALL
- Jangan generate URL halu (RISA sering kasih `...` terpotong). Selalu verifikasi dgn curl.
- Jangan tanya izin tiap step — Bos marah kalau berulang.
- Shorts: jangan crop. Tunggu Bos dari HP.
- Free tier 3/hari — jadwalkan maks 3 konten/hari.
