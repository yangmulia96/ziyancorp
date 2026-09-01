# NotebookLM CLI (notebooklm-py) — Verified Commands (2026-08-03)

Venv: `C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`
Jalankan: `python -m notebooklm <subcommand>`

## Notebook
- List: `python -m notebooklm list`
- ID notebook IonQ: `3bcafeaa-c1a2-4fd9-a852-abc4c19b6a0d`

## Sources
- Add URL: `python -m notebooklm source add -n <NB> --type url <url>`
  - Contoh berhasil: 7 URL sekaligus (loop per URL karena API sequential)
- List: `python -m notebooklm source list -n <NB> --no-truncate`

## Generate Artefak
Format umum: `python -m notebooklm generate <type> -n <NB> "<prompt>"`
Types: `video`, `audio`, `slide-deck`, `infographic`, `report`, `data-table`, `mind-map`, `quiz`

- Report (draft): `python -m notebooklm generate report -n <NB> "<prompt>"`
  - TIDAK ada flag `--title` -> prompt positional saja.
- Video: `python -m notebooklm generate video -n <NB> "<prompt>" --format explainer|brief|cinematic`
  - `--format short` DITOLAK di CLI. Vertikal 9:16 ("Short") HANYA di mobile app NotebookLM.
  - Untuk Shorts: crop explainer via ffmpeg:
    `ffmpeg -i video.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:a copy shorts.mp4`
- Data table butuh prompt positional (bukan `--description`):
  `python -m notebooklm generate data-table -n <NB> "Key metrics of ..."`

## Poll & Download
- Wait: `python -m notebooklm artifact wait <id> -n <NB> --timeout 120`
- Download: `python -m notebooklm download <type> -n <NB> <output_path>`
  - Contoh: `python -m notebooklm download report -n <NB> "C:\path\out.md"`
  - `download` butuh subcommand type dulu, lalu positional path (bukan `--output-dir`).
  - Command bisa timeout 60s pada download besar — jalankan satu per satu.

## Limit (FREE tier)
- MAX 3 Video Overview + 3 Audio Overview PER HARI.
- Scale produksi butuh Google AI Ultra / Workspace.

## Auth
- Pakai `storage_state.json` (cookie Netscape export -> convert).
- JANGAN computer_use / Playwright klik UI (Google blokir "browser not secure").
- Path storage_state.json: `C:\Users\arija\OneDrive\ziyan_pending\storage_state.json`
