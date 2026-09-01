---
description: Tips integrasi Gemini API ke Hermes
---

# Gemini API Integration Tips

## Integrasi yang sudah dilakukan

1. **topic_engine.py** — sudah pakai Gemini API key
   - Model: `gemini-3.5-flash-lite` (working, diganti dari 3.6-flash yang high demand)
   - API key: di hardcode di file (panjang 53 chars)

2. **Test hasil** — model berhasil generate topik baru:
   - "Owl Adoption & Cross-Species Fostering"
   - YouTube: "Why This Killer Bird Secretly Adopted an Orphan"

## Cara pakai Gemini untuk produksi

```bash
cd C:\Users\arija\ziyancorp\scenic_wildlife_bot
python topic_engine.py  # generate topik via Gemini
```

## Model Gemini yang tersedia dan working

| Model | Status |
|-------|--------|
| `gemini-3.5-flash-lite` | ✅ Working |
| `gemini-3.1-flash-lite` | ✅ Working |
| `gemini-3-flash-preview` | ✅ Working |
| `gemini-3.6-flash` | ❌ High demand (503) |
| `gemini-2.5-flash` | ❌ Deprecated (404) |

## Fallback

Jika Gemini quota habis atau error, bisa switch ke:
- OpenRouter via 9Router (port 20128)
- Kembali ke model Solar (Hermes default)
