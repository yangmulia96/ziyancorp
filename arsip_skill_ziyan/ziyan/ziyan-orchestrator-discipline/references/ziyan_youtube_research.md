# Riset YouTube / Video References (Bos kirim link)

## Cara ambil transcript penuh (WAJIB sebelum simpulkan)
```python
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
t = api.fetch("<VIDEO_ID>", languages=["id","en"])
txt = " ".join([s.text for s in t])
```
- ID dari URL `youtu.be/<ID>` atau `watch?v=<ID>`.
- Fallback: `curl -s "https://r.jina.ai/https://www.youtube.com/watch?v=<ID>"` lalu grep kata kunci.

## Fakta Veo / Google Flow (dari riset 2026-08-08)
- Google Flow (flow.google.com) = web tool, 1000 credits/bulan (dari langganan Google AI Premium Bos). TIDAK ada API publik -> gak bisa dipakai dari n8n.
- Veo via API butuh Google AI Studio key (generativelanguage.googleapis.com) + Vertex API enabled di GCP.
- Vertex AI Veo = BERBAYAR (butuh billing/kartu kredit). Bos budget $0 kartu baru -> gak bisa Veo API otomatis.
- NanoBanana (gemini-2.5-flash-image) text-to-image bisa jalan dengan AI Studio key gratis (tanpa billing, rate-limit).
- n8n node Gemini untuk Veo butuh OAuth2 client ID/secret (bukan API key polos).

## Pola workflow n8n (dari video referensi Bos)
Telegram Trigger -> Switch (text/image/video/edit) -> Gemini node (generate image / video) -> Telegram send.
File template: ziyan_n8n_templates/ziyan_ai_media_bot.json (struktur sama, butuh GEMINI_API_KEY + billing untuk Veo).
