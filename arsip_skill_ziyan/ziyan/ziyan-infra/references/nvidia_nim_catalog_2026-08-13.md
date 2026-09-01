# NVIDIA NIM Catalog Snapshot — 2026-08-13

## Akses
- Listing models: `GET https://integrate.api.nvidia.com/v1/models` → 200 OK, 87 model.
- Inference: `POST https://integrate.api.nvidia.com/v1/chat/completions` → **404 page not found** untuk akun/tier ini.
- Auth: header `Authorization: Bearer nvapi-...` valid untuk listing, tidak untuk inference.

## Model Terdeteksi (subset relevan ZIYAN)
- `nvidia/nemotron-3.5-lightning-30b-a3b` — agentic, fastest 30B MoE.
- `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` — omni-modal image/video/speech/text.
- `nvidia/riva-translate-4b-instruct-v2` — translation 37 bahasa.
- `nvidia/nemotron-3-embed-1b` — embedding RAG.
- `meta/muse-glimmer-30b` — multimodal reasoning text+image.
- `z-ai/glm-5.2` — agentic workflows, coding.
- `poolside/laguna-xs-2.1` — agentic coding 33B MoE.
- `thinkingmachines/inkling` — multimodal MoE 256-expert.

## Status 9Router
- Beberapa model NVIDIA sudah ada via OpenRouter free: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`, `openrouter/nvidia/nemotron-3-super-120b-a12b:free`, `openrouter/nvidia/nemotron-3-nano-30b-a3b:free`, `openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`.
- Model `nemotron-3.5-lightning-30b-a3b`, `riva-translate-4b-instruct-v2`, `nemotron-3-embed-1b`, `inkling` belum ada di 9Router per snapshot ini.

## Rekomendasi
- Jangan tambah provider `nvidia-nim` ke Hermes untuk inference sampai endpoint inference tersedia.
- Pakai jalur 9Router/OpenRouter untuk model NVIDIA yang sudah working.
- Jika butuh model baru NVIDIA, evaluasi ulang endpoint inference NVIDIA NIM di sesi berikutnya atau via dashboard `localhost:20128`.
