# Session 2026-08-10: Additional Resilience Pitfalls

## PITFALL #40 — VISION_ANALYZE ERROR 404/400 = 9ROUTER MATI, BUKAN TOOL RUSAK  [TERBUKTI 2026-08-10]
- GEJALA: `vision_analyze` balik `Error code: 404` / `authentication_error: Missing API key` / `400 Unable to process input image`. Agent & Bos simpulkan "vision rusak permanen, buang tool".
- ROOT CAUSE: **9Router tidak jalan** (`curl -s -m5 http://127.0.0.1:20128/health` kosong). Vision config pakai `ag/gemini-3.6-flash-medium` via 9Router proxy.
- FIX URUTAN:
  1. Cek 9Router: `curl -s -m5 http://127.0.0.1:20128/health` → kosong = mati.
  2. Nyalakan 9Router: `export HERMES_CUSTOM_9ROUTER_API_KEY=sk-... && 9router --tray --no-browser &`
  3. Tunggu health OK, lalu test vision lagi.
- Rate-limit 429/400 sesaat = kuota gemini penuh, tunggu beberapa menit (bukan rusak permanen).
- **JANGAN buang vision_analyze** — tool yang bisa diperbaiki. Config vision di `config.yaml` auxiliary.vision.model = `ag/gemini-3.6-flash-medium` sudah benar.

## PITFALL #41 — SCREEN LOCK PREVENTION TANPA ADMIN (HKCU REGISTRY)  [TERBUKTI 2026-08-10]
- GEJALA: Laptop ke-lock otomatis → 9Remote tampil "Windows is locked" → Bos tidak bisa remote.
- HKLM butuh admin. HKCU **tidak butuh admin** (agent punya akses user `arija`).
- FIX cepat (tanpa admin):
  ```
  reg add "HKCU\Control Panel\Desktop" /v ScreenSaveActive /t REG_SZ /d 0 /f
  reg add "HKCU\Control Panel\Desktop" /v ScreenSaverIsSecure /t REG_SZ /d 0 /f
  reg add "HKCU\Control Panel\Desktop" /v ScreenSaveTimeOut /t REG_SZ /d 9999 /f
  ```

## PITFALL #42 — DISCORD GATEWAY 502 = NOUS PROVIDER OVERLOAD, FALLBACK KE 9ROUTER  [TERBUKTI 2026-08-10]
- GEJALA: Log `errors.log` penuh `HTTP 502: Bad gateway — origin is overloaded` dari `provider=nous model=tencent/hy3:free`. Retry 3x gagal → user dapet "model provider failed after retries".
- ROOT CAUSE: Server inference-api.nousresearch.com overload (Cloudflare 502). Bukan bug agent.
- FIX: Ganti model default ke 9Router (`channel-researcher` combo 120 :free) yang stabil.
  ```
  hermes config set model.default channel-researcher
  hermes config set model.provider 9router
  ```
- 9Router health check: `curl -s http://127.0.0.1:20128/health` harus OK sebelum pakai.

## PITFALL #43 — N8N SILENT CRASH NODE V24 + NO-ADMIN NODE 22 FIX  [TERBUKTI 2026-08-10]
- GEJALA: `n8n start` keluar tanpa output, port 5678 tidak LISTEN, HTTP 000. DB/env OK.
- ROOT CAUSE: Node v24.16.0 tidak kompatibel n8n 2.33 (butuh Node 20/22). Crash senyap.
- FIX NO-ADMIN: Download Node 22.22.0 portable ZIP → extract → jalankan n8n dengan node 22.
  ```
  curl -L -o node22b.zip "https://nodejs.org/dist/v22.22.0/node-v22.22.0-win-x64.zip"
  unzip -q node22b.zip -d node22b
  C:\Users\arija\node22b\node-v22.22.0-win-x64\node.exe "C:\Users\arija\AppData\Local\npm-cache\_npx\<hash>\node_modules\n8n\bin\n8n" start
  ```
- Update `start-n8n.bat` pakai Node 22 path.
- Verifikasi: `netstat -ano | findstr 5678` (LISTENING) + `curl -s -o /dev/null -w "%{http_code}" localhost:5678/healthz` (200).

## PITFALL #44 — 9REMOTE LOCALHOST CONFUSION  [TERBUKTI 2026-08-10]
- SALAH: Agent sarankan ganti `localhost:5678` ke IP laptop saat Bos remote via HP → `ERR_CONNECTION_REFUSED`.
- FAKTA: 9Remote hanya menampilkan layar laptop. Browser jalan di laptop. `localhost` di situ = localhost laptop = BENAR. Refused karena n8n mati, bukan localhost salah.
- FIX: Jangan pernah suruh Bos ganti `localhost` ke IP saat remote. Cukup pastikan n8n hidup (netstat 5678 LISTENING), lalu Bos reload `localhost:5678`.