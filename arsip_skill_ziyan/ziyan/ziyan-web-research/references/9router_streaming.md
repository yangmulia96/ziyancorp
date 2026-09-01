# 9Router Streaming Response Parsing

Terbukti 2026-08-08: proxy 9Router (`http://localhost:20128`) mengembalikan
SSE (`text/event-stream`) untuk beberapa model (terutama `kr/claude-sonnet-4.5`),
meski body memakai `"stream": false`.

## Gejala
- `curl .../v1/chat/completions ... | python3 -c "import json; json.load(sys.stdin)"`
  → `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`
- Isi stdout mulai `data: {"id":"chatcmpl-...","object":"chat.completion.chunk",...}`

## Parser SSE (selalu pakai ini untuk 9Router)
```python
import json
text = ""
with open("/c/Users/arija/resp.json") as f:
    for line in f:
        line = line.strip()
        if line.startswith("data: "):
            try:
                d = json.loads(line[6:])
                c = d["choices"][0]["delta"].get("content", "")
                if c:
                    text += c
            except Exception:
                pass
print(text[:2000])
```

## Variabel env
- `HERMES_CUSTOM_9ROUTER_API_KEY` = key proxy 9Router (bukan key OpenRouter/Bos).
  Ambil di terminal: `KEY="$HERMES_CUSTOM_9ROUTER_API_KEY"` lalu pakai di header
  `Authorization: Bearer $KEY`.

## Model yang terbukti stream vs JSON
- `kr/claude-sonnet-4.5` → SSE (decode manual wajib)
- `gemini/gemini-3.5-flash-lite` → biasanya JSON utuh (tapi tetap amankan dengan SSE-parser)
- `kr/claude-haiku-4.5` → JSON utuh
