# NotebookLM CLI — Pola Terverifikasi (2026-08-03)

Venv: `C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m notebooklm`
Auth file aktif: `C:\Users\arija\OneDrive\ziyan_pending\storage_state.json` (70 cookie, SID lengkap).

## Verifikasi auth
```
python -m notebooklm list
```
→ Daftar notebook muncul = auth OK. Error "Authentication expired" = cookie mati.

## Daftar perintah nyata (terbukti jalan 2026-08-04)
- `notebooklm create "ZIYAN_<Topik>_2026-08-04"` → return nama + `notebooklm use <ID>` tip. ID format `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.
- `notebooklm source list -n <NB_ID> --no-truncate` — list sumber (atau tanpa flag, tampil tabel)
- `notebooklm source add -n <NB_ID> --type url "<URL>"` — inject URL (web page). Loop berurutan + sleep 1-2. Kalau kena "Rate limiting or quota exceeded" → tunggu, jangan spam.
- `notebooklm generate <type> -n <NB_ID> "<prompt>"` — type: video, audio, slide-deck, infographic, report, data-table, mind-map, quiz
  - `video` → explainer 16:9 HANYA. TIDAK ada flag `--format short` (error: only explainer/brief/cinematic). Short 9:16 ADA di MOBILE APP, bukan CLI.
  - `audio` → MP3 (kadang MP4 container tapi ext .mp3, 37-43MB)
  - `data-table` WAJIB positional DESCRIPTION: `notebooklm generate data-table -n <NB_ID> "deskripsi tabel"`
  - `mind-map` TIDAK support prompt positional → pakai `--kind interactive` (sync, "Children: 6 nodes"). `note --kind note-backed` juga ada.
  - `report` → Markdown draft SEO (positional prompt).
  - `quiz` → JSON.
- `notebooklm artifact list -n <NB_ID> --json` — cek status semua artefak (type/status/id)
- `notebooklm artifact wait <ARTIFACT_ID> -n <NB_ID> --timeout 140` — poll. SHELL timeout 60s memotong; untuk wait panjang pakai cron script (lihat bawah) bukan inline.
- `notebooklm download <type> -n <NB_ID> "<OUTPUT_PATH>"` — type sama dengan generate.
  - OUTPUT_PATH posisional (bukan `--output-dir`). Contoh: `notebooklm download infographic -n <NB_ID> "C:/out/infographic.png"`
  - `slide-deck` → PDF tanpa ekstensi (rename manual ke .pdf).
  - Timeout download 60s bisa kena → jalankan satu per satu, bukan paralel.

## FREE-TIER LIMIT (KOREKSI BOS 2026-08-03 — FAKTA)
- **MAX 3 Video Overview + 3 Audio Overview PER HARI** (bukan 20-30 seperti riset agent keliru).
- Implikasi: 1 hari max 3 Long video + 3 Short (native di HP) + 3 Audio.
- Scale produksi butuh Google AI Ultra / Workspace.
- `notebooklm generate video` memakai 1 quota video; `audio` memakai 1 quota audio.

## Cron poll + auto-download (pola terbukti)
Script polling (jalankan via cronjob `*/20 * * * *`):
```python
import subprocess, os, json
VENV=r"C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
NB="<NB_ID>"; OUT=r"C:\Users\arija\ziyan_artifacts\<topik>"; os.makedirs(OUT,exist_ok=True)
d=json.loads(subprocess.run(f'"{VENV}" -m notebooklm artifact list -n "{NB}" --json',shell=True,capture_output=True,text=True,timeout=120).stdout)
for a in d.get("artifacts",[]):
    if a.get("status")!="complete": continue
    subprocess.run(f'"{VENV}" -m notebooklm artifact wait "{a["id"]}" -n "{NB}" --timeout 100',shell=True)
    subprocess.run(f'"{VENV}" -m notebooklm download {a["type"]} -n "{NB}" "{os.path.join(OUT,a["type"])}"',shell=True)
```
Lalu cron ke-2 auto-upload YouTube bila folder sudah ada 8 file.

## JANGAN PAKAI computer_use klik UI NotebookLM
Google detect → "browser not secure". Semua lewat CLI + storage_state.json. Re-auth: export cookie Chrome Netscape .txt (domain google.com+notebooklm.google.com) → convert ke storage_state.json via Python.

## 8 Artefak wajib (blueprint ZIYAN)
video, audio, slide-deck, infographic, report, data-table, mind-map, quiz.

## Gotcha rate-limit
NotebookLM batasi video/audio/slide-deck harian. Generate 8 sekaligus → 5 langsung jadi, 3 pending kena quota.
Solusi: cron poll tiap 30 mnt (`artifact wait` + auto `download` bila completed).

## JANGAN PAKAI (terbukti gagal)
- `notebooklm login --browser-cookies brave` → DPAPI error Windows
- `notebooklm login --fresh` headless di terminal → timeout (butuh Bos login di Chromium Playwright, biarkan window tertutup sendiri)
- Path `~/.notebooklm/profiles/...` → SALAH, cookie ada di OneDrive/ziyan_pending
