# API Key Status & Setup Reference

Sumber: Audit API keys di session 2026-08-12 (Hermes + n8n + ZIYAN).

---

## ✅ SUDAH SIAP & WORKING

| Provider | Key Location | Status | Used By |
|----------|--------------|--------|---------|
| **9Router** | `HERMES_CUSTOM_9ROUTER_API_KEY` (Hermes .env) | ✅ Active | LLM chat (120+ free models) |
| **Groq** | Via 9Router | ✅ Active | STT (whisper-large-v3), fast LLM |
| **Gemini** | `GEMINI_API_KEY` (Hermes .env) + 9Router | ✅ Active | Vision, text, multimodal |
| **OpenRouter** | `OPENROUTER_API_KEY` (Hermes .env) + 9Router | ✅ Active | Fallback models |
| **Vertex AI** | Via 9Router | ✅ Active | Backup Gemini |
| **Kimi** | Via 9Router (OAuth) | ✅ Active | Coding model |
| **Kiro** | Via 9Router (OAuth) | ✅ Active | Agentic model |
| **Discord Bot** | `DISCORD_BOT_TOKEN` (Hermes .env) | ✅ Valid (Ceo#5499) | Gateway |
| **Telegram Bot** | `TELEGRAM_BOT_TOKEN` (Hermes .env) | ✅ Active | Gateway + CS bot |
| **X/Twitter** | `.x_credentials` (OAuth1a) | ✅ 200 OK | Auto-post |
| **Facebook** | `OneDrive/ziyan_pending/fb_page_token.txt` | ✅ 60-day token | Auto-post FB Page |
| **YouTube** | `AppData/Local/hermes/ziyan_youtube_token.json` | ✅ Auto-refresh | Auto-upload |
| **Google Sheets** | `ziyan_google_token.json` | ✅ Refreshed | Batch processing |

---

## ❌ MISSING - CRITICAL UNTUK CONTENT FACTORY

| Provider | Dibutuhkan Untuk | Cara Dapatkan | Prioritas |
|----------|------------------|---------------|-----------|
| **Fal.ai** | Model 1 & 3 (Flux + Kling + MMAudio) | Daftar fal.ai → API Key (free credit $10-20) | **P1 - BLOKER** |
| **Kling AI** | Model 1, 2, 3 (Video generation) | Kling AI API (Kuaishou) - apply/approval | **P1 - BLOKER** |
| **Nano Banana** | Model 1 (Image editing produk) | **No official API** - workaround: Gemini/Imagen via 9Router/Vertex | **P1 - WORKAROUND** |
| **Sora 2** | Model 2 (UGC Avatar video) | OpenAI Sora - limited access/waitlist | **P2** |
| **Maya Router** | Model 2 (Prompt routing lokal) | Open source / custom n8n node | **P2** |
| **ElevenLabs** | Voiceover narasi | Key di .env tapi commented → uncomment `ELEVENLABS_API_KEY` | **P2** |

---

## SETUP CHECKLIST UNTUK ZIYAN

### Immediate (Hari Ini)
- [ ] Daftar Fal.ai → dapatkan `FAL_KEY` → add ke `.env` Hermes & n8n credentials
- [ ] Apply Kling AI API (Kuaishou) → tunggu approval
- [ ] Uncomment `ELEVENLABS_API_KEY` di `.env` Hermes

### This Week
- [ ] Setup Nano Banana workaround: test Gemini/Imagen image editing via 9Router
- [ ] Build custom n8n node untuk Maya Router (prompt routing lokal)
- [ ] Test Fal.ai endpoints: Flux, Kling, MMAudio via n8n HTTP Request

### Monitoring
- [ ] 9Router healthz check via cron (already: Midnight Snapshot)
- [ ] Token expiry tracking: FB (60 days), YT (auto), Sheets (refresh)

---

## 9Router Free Models Available (120+)

**Active Daily Drivers:**
- `channel-researcher` (combo 120+ model round-robin) ← DEFAULT
- `gemini/gemini-3.6-flash` ← Vision
- `groq/llama-3.3-70b-versatile` ← Fast text
- `groq/whisper-large-v3` ← STT

**Backup:**
- `openrouter/google/gemma-4-26b-a4b-it:free`
- `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`
- `cf/@cf/meta/llama-3.1-70b-instruct-fp8-fast`
- `nvidia/nemotron-3-ultra-550b-a55b`
- `kgw/kilo-auto/free`

**Note:** Model `kr/*` (Claude variants) sering 402 quota habis. Jangan andalkan untuk produksi.