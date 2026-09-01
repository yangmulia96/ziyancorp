---
name: ziyan-agent-patterns
description: ZIYAN durable ops — video context, 9Router, ffmpeg, n8n, bridge.
version: 1.1.0
author: ZIYAN Orchestrator
license: MIT
---

# ZIYAN Agent Patterns (Operasional Durable)

## 1. VIDEO CONTEXT RULE (dari koreksi Bos 2026-08-08)
- Jika Bos kirim video + maksud tertulis ("pelajari supaya kamu belajar X"), DELIVERABLE = tentang X, BUKAN deskripsi isi video.
- JANGAN cuma re-deskripsikan isi → Bos sudah tahu. Dia mau AGEN paham KONTEKS/tujuan.
- Video SAMA berkali (cache path beda, hash sama) → jangan bedah ulang, rujuk hasil lalu, tanya instruksi lanjut.

## 2. 9ROUTER ACCESS
- Key di env: `$HERMES_CUSTOM_9ROUTER_API_KEY` (35 char) ATAU line 44 `ziyan_keys.env` (267 char JWT).
- Base URL: `http://localhost:20128`
- Chat: `POST /v1/chat/completions` header `Authorization: Bearer $KEY`
- Streaming SSE — pakai `"stream":false` untuk dapet JSON biasa.
- Web search: `/v1/models/web` kosong kalau provider (Tavily/Exa) belum di-set → pakai DuckDuckGo lite.
- **Model gratis stabil:** `kr/claude-sonnet-4.5`, `kr/claude-haiku-4.5`, `gemini/gemini-3.5-flash-lite`.
- **$0 MODE**: pakai combo `channel-researcher` (120 model gratis). JANGAN `openrouter` bare (tembus cloud berbayar). Lihat `references/9router_free_mode.md`.
- **Jalankan 9Router**: `bash "C:/Users/arija/AppData/Roaming/npm/9router" --tray --no-browser` (BACKGROUND, bukan `node`).

## 3. FFMPEG SINGLE IMAGE
- `ffmpeg -y -ss 00:00:02 -i video.mp4 -frames:v 1 -q:v 3 -update 1 out.jpg` (tanpa `-update 1` → error).

## 4. SUB-AGENT FALLBACK & MODEL
- JANGAN suruh sub-agent "cari di web" (sering gagal search). Orion yang riset, pass hasil ke sub-agent.
- Sub-agent model: riset → `kr/claude-haiku-4.5`; ringan → `gemini/gemini-3.5-flash-lite`.
- delegation.model wajib = `channel-researcher` (bukan `openrouter` bare).

## 5. N8N ACTIVATE / IMPORT (v2.33+)
- Import: `POST /api/v1/workflows` header `X-N8N-API-KEY` (line 44 ziyan_keys.env).
- Activate: `POST /api/v1/workflows/{id}/activate` (PATCH/PUT ditolak).
- Node `executeCommand` DIBLOKIR v2.33 → ganti `code`. n8n ~45s sebelum healthz 200.
- **Node.js version**: WAJIB Node 20/22 LTS. Node 24+ crash tanpa error (exit code 0, log kosong). Pakai Node 22.22 LTS.
- **Workflow folder wajib**: n8n 2.33 butuh `parentFolderId` di `workflow_entity`. Tanpa folder → workflow tidak muncul di UI (masih active=1 di DB tapi invisible). Fix: buat folder di tabel `folder` (butuh `projectId` dari tabel `project`), lalu `UPDATE workflow_entity SET parentFolderId=...`.
- **Credential Telegram**: n8n 2.33 BLOCK inject credential via API/DB untuk Telegram API (encrypt khusus). Harus manual klik UI (Settings → Credentials → Add → Telegram API). Tapi link credential ke workflow node BISA lewat DB: update node `credentials.telegramApi = credential_id`.
- **DB**: `C:\\Users\\arija\\.n8n\\database.sqlite` (table `workflow_entity`, `credentials_entity`, `folder`, `project`).
- **Auto-start**: `start-n8n.bat` di Startup folder pakai Node 22.22 path eksplisit.

## 6. WATCHDOG CRON
- Cron 30m cek 9router + n8n + disk, JANGAN notif kalau sehat.

## 7. ETHICS (prinsip Bos)
- Tidak ada: bobol wifi, hack, spam, impersonate. Outbound email batas 50-100/hari + unsubscribe.

## 8. CAROUSEL / HTML→PNG
- Chrome headless: `--screenshot=` butuh backslash Windows (`C:\...`); `file:///` butuh forward-slash.

## 10. FFMPEG DRAWTEXT DI WINDOWS
- Font: `fontfile='C\:/Windows/Fonts/arial.ttf'` (backslash+colon). Spasi di text → underscore. Emoji error.

## 9. GITHUB PAGES USER SITE
- URL `username.github.io` butuh repo `username.github.io`. Rename ubah semua URL.

## 11. VISION TOOL (vision_analyze) DEPENDENCY ON 9ROUTER
- Config di `config.yaml`: `auxiliary.vision.provider: custom`, `model: ag/gemini-3.6-flash-medium`, `base_url: http://127.0.0.1:20128/v1`
- **Vision HANYA jalan kalau 9Router hidup** (port 20128 + API key valid)
- Kalau 9Router mati → vision error 404 (aux model not found) — BUKAN tool rusak permanen
- Fix: start 9Router dulu (`bash 9router --tray --no-browser` + set `HERMES_CUSTOM_9ROUTER_API_KEY`)
- Rate-limit gemini (429/400 "Unable to process input image") wajar, tunggu reset ~20s atau ganti model
- `computer_use` capture SOM error di Windows (UIAccess block) — pakai browser tools atau manual screenshot untuk visual verification

## 12. VIDEO ANALYSIS PIPELINE (terverifikasi 2026-08-10)
**Pola yang JALAN:** 3 video (13MB, 4MB, 15MB) → ffmpeg extract 3 frame/video (0s, 5s, 10s) → copy ke `AppData/Local/hermes/cache/images/` → `vision_analyze` per frame → sintetis hasil.
- **ffmpeg command (Windows):** `ffmpeg -y -ss {t} -i "video.mp4" -frames:v 1 -q:v 2 "C:/tmp/frame_{t}.jpg"` (tanpa `-update 1` error, gunakan `-frames:v 1`)
- **Path vision:** HARUS di folder cache hermes (`AppData/Local/hermes/cache/images/`) — path `C:/tmp/` gagal 404
- **Rate limit:** 6 vision call beruntun → success. Bila 429 → tunggu 20s.
- **Output:** Ringkasan per video + pola konten + disimpan ke `REFERENSI_ASSET.md` sebagai aset riset.
- **Sub-agent alternative:** Bisa delegate_task riset video massal, tapi butuh file lokal + vision jalan.
- **Detail & commands:** `references/video_analysis_pipeline.md`</li>

## 15. CONTENT FACTORY ARCHITECTURE (terverifikasi 2026-08-12)
**Sumber:** 4 video YouTube (channel ADANG HDYT) + implementasi ZIYAN.
**Detail:** `references/content-factory-architecture.md`

**4 Model:**
1. **Model 1** - Image-to-Video Affiliate (Sistem 2 AI Influencer): Nano Banana → Kling/Sora → ~Rp0-5k
2. **Model 2** - Batch Sheets → Video UGC (Sistem 3 Value-First): Maya Router → Sora 2/Kling → ~Rp2.5k
3. **Model 3** - Faceless Storytelling (Tuyul Digital): OpenAI → Fal.ai (Flux+Kling) → MMAudio → FFmpeg → ~Rp43k
4. **Model 4** - Massal Zero-Cost (SKIP): DeepSeek + FFmpeg lokal → reused content risk

**Priority ZIYAN:** Sistem 2 → Model 1, Sistem 3 → Model 2, n8n orchestration both.

## 13. GATEWAY AUTO-START & SUPERVISION (akar masalah offline 2026-08-10)
**Gejala:** Gateway Discord/Telegram sering offline → WebSocket `ack_stale` → reconnect 46x. Gateway process TIDAK jalan saat diperiksa (PID tidak ada).
**Akar:** Tidak ada **process supervision** (systemd/NSSM/PM2) → kalau crash/restart laptop/memory leak → mati permanen.
**Fix permanen (perlu implementasi):**
1. **Windows Service via NSSM** (Non-Sucking Service Manager) — install gateway sebagai service Windows, auto-start boot, auto-restart crash.
2. **Atau PM2** (Node process manager) — `pm2 start gateway.py --name ziyan-gateway --watch --restart-delay 5000`.
3. **Health check cron** (no_agent) tiap 2 menit: cek `curl -s http://localhost:20128/v1/models` + gateway log → kalau mati, restart service.
4. **Environment:** `HERMES_CUSTOM_9ROUTER_API_KEY` wajib di-set di service env (bukan shell env).

## 13b. DISCORD GATEWAY TOKEN MANAGEMENT (terverifikasi 2026-08-12)
**Masalah:** Token valid via REST API tapi gateway gagal `Improper token has been passed`.
**Akar:** Gateway process cache token saat startup, tidak reload `.env` changes.
**Fix:** Kill all gateway processes → export `DISCORD_BOT_TOKEN` di shell → start gateway dengan token di env process.
**Solusi permanen:** Process supervision (NSSM/PM2) dengan env var baked in + cron health check (applied: `Hermes_Gateway_Auto` + `Hermes_Gateway_Health`).
Detail: `references/discord_gateway_token_management.md`

## 14. DISCORD GATEWAY WEBSOCKET UNHEALTHY (ack_stale) — ROOT CAUSE
**Gejala:** Gateway Discord/Telegram sering offline → WebSocket `ack_stale` → reconnect 46x. Gateway process TIDAK jalan saat diperiksa (PID tidak ada).
**Akar:** Tidak ada **process supervision** (systemd/NSSM/PM2) → kalau crash/restart laptop/memory leak → mati permanen.
**Fix permanen (perlu implementasi):**
1. **Windows Service via NSSM** (Non-Sucking Service Manager) — install gateway sebagai service Windows, auto-start boot, auto-restart crash.
2. **Atau PM2** (Node process manager) — `pm2 start gateway.py --name ziyan-gateway --watch --restart-delay 5000`.
3. **Health check cron** (no_agent) tiap 2 menit: cek `curl -s http://localhost:20128/v1/models` + gateway log → kalau mati, restart service.
4. **Environment:** `HERMES_CUSTOM_9ROUTER_API_KEY` wajib di-set di service env (bukan shell env).

## 14. DISCORD GATEWAY WEBSOCKET UNHEALTHY (ack_stale) — ROOT CAUSE
**Log pattern:** `WARNING [Discord] Discord Gateway WebSocket unhealthy (ack_stale, 1/2)` → `INFO [Discord] Connected as Hermes_bot#6835`
**Penyebab:** Discord heartbeat ack tidak terima dalam waktu (Discord butuh heartbeat tiap 41.25s, ack max 2x). Bisa karena:
- Gateway process blocked (GC, heavy LLM call, CPU spike)
- Network latency/jitter (Windows WiFi sleep, power saving)
- Single-threaded event loop blocked oleh synchronous HTTP call ke 9router/LLM
**Mitigasi:**
- Pastikan gateway jalan di **dedicated process** (tidak share thread dengan agent loop)
- Gunakan `async` HTTP client untuk 9router call (non-blocking)
- Set Discord `identify` + `heartbeat_interval` sesuai spec
- Monitor `ack_stale` count → alert kalau > 3/menit

## 12. SHARED MEMORY BRIDGE (TG↔DC↔Desktop) — perintah Bos 2026-08-09
Hermes TIDAK punya bridge bawaan (tiap platform = session terpisah). Solusi: 1 file disk + 1 cron.
- **File ingatan bersama**: `C:\Users\arija\ZIYAN_BRIDGE\SHARED_MEMORY.md` (ringkasan + 30 pesan TG/DC terakhir + keputusan). DEFAULT — kalau Bos tanya "apa di TG/DC tadi", BACA file ini + `session_search`.
- **Cron bridge**: `hermes cronjob create` tiap 30m, job `e5e90dbf44f7` ("ZIYAN Bridge TG-DC"). Prompt: baca `agent.log`, extract pesan terbaru, update SHARED_MEMORY.md, lapor ringkas.
- Baca log: `grep -E "platform=telegram|platform=discord" agent.log` → `inbound message` (msg=) & `response ready` (chars). User TG Bos = `Yang Mulia` (chat 7349146540).
- Statistik: Discord ~407, Telegram ~354 pesan. 2 bot TG: @Ziyanclipperbot ($0) + @Employeezynbot (CS).
- JANGAN edit config.yaml manual utk delegation — dilindungi. Pakai `hermes config set delegation.model "channel-researcher"`.
- Recipe + script: `references/ziyan_shared_memory_bridge.md`.

## 10c. MEMORY TOOL PITFALL (operasional)
- Memory PENUH ~2200 char. Sebelum add, KONSOLIDASI (hapus/gabung entry usang).
- `memory replace` SERING GAGAL `"content is required"` kalau new_text panjang/multiline (wrapper drop field). FALLBACK: `remove` (exact old_text) lalu `add`. Jangan loop retry replace.
- `add` gagal kalau melebihi limit → remove dulu entry lain lalu add.

## CATATAN
- ziyan-video-to-product USER-OWNED (Bos buat). Sarankan `hermes curator adopt` kalau perlu patch.
- File pendukung: ziyan_knowledge_sales_agent.md, ziyan_model_roster.md, ziyan_sop_carousel.md.
- Bridge ingatan: `references/ziyan_shared_memory_bridge.md`. $0 9Router: `references/9router_free_mode.md`.
