# NotebookLM Automation via notebooklm-py — Windows Recipe (verified 2026-08-01)

Riset: divisi-riset-mendalam, 1 Aug 2026. Status: terverifikasi ada, CLI jalan, install + login DIUJI di Windows.

## Fakta terverifikasi
- Package: `notebooklm-py` v0.7.3 di PyPI (author Teng Lin, MIT).
- CLI asli: `python -m notebooklm`. Subcommand ada: `generate video`, `source add-research`, `download video`, `artifact list`, `login`.
- Repo GitHub di laporan sub-agent SALAH (404) — PyPI valid. Jangan percaya URL repo dari sub-agent; verifikasi via `curl https://pypi.org/pypi/notebooklm-py/json`.

## Install ke venv Hermes (BUKAN Python sistem — env pipisan bikin login gagal di venv)
Di CMD/terminal:
```
cd C:\Users\arija
set VIRTUAL_ENV=C:\Users\arija\AppData\Local\hermes\hermes-agent\venv
uv pip install "notebooklm-py[browser]"
C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m playwright install chromium
```
Pitfall: `uv pip install --python <venv>/Scripts/python.exe <pkg>` GAGAL di Windows
(uv tidak kenali path exe sebagai env). Harus pakai env var `VIRTUAL_ENV`.

## Login (1x, Bos manual — TIDAK ada flag --master-token di CLI ini)
```
C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m notebooklm login --fresh
```
→ Chromium muncul → Bos login Google `mziyan266@gmail.com` → tutup jendela.
Cookie tersimpan di `~/.notebooklm/profiles/default/storage_state.json`.

Pitfall: `notebooklm login --browser-cookies brave|chrome` GAGAL di Windows:
"Could not decrypt brave/chrome cookies" (rookiepy tdk bisa DPAPI Brave/Chrome Windows).
Pakai `login --fresh` (launch Chromium) sebagai gantinya.

Pitfall: jangan tutup jendela sebelum login selesai →
"The browser window was closed during login" → ulang dengan `--fresh`.

## Perintah inti (alur mandiri)
```
notebooklm create "CD <tanggal> <topik>" --use
notebooklm source add-research "<topik>" --mode deep --from web --import-all --cited-only
notebooklm generate video "<angle EN>" --format explainer --style documentary --wait --timeout 1800
notebooklm download video "C:/Users/arija/ziyan_videos/cd_<tanggal>.mp4" --latest
```
- Shorts: `--format short`.
- `artifact list --type video --json` untuk polling status via cron.
- `auth refresh` untuk keepalive kalau cookie expired.

## Caveat (wajib sampaikan Bos)
1. Unofficial (reverse-engineer RPC `batchexecute`) → melanggar semangat ToS Google. Risiko: rate-limit, sesi dicabut. Mitigasi: akun khusus produksi, volume wajar (3 short/hari + 3 long/minggu), jangan paralel agresif.
2. Cookie = kredensial setara password. Simpan lokal, JANGAN lewat chat/Discord/repo.
3. Endpoint internal bisa berubah → pin `notebooklm-py==0.7.3` + fallback Playwright + alarm cron.
4. Video Overview generate >30 mnt → jadwalkan generate (pagi) & download (siang) terpisah, jangan blocking-poll.

## Alternatif (kalau RPC patah)
- `notebooklm-mcp` (roomi-fields): REST + MCP, 33 endpoint, multi-account rotation.
- Veo 3.1 via Gemini API/Vertex (`veo-3.1-generate-preview`): RESMI & legal, tapi BUKAN Video Overview (klip pendek, harus dirakit sendiri) + BERBAYAR per detik (langganan AI Pro/Ultra tidak berlaku).
- Playwright/CDP attach ke Chrome profil login: lambat & rapuh, fallback terakhir.
