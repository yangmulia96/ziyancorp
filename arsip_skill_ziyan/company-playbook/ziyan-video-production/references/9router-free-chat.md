# 9Router Free-Model Chat Pattern (ZIYAN)

Reusable pattern untuk generate skrip / metadata / social via 9Router free models di script otonom (cron/Hermes).

## Aturan wajib (terbukti 2026-08-13)
1. **Parsing:** 9Router SELALU nempel trailing text (`data: [DONE]`) setelah JSON. `json.loads()` GAGAL ("Extra data"). Pakai:
   `resp, _ = json.JSONDecoder().raw_decode(raw_text)[0]`
2. **poolside/* 429 under load:** `openrouter/poolside/laguna-s-2.1:free` balikin OK di 1 call tapi **429 di call ke-2+** dalam script multi-call. JANGAN andalkan untuk batch generation — selalu sediakan fallback.
3. **Fallback stabil:** `groq/llama-3.3-70b-versatile` (via 9Router) stabil untuk skrip/SEO/metadata. Pakai sebagai fallback kalau model user 429.

## Helper chat() minimal (Python, Windows-native)
```python
import json, urllib.request, os, time

KEY = os.environ.get("HERMES_CUSTOM_9ROUTER_API_KEY")
URL = "http://127.0.0.1:20128/v1/chat/completions"
# model user dulu, lalu fallback stabil
MODELS = ["openrouter/poolside/laguna-s-2.1:free", "groq/llama-3.3-70b-versatile"]

def chat(system, user, maxtok=2000):
    last = None
    for model in MODELS:
        try:
            body = json.dumps({"model": model, "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}], "max_tokens": maxtok, "temperature": 0.6}).encode()
            req = urllib.request.Request(URL, data=body, headers={
                "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}, method="POST")
            raw = urllib.request.urlopen(req, timeout=180).read().decode("utf-8", "ignore")
            resp, _ = json.JSONDecoder().raw_decode(raw)   # WAJIB: ada trailing text
            return resp["choices"][0]["message"]["content"]
        except Exception as e:
            last = e
            time.sleep(2)
    raise RuntimeError(f"all models failed: {last}")
```

## Tips LLM → JSON
- Untuk metadata JSON, KELUARKAN teks panjang (blog/article body) dari JSON → generate sebagai call Markdown terpisah. String panjang dengan raw newline memecah `json.loads` meski sudah `raw_decode`.
- Field multi-item (thread tweet) pakai delimiter `|||`, BUKAN array JSON, agar parsing robust (split on `|||`).
- Selalu `strip_fence()` (buang ```json ... ```) sebelum parse.
- Rate-limit 429 dari poolside bersifat sementara; fallback loop di atas menangani tanpa intervensi.
