# 9router SSE Response Format — Reference

## Symptom (what you see)
Calling `http://127.0.0.1:20128/v1/chat/completions` with raw `urllib`/`curl` and doing `json.loads(full_body)`:
- `json.decoder.JSONDecodeError: Extra data: line 3 column 1 (char N)` — because the body is multiple `data: {...}` lines, not one JSON object.
- OR `KeyError: 'message'` — because each chunk has `choices[0].delta.content`, not `choices[0].message.content`.

## Raw body (real capture, 2026-08-08)
```
data: {"id":"chatcmpl-1786149819588","object":"chat.completion.chunk","created":1786149819,"model":"auto","choices":[{"index":0,"delta":{"role":"assistant","content":"Halo! Ada"},"finish_reason":null}]}

data: {"id":"chatcmpl-1786149819588","object":"chat.completion.chunk","created":1786149819,"model":"auto","choices":[{"index":0,"delta":{"content":" ini"},"finish_reason":null}]}

data: {"id":"chatcmpl-1786149819588","object":"chat.completion.chunk","created":1786149819,"model":"auto","choices":[{"index":0,"delta":{},"finish_reason":"stop"}],"usage":{"kiro_credits":0.0147,"prompt_tokens":827,"completion_tokens":7,"total_tokens":834}}

```

## Correct parser (Python, raw urllib)
```python
import json, urllib.request
raw = urllib.request.urlopen(req, timeout=25).read().decode()
parts = []
for line in raw.splitlines():
    line = line.strip()
    if not line.startswith("data:"):
        continue
    payload = line[5:].strip()
    if payload in ("[DONE]", ""):
        continue
    try:
        obj = json.loads(payload)
        if "choices" in obj:
            d = obj["choices"][0].get("delta", {})
            if d.get("content"):
                parts.append(d["content"])
    except Exception:
        pass
return "".join(parts).strip()
```

## Alternative
Set request header `Accept: application/json` — 9router sometimes returns a single JSON object when explicitly asked, but SSE is the default and most reliable to parse defensively.

## Model names
9router prefixes proxied models with `kr/` (e.g. `kr/auto`, `kr/claude-haiku-4.5`). Do NOT use `openrouter/auto` or raw OpenRouter IDs like `nvidia/nemotron-...:free` — 9router will 404 on those. `kr/auto` is the safe auto-router.
