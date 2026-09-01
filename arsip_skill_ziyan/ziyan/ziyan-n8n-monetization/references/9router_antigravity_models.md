# 9Router Proxy — Model Antigravity (`ag/*`)

Sumber: screenshot `localhost:20128/dashboard/providers/antigravity` (akun `mziyan266@gmail.com`, status Active). Semua model di bawah **bisa dipanggil langsung** dari Hermes via:

```
POST http://127.0.0.1:20128/v1/chat/completions
Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY
Content-Type: application/json
{ "model": "ag/<nama>", "messages": [{"role":"user","content":"..."}], "max_tokens": 200 }
```

Bukan app terpisah — 9Router Proxy adalah jembatan. Antigravity = provider routing layer (Google Gemini/Claude/GPT-OSS via Google OAuth).

## Katalog (13 model, 2026-08-07)

| Model | Keluarga | Kehebatan | Paling cocok buat |
|---|---|---|---|
| `ag/gemini-3.6-flash-high` | Gemini 3.6 Flash | Tercepat + kualitas maksimal (High) | Caption, riset cepat, chat harian |
| `ag/gemini-3.6-flash-medium` | Gemini 3.6 Flash | Seimbang speed/kualitas | **Vision** (sudah tested lihat screenshot), analisa gambar |
| `ag/gemini-3.6-flash-low` | Gemini 3.6 Flash | Paling hemat, sangat cepat | Filter/klasifikasi, batch ringan |
| `ag/gemini-3.5-flash-high` | Gemini 3.5 Flash | Gen sebelumnya, masih kuat | Cadangan kalau 3.6 penuh/limit |
| `ag/gemini-3-flash-agent` | Gemini 3 Flash | Mode **agent** (multi-step, tool use) | Riset otomatis, eksekusi tugas berantai |
| `ag/gemini-3.5-flash-extra-low` | Gemini 3.5 Flash | Paling irit | Batch besar, task simpel |
| `ag/gemini-pro-agent` | Gemini 3.1 Pro | **Pro** = reasoning berat, agent | Strategi bisnis, analisa kompleks |
| `ag/gemini-3.1-pro-low` | Gemini 3.1 Pro | Pro versi lama, hemat | Cadangan reasoning |
| `ag/claude-sonnet-4-6` | Claude Sonnet 4.6 | Nulis rapi, kode bagus, thinking | **Caption estetik affiliate**, copywriting |
| `ag/claude-opus-4-6-thinking` | Claude Opus 4.6 | **Paling pintar + thinking** | Rencana strategis, reasoning sulit |
| `ag/gpt-oss-120b-medium` | GPT-OSS 120B | Open-source, gratis | Alternatif umum/kode |
| `ag/gemini-3-flash` | Gemini 3 Flash | Versi dasar stabil | Default harian |

## Rekomendasi pemakaian ZIYAN
- **Caption affiliate**: `ag/claude-sonnet-4-6` (estetik) atau `ag/gemini-3.6-flash-high` (cepat+gratis). Ganti di workflow node `AI: Generate Caption` (sekarang pakai `openrouter/auto`).
- **Vision/screenshot Bos**: `ag/gemini-3.6-flash-medium` (sudah jadi `auxiliary.vision.model` Hermes).
- **Riset/agent otomatis**: `ag/gemini-3-flash-agent` / `ag/gemini-pro-agent`.
- **Thinking berat**: `ag/claude-opus-4-6-thinking`.

## Pitfall
- Model `ag/*` di 9Router **berbeda** dengan `gemini/*` atau `kr/*` — prefix `ag/` wajib.
- Kalau `ag/*` 404 → cek di dashboard 9Router apakah provider Antigravity masih Active (OAuth bisa expire, perlu re-login di UI).
- Jangan campur dengan `9router-image` (`/v1/images/generations`) — itu endpoint gambar, beda.
