# ZIYAN Agent Roster (Model Gratis 9Router)

Update: 2026-08-08 — Model terbaik yang STABIL di 9Router (test ulang, quota lega)

## Sub-Agent (5 posisi: 4 agent + 1 Orchestrator)
| Agent | Tugas | Model 9Router | Status |
|---|---|---|---|
| RISA | Riset mendalam & trending | `kr/claude-sonnet-4.5` | ✅ pintar stabil |
| NOVA | Bangun sistem & arsitektur | `kr/claude-sonnet-4.5` | ✅ pintar stabil |
| FAZA | Video & editing | `kr/claude-haiku-4.5` | ✅ cukup |
| PANDA | Distribusi & publish | `gemini/gemini-3.5-flash-lite` | ✅ hemat |
| ORION (Orkestrator/saya) | Sintesis & keputusan | `kr/claude-sonnet-4.5` | ✅ |

## Model PINTAR yang STABIL (test 2026-08-08):
- `kr/claude-sonnet-4.5` ← paling pintar yang jalan
- `kr/deepseek-3.2` (alternatif pintar)
- `kr/claude-haiku-4.5` (cepat)
- `gemini/gemini-3.5-flash-lite` (ringan)

## Model GAGAL (quota/key 9Router Bos):
- `kr/claude-opus-4-6-thinking` (error)
- `gemini/gemini-3.1-pro-preview` (error)
- `gc/gemini-3.1-pro-preview` (error)
- `ag/gemini-pro-agent` (flaky)
- `kimi/kimi-k2.7-code` (error)

## Catatan:
- Sub-agent RISA gagal web search mandiri (delegate_task tidak kasih akses search)
  → Solusi: Orchestrator yang riset, sub-agent proses
- Semua lewat 9Router proxy (port 20128), key dari HERMES_CUSTOM_9ROUTER_API_KEY
