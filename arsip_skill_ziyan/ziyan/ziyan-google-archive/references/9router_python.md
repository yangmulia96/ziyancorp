# 9Router from Python (local AI gateway)

9Router runs at `http://127.0.0.1:20128` (local, free models). Use it from Python for
caption generation, classification, or any LLM call inside ZIYAN scripts.

## Endpoint
`POST http://127.0.0.1:20128/v1/chat/completions` (OpenAI-compatible).

## CRITICAL: API key header is REQUIRED
Without it you get `{"error":{"message":"Missing API key","type":"authentication_error"}}`.
The key lives in env `HERMES_CUSTOM_9ROUTER_API_KEY` (read it from `os.environ`; do NOT
hardcode). Send it as a Bearer header:

```python
import os, requests
key = os.environ.get("HERMES_CUSTOM_9ROUTER_API_KEY", "")
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
```

## CRITICAL: response is SSE even with stream=False
9Router returns Server-Sent-Events (`data: {json}\n`) regardless of `stream:False`.
Do NOT call `r.json()` — it raises. Parse line-by-line and accumulate `delta.content`:

```python
r = requests.post(URL, headers=headers, json={
    "model": "kr/claude-sonnet-4.5",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 300, "temperature": 0.8, "stream": False
}, timeout=40)
text = r.text
if text.strip().startswith("data:"):
    content = ""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("data:") and "[DONE]" not in line:
            try:
                obj = json.loads(line[5:].strip())
                content += obj["choices"][0]["delta"].get("content", "")
            except Exception:
                pass
    return content.strip() or fallback
return r.json()["choices"][0]["message"]["content"].strip()
```

## Confirmed working model (2026-08-15)
- `kr/claude-sonnet-4.5` — present on 9Router, free, works for caption gen.

## Gotchas
- If `curl` to `/health` returns HTML (not JSON), the server is up but `/health` returns a
  web page — use `/v1/models` to confirm model list.
- Vision 404 from Hermes `vision_analyze` is a DIFFERENT issue: set
  `hermes config set auxiliary.vision.model kr/claude-sonnet-4.5` (agent CAN run this).
