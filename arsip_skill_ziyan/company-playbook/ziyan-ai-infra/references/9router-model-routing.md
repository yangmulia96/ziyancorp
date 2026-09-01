# 9Router Model Routing — Gotchas (terbukti 2026-08-13)

Pola pemanggilan 9Router untuk generate konten (skrip/SEO) agar tidak gagal
secara silent. Berlaku untuk proxy lokal `http://127.0.0.1:20128/v1`
(OpenAI-compatible, key di env `HERMES_CUSTOM_9ROUTER_API_KEY`, header
`Authorization: Bearer $KEY` WAJIB di SETIAP request).

## 1. channel-researcher (combo) memotong output
- `channel-researcher` adalah combo riset. Ia bisa merute ke model reasoning
  (mis. `nvidia/nemotron-3-ultra-550b`).
- Gejala gagal: response `finish_reason: "length"`, `choices[0].message.content: null`,
  field `reasoning` berisi CoT panjang tapi TIDAK ADA output final.
- Akibat: skrip/SEO tidak jadi (content kosong / null).
- FIX: untuk output final (skrip video, judul, deskripsi, tag), **JANGAN** pakai
  channel-researcher. Panggil model non-reasoning secara langsung.

## 2. Prefix provider wajib
- `google/gemma-4-31b-it:free` → error `No active credentials for provider: google`
  (provider `google` TIDAK terkonfigurasi di proxy ini).
- Harus pakai prefix `openrouter/`: `openrouter/google/gemma-4-31b-it:free`.
- TAPI `openrouter/google/gemma-4-31b-it:free` sering **429 rate-limited** →
  tidak stabil untuk produksi. Hindari.

## 3. Model yang JALAN & STABIL (2026-08-13)
- ✅ `groq/llama-3.3-70b-versatile` — non-reasoning, output bersih, gratis
  (TANPA suffix `:free`), response cepat. REKOMENDASI untuk generate skrip/SEO.
- ✅ `kr/claude-haiku-4.5`, `kr/gpt-5.6-sol` — jalan di proxy ini (kr/* tersedia,
  beda dgn catatan lama "kr hindari").
- ✅ `poolside/laguna-s-2.1:free` — bila channel poolside aktif.
- ✅ `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` — stabil untuk
  reasoning ringan (output tidak bocor ke content).

## 4. Cara panggil (curl, contoh kerja)
```bash
curl -s -m 150 "http://127.0.0.1:20128/v1/chat/completions" \
  -H "Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"groq/llama-3.3-70b-versatile","temperature":0.7,"max_tokens":900,"stream":false,"messages":[{"role":"user","content":"<prompt>"}]}'
```
- `max_tokens` cukup besar (≥800) agar output final tidak kepotong — terutama
  bila model punya fase reasoning.
- Parse hasil: `choices[0].message.content` (bukan `reasoning`).

## 5. Jangan percaya daftar model statis
- `GET /v1/models` bisa berubah tiap instance. SELALU curl `/v1/models` dulu,
  pilih dari id yang muncul di respons.
- `google/*` APA ADUNYA 404 di proxy ini — jangan hardcode `google/gemma-*`.
- Rotasi: bila kena 402/429/timeout → ganti ke model free berikutnya dari
  prioritas di atas.
