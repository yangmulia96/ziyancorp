---
name: divisi-notebooklm-automation
description: "Generate video NotebookLM mandiri via notebooklm-py CLI."
category: ziyan
---

# Divisi NotebookLM Automation — ZIYAN

Agent generate video NotebookLM SECARA MANDIRI (tanpa Bos pegang browser) pakai library `notebooklm-py` (PyPI, unofficial RPC Google).

## Prerequisites (sudah dipasang)
- `notebooklm-py==0.7.3` di venv Hermes: `C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m notebooklm`
- Auth: cookie session dari Brave (Bos sudah login `mziyan266@gmail.com`). Disimpan di `~/.notebooklm/profiles/<profile>/storage_state.json` (jangan ke chat).

## Login 1x (Bos arahkan, agent jalankan)
```
cd C:\Users\arija
set VIRTUAL_ENV=C:\Users\arija\AppData\Local\hermes\hermes-agent\venv
python -m notebooklm login --browser-cookies brave --account mziyan266@gmail.com
```
Setelah ini, agent bisa generate tanpa interaksi. Re-auth kalau cookie expired: `notebooklm auth refresh` (atau login ulang).

## Pipeline Generate (cron harian)
1. Tentukan topik (rotasi Tech/AI/Biz/Finance, English) — dari `topic_rotation.json`.
2. Buat notebook: `notebooklm create "CD <tanggal> <topik>" --use`
3. Cari+impor sumber: `notebooklm source add-research "<topik>" --mode deep --from web --import-all --cited-only`
4. Generate video: `notebooklm generate video "<angle + audiens EN>" --format explainer --style documentary --wait --timeout 1800`
   - Shorts: `--format short`
5. Download: `notebooklm download video "C:/Users/arija/ziyan_videos/cd_<tanggal>.mp4" --latest`
6. Upload ke Compound Daily (lihat skill `divisi-youtube-ziyan`, pakai `youtube_token_compound.json`).

## Pitfalls
- **Unofficial** = risiko ToS/rate-limit. Pakai akun khusus produksi, volume wajar (3 short/hari + 3 long/minggu).
- Cookie = kredensial sensitif. Jangan ke chat/repo. Simpan di disk lokal.
- Generate >30 mnt → jadwalkan generate (pagi) & download (siang) terpisah, jangan blocking.
- Endpoint internal bisa berubah → pin versi `notebooklm-py==0.7.3`. Kalau patah, fallback Playwright / Veo Vertex.
- Explainer dukung banyak bahasa; Short historis English-only. Compound Daily = EN → aman.

## Poll & Download 8 Artefak (script pattern WAJIB)
Template teruji: `C:\Users\arija\ziyan_pending\poll_openai_math.py` (copy, ganti `NB` + `OUT`).
Aturan yang WAJIB dipatuhi (semua ini pernah bikin script gagal senyap):
- Status API = `"completed"` (BUKAN `"complete"`). Salah string → semua artefak dianggap pending.
- Subcommand download itu **kebab-case lowercase**, bukan `type` dari API:
  `Video→video`, `Audio→audio`, `Slide Deck→slide-deck`, `Infographic→infographic`,
  `Mind Map→mind-map`, `Report→report`, `Quiz→quiz`, `Data Table→data-table`.
  Pakai `download {api_type}` mentah (ada spasi/kapital) → CLI error, tapi script yang
  tidak cek returncode akan tetap print "Downloaded" padahal folder KOSONG.
- Selalu cek `rr.returncode == 0 and os.path.exists(outp)` sebelum klaim sukses.
- Target per artefak pakai `-a "<artifact_id>" --force "<path>"`.
- NotebookLM bisa keluarkan **>1 artefak tipe sama** (Video Explainer 16:9 + Video Brief 9:16).
  Beri suffix nama file kalau duplikat, kalau tidak file kedua menimpa yang pertama.
- Video/Slide Deck paling lambat (bisa >15 mnt setelah artefak lain selesai) → polling loop
  `artifact wait` + re-list, jalankan `background=true` karena foreground timeout 600s.

## Upload YouTube terjadwal
Script: `C:\Users\arija\ziyan_credentials\upload_youtube_scheduled.py`
```
python upload_youtube_scheduled.py <video.mp4> "<title>" <desc.txt> "<tags,csv>" <publishAt_ISO8601Z> [token.json]
```
- `publishAt` = UTC. WIB = UTC+7 → 14:00 WIB besok = `<besok>T07:00:00Z`.
- `privacyStatus` WAJIB `private` kalau ada `publishAt` (aturan YouTube).
- Default token = `youtube_token_compound.json` (channel Compound Daily UCzWib2-2CPkWo315fzucaUw).
  `youtube_token.json` juga Compound Daily; `youtube_token_ziyanmalik.json` = channel Ziyan Malik.
- Selalu refresh access_token dari refresh_token dulu (yang tersimpan sering expired).
- Verifikasi setelah upload: GET `videos?part=status,contentDetails&id=<id>` → cek
  `privacyStatus=private`, `publishAt` benar, `uploadStatus=uploaded`.

## Verifikasi
- `ffprobe -v error -show_entries format=duration -show_entries stream=width,height -of csv=p=0 file.mp4`
  → Explainer 1280x720 (~8 mnt), Brief 720x1280 (~70 dtk, sudah 9:16 native, TIDAK perlu crop).
- `notebooklm list` → notebook muncul
- `notebooklm artifact list --type video --json` → cek status generate
- File mp4 ada di `C:\Users\arija\ziyan_videos\` sebelum upload
