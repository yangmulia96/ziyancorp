# 9Router chat completions (local proxy at :20128)

## Endpoint
`POST http://127.0.0.1:20128/v1/chat/completions` (OpenAI-compatible).

## Auth
Header required:
`Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY`
The key lives in env (`HERMES_CUSTOM_9ROUTER_API_KEY`, ~35 chars). Without it:
`{"error":{"message":"Missing API key","type":"authentication_error","code":"invalid_api_key"}}`

## Streaming gotcha
9Router returns **SSE** even when you send `"stream": false`. The body is a sequence of
`data: {json}\n` lines ending with `data: [DONE]`. Do NOT call `r.json()` on the raw text —
it will raise. Parse instead:
```python
text = r.text
if text.strip().startswith("data:"):
    content = ""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("data:") and "[DONE]" not in line:
            obj = json.loads(line[5:].strip())
            content += obj["choices"][0]["delta"].get("content", "")
    caption = content.strip()
else:
    caption = r.json()["choices"][0]["message"]["content"].strip()
```

## Models seen working
`kr/claude-sonnet-4.5` (free tier) returns 200 with SSE deltas.

## Note
9Router must be running (tray / `9router --tray --no-browser`) or the request hangs/refuses.
