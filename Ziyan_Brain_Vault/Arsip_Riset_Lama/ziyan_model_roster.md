# ZIYAN Model Roster — Inventori Model Gratis

Dokumen ini adalah referensi senjata AI ZIYAN. Diperbarui: 2026-08-07.
Semua model diakses lewat 9Router proxy (http://localhost:20128) — gratis.

## CARA PAKAI
- Saya (Orkestrator) baca file ini sebelum dispatch agent/task.
- Bos bisa review untuk tahu kapabilitas ZIYAN.
- Kalau 9Router restart, combo hilang → cek daftar ini untuk rebuild.

---

## 1. CHAT / TEXT (Reasoning & Coding) — ~60 model

### Reasoning Kuat (untuk agent riset, sintesis, keputusan)
- kr/claude-opus-5 (+ thinking, +agentic)
- kr/claude-opus-4.8 (+ thinking, +agentic)
- kr/claude-opus-4.7 / 4.5 (+ varian)
- kr/gpt-5.6-sol / terra / luna (+ thinking, +agentic)

### Coding (bikin/debug script, workflow)
- kr/qwen3-coder-next
- kr/deepseek-3.2
- openrouter/cohere/north-mini-code:free

### Ringan & Cepat (chat harian, draft)
- kr/claude-haiku-4.5 (+ thinking, +agentic)
- kr/claude-sonnet-5 / 4.5 (+ thinking, +agentic)
- gemini/gemini-3.6-flash
- gemini/gemini-3.5-flash-lite
- kr/glm-5, kr/MiniMax-M2.5

### Free Murni (fallback tanpa limit ketat)
- openrouter/openrouter/free
- openrouter/nvidia/nemotron-3-ultra-550b / super-120b / nano-30b / nano-omni-reasoning
- openrouter/poolside/laguna-xs-2.1 / laguna-m.1 / laguna-s-2.1 (free)
- openrouter/google/gemma-4-31b-it / gemma-4-26b-a4b-it (free)
- openrouter/inclusionai/ling-3.0-flash:free

---

## 2. VISION (Baca Gambar/Video)
Tidak ada kategori image-to-text terpisah. Gunakan **Vision Adapter** (ON di 9Router):
- ag/gemini-3.6-flash-medium
- ag/gemini-3.6-flash-low
- ag/claude-opus-4.6-thinking
- kr/claude-opus-5 / 4.8 (semua varian support vision)

**Pakai:** Bos kirim foto/screenshot → saya baca langsung via vision_analyze.

---

## 3. IMAGE GENERATION — 24 model
- gemini/gemini-3.1-flash-image-preview
- gemini/gemini-3-pro-image-preview
- gemini/gemini-2.5-flash-image
- ag/gemini-3.1-flash-image
- cf/@cf/black-forest-labs/flux-2-klein-9b / 4b / dev
- cf/@cf/black-forest-labs/flux-1-schnell
- cf/@cf/leonardo/lucid-origin / phoenix-1.0
- cf/@cf/bytedance/stable-diffusion-xl-lightning
- cf/@cf/lykon/dreamshaper-8-lcm

**Pakai:** slide carousel, thumbnail YouTube, poster produk, bg logo.

---

## 4. VIDEO GENERATION (skill: 9router-video)
- veo-3 (dan varian) — BUTUH quota Gemini (2026-08-07 gagal 429)
- Alternatif: NanoBanana image → CapCut manual

**Pakai:** video affiliate, explainer, short faceless.

---

## 5. TTS (Text-to-Speech) — 8 model
- openrouter/openai/gpt-4o-mini-tts
- openrouter/openai/tts-1-hd / tts-1
- gemini/gemini-3.1-flash-tts-preview
- gemini/gemini-2.5-flash-preview-tts / pro-preview-tts
- nvidia/fastpitch / tacotron2

**Pakai:** voiceover video, podcast, narration.

---

## 6. STT (Speech-to-Text) — 7 model
- groq/whisper-large-v3 / whisper-large-v3-turbo / distil-whisper-large-v3-en
- gemini/gemini-2.5-pro / 2.5-flash / 2.5-flash-lite / 2.0-flash

**Pakai:** transkrip video Bos, subtitle otomatis, meeting.

---

## 7. EMBEDDING — 13 model
- openrouter/openai/text-embedding-3-large / 3-small / ada-002
- openrouter/qwen/qwen3-embedding-8b
- openrouter/perplexity/pplx-embed-v1-4b / v1-0.6b
- gemini/gemini-embedding-2-preview / gemini-embedding-001 / text-embedding-005 / 004 / embedding-001

**Pakai:** RAG, pencarian semantik, knowledge base ZIYAN.

---

## 8. WEB SEARCH / FETCH (skill: 9router-web-search)
- Bukan model, tapi capability gratis untuk riset (DuckDuckGo, Exa, Tavily via 9Router).

---

## COMBO 9ROUTER (sudah ada)
| Combo | Strategi | Isi |
|---|---|---|
| channel-researcher | Fallback | openrouter/free, kr/claude-opus-4.8, kr/claude-sonnet-5, +121 more |
| openrouter | Fallback | openrouter/free, lyria-3-clip, gemma-4-31b, +11 more |

**Vision Adapter:** ON (auto-switch ke model vision kalau input gambar)
**Audio Adapter:** OFF ("No models" — belum diisi)

---

## MAPPING AGENT → MODEL
| Agent | Model | Kategori |
|---|---|---|
| RISA (riset) | 9router/riset* | Chat ringan + web |
| NOVA (notebooklm/script) | 9router/coding* | Coding |
| FAZA (video/edit) | 9router/channel-researcher | Vision + chat |
| PANDA (distribusi) | 9router/channel-researcher | Chat |
| Orion (saya) | nous/tencent/hy3:free | Parent eksklusif |

*Combo riset/coding belum dibuat di Dashboard — buat manual kalau perlu.

---

## BATASAN & PITFALL
- Veo-3: quota 429 (perlu billing Gemini)
- Audio Adapter kosong: STT jalan, TTS jalan, tapi auto-switch audio belum aktif
- Model kr/* (Kilo/Router) mungkin butuh key khusus — cek 9Router Dashboard
- Jangan pakai Opus buat task receh (boros)

---

## TOTAL: ~112 model gratis
8 kategori: Chat(60) • Vision(auto) • Image(24) • Video(veo) • TTS(8) • STT(7) • Embedding(13) • Web(skill)
