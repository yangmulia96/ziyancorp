---
name: ziyan-zero-cost-llm
description: Keep ZIYAN LLM usage at $0 via 9Router free-tier config.
---

# ZIYAN Zero-Cost LLM Routing

Bos punya akun OpenRouter cloud berbayar. 9Router lokal (proxy laptop) bisa 100% gratis kalau dikonfigurasi benar. Salah config = saldo kepotong (nyata: $0.11 hilang karena fallback model berbayar).

## Prinsip
- Model `:free` OpenRouter = **cost $0** (quota harian, bukan saldo).
- `kr/` (Kilo), `kgw/`, `ag/`, `cf/`, `gemini/`, `groq/`, `kimi/`, `nvidia/`, `vx/`, `gc/` = provider gratis Bos (tidak lewat OpenRouter cloud).
- HANYA `openrouter/...` TANPA `:free` yang berbayar (lyria music + aneh). Dari 123 model: **120 gratis, 3 berbayar**.
- Bot & sub-agent WAJIB pakai `:free` eksplisit.

## 9Router Config = SQLite (BUKAN JSON backup)
- Aktif di `C:/Users/arija/AppData/Roaming/9router/db/data.sqlite`
- Table `combos`, kolom `models` = JSON array.
- ⚠️ `9router-backup-*.json` di home = hanya snapshot, edit di situ TIDAK mempengaruhi instance.
- Bersihkan combo jadi cuma `:free`:
  ```python
  import sqlite3, json
  db='C:/Users/arija/AppData/Roaming/9router/db/data.sqlite'
  c=sqlite3.connect(db); cur=c.cursor()
  cur.execute('SELECT id, models FROM combos')
  for rid, m in cur.fetchall():
      models=json.loads(m)
      only_free=[x for x in models if ':free' in x]
      if not only_free: only_free=['openrouter/nvidia/nemotron-3-ultra-550b-a55b:free',
        'openrouter/google/gemma-4-31b-it:free','openrouter/groq/mixtral-8x7b-32768:free']
      cur.execute('UPDATE combos SET models=? WHERE id=?', (json.dumps(only_free), rid))
  c.commit()
  ```
- Hapus combo lain: `DELETE FROM combos WHERE id<>'<main_id>'`
- **Combo ordering = intelligence priority** (Bos mau "paling pintar + gratis"): urutkan `ag/claude-opus-4-6-thinking` (top) → `kr/gpt-5.6-terra` → `kr/claude-sonnet-5` → `gc/gemini-3-pro-preview` → `kr/deepseek-3.2` → `kr/claude-haiku-4.5` → `openrouter/nemotron-3-ultra-550b-a55b:free` (quota jelas, urutan bawah). Semua `:free`.
- **REQUEST PAKAI NAMA COMBO, BUKAN MODEL SPESIFIK** → 9Router auto-fallback round-robin kalau 1 model kena rate-limit (Nvidia 32/32 wajar). Di bot/sub-agent: `model: "channel-researcher"` (bukan `openrouter/nvidia/nemotron-...:free`).
- `hermes config set delegation.model "channel-researcher"` → sub-agent ikut auto-fallback (jangan `:free` spesifik, jangan `openrouter` bare).
- Model `ag/claude-opus-4-6-thinking` = pintar tapi lambat (thinking). Buat respon cepat pakai `kr/claude-sonnet-5` (bukan thinking).
- Nemotron `:free` paling atas (priority utama) — tapi untuk auto-fallback, taruh sebagai urutan bawah karena quota harian cepat habis; biarkan opus/sonnet di atas.

## Jalankan 9Router
- ⚠️ `9router` = **bash script**, BUKAN node app. `node 9router` GAGAL (SyntaxError).
- Benar: `bash "C:/Users/arija/AppData/Roaming/npm/9router" --tray --no-browser`
- Cek: `curl -s -m5 http://127.0.0.1:20128/v1/models` (≈12s setelah start)
- Kill: `netstat -ano | grep :20128` → `taskkill /F /PID <pid>`

## SUB-AGENT (delegate_task) — PENYEBAB SALDO KEPOTONG
- Config: `~/.hermes/config.yaml` → `delegation: model: openrouter, provider: 9router`
- ⚠️ `openrouter` BARE tidak ada route di 9Router → Hermes **fallback ke OpenRouter cloud** (key `sk-or-...`) = BERBAYAR.
- FIX via CLI (jangan edit YAML manual — dilindungi):
  ```
  hermes config set delegation.model "openrouter/poolside/laguna-s-2.1:free"
  hermes config set delegation.provider 9router
  ```
- Verify: `hermes config get delegation.model` → harus `:free` eksplisit.
- Rate-limit `:free` (Nvidia 32/32) wajar, BUKAN saldo. 9Router fallback ke `:free` lain.

## PARENT MODEL (chat/planning) — HARUS GRATIS
- Parent model = yang dipakai buat chat Bos, planning, orchestration.
- Config via CLI:
  ```
  hermes config set model.default "openrouter/poolside/laguna-s-2.1:free"
  hermes config set model.provider 9router
  hermes config set model.base_url "http://127.0.0.1:20128/v1"
  ```
- Verify: `hermes config get model.default model.provider` → `openrouter/poolside/laguna-s-2.1:free` + `9router`.

## CRON JOBS — WAJIB PIN KE MODEL GRATIS
- Cron job default pakai model snapshot saat create (bisa premium).
- Pin ulang via `cronjob action=update`:
  ```
  cronjob action=update job_id=<id> model="openrouter/poolside/laguna-s-2.1:free" provider="9router"
  ```
- Cek: `cronjob action=list` → pastikan `model` & `provider` benar, bukan `null` atau premium.

## DISCORD GATEWAY TOKEN LOCATION
- Token may be stored in `Local/.env` (`C:/Users/arija/AppData/Local/hermes/.env`) while `.env` in Roaming is empty. Gateway can function even when `DISCORD_BOT_TOKEN` is not visible in the main env.
- Bot invite: OAuth2 URL Generator → scopes `bot` + permissions `Send Messages`, `Read Message History`, `Embed Links`, `Attach Files`, `Use Slash Commands`, `Read Messages/View Channels`.
- Verify Discord connected in gateway log: `[Discord] Connected as <BotName>#<discriminator>` + `✓ discord connected`.

## Bot / Script LLM
- Pakai `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (Sonnet replacement).
- curl: `http://127.0.0.1:20128/v1/chat/completions` + `-H "Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY"`
- **Python requests**: wajib header Bearer + parse SSE manual (9Router balik `data: {...}` chunk meski `stream:False`). Lihat `references/9router_requests_sse.md`.

## YouTube Transcription (CC-First, GRATIS & INSTAN)
- Whisper CPU base = 12 menit/video (lambat). Pakai **CC** kalau ada subtitle:
  `yt-dlp --write-auto-subs --sub-langs id,en --skip-download -o "out" <url>` → `out.id.vtt` (instant).
- Fallback whisper **tiny** (bukan base): ~1.5 menit / 3 menit video.

## Telegram Bot Pitfalls
- Handler jangan sync-process (polling timeout). Pakai `asyncio.create_task(process_video(...))` lalu balas "Memproses..." langsung.
- Caption max **1024 char** — potong analysis ke [:900] + "🔥 Potensi Viral: X%".
- Kirim: `send_video(..., read_timeout=120, write_timeout=120)`, fallback `send_document`.

## Verify $0
- Test response → `"usage":{"cost":0}` = aman.
- Saldo: openrouter.ai/activity harus $0 kalau cuma `:free`.

## Evidence Hierarchy & Limits
- **Primary**: live 9Router API (`/v1/models`, usage endpoints, dashboard).
- **Secondary**: `model_catalog.json`, `config.yaml`, `agent.log`.
- **Catalog ≠ inference**: model appearing in `model_catalog.json` or `config.yaml` does not prove inference works. Verify endpoint separately.
- **No usage quotas from logs alone**: Hermes logs show model names, not per-provider daily token limits. Use provider dashboards/APIs for quotas.

## Real‑Time Verification Pattern
- **SQLite combo inspection**:
  ```bash
  sqlite3 "C:/Users/arija/AppData/Roaming/9router/db/data.sqlite" "SELECT name, models FROM combos LIMIT 1" | head -3
  ```
- **Confirm channel‑researcher uses only free models** — the combo should contain `:free` models or `kr/`, `kgw/`, `cf/` providers (not `openrouter/` without `:free`).
- **Local cache evidence**:
  - `AppData/Local/hermes/cache/model_catalog.json` — cached Hermes catalog, not live 9Router state.
  - `AppData/Local/hermes/config.yaml` — registered providers/models.
  - `AppData/Local/hermes/logs/agent.log` — model/provider used in actual API calls.
- **Estimate token/credit costs realistically**: 50 Kiro credits ≈ 5–10 heavy tasks (full code review, video script + research). For ZIYAN, prioritize unlimited‑free providers (Gemini 2.5/3.5 Flash, OpenRouter `:free`, Cloudflare Workers AI) over scarce credits.

## Discord Gateway Token Location
- Token may be stored in `Local/.env` (`C:/Users/arija/AppData/Local/hermes/.env`) while `.env` in Roaming is empty. Gateway can function even when `DISCORD_BOT_TOKEN` is not visible in the main env.
- Verify actual routing with:
  ```bash
  curl -s http://localhost:20128/v1/chat/completions -H "Authorization: Bearer $KEY" -d '{"model":"channel-researcher","messages":[{"role":"user","content":"test"}],"max_tokens":5}'
  ```
  Response should come from a free provider (OpenRouter/KGW/Cloudflare).

Lihat `references/9router_commands.md` untuk command siap-pakai dan `references/nvidia-nim-evidence.md` untuk batasan inferensi NVIDIA NIM.</arg_key>
