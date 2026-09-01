# 9router API Quirks (learned building ZIYAN CS bot)

Base URL: `http://127.0.0.1:20128/v1/chat/completions` (local 9router proxy).
Auth: `Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY`.

## Model naming
9router uses `kr/` prefix, NOT `openrouter/`. Valid examples:
- `kr/auto` (routes to configured best)
- `kr/claude-haiku-4.5`, `kr/claude-sonnet-4.5`, `kr/deepseek-3.2`
OpenRouter raw names like `nvidia/nemotron-3-ultra-550b-a55b:free` → 404 on 9router.

## Response format = Server-Sent Events (SSE), NOT single JSON
9router streams `data: {json}\n\n` chunks. Each chunk has `choices[0].delta.content`
(NOT `choices[0].message.content`). Final chunk has `finish_reason:"stop"`.

### WRONG parser (caused "[CS gangguan: Extra data]" / "no json")
```python
raw = urlopen(req).read().decode()
s = raw.find("{"); e = raw.rfind("}")
r = json.loads(raw[s:e+1])  # fails: multiple JSON objects / whitespace
```

### CORRECT parser
```python
raw = urlopen(req).read().decode()
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
            delta = obj["choices"][0].get("delta", {})
            if delta.get("content"):
                parts.append(delta["content"])
    except:
        pass
return "".join(parts).strip()
```

## Notes
- `kr/auto` returns `model:"auto"` in response — fine.
- Usage shows `kiro_credits` (not OpenRouter `prompt_tokens` style) — ignore for parsing.
- If 9router is down, CS bot fails silently; it is a local service that must be running.
