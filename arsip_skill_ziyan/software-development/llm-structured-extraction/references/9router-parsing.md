# 9Router free-model chat call — robust parsing snippet

Re-runnable pattern for calling 9Router `/v1/chat/completions` and parsing the
response without silent failures. Verified 2026-08-13 on Windows host.

```python
import json, os, urllib.request
from json import JSONDecoder

KEY  = os.environ.get("HERMES_CUSTOM_9ROUTER_API_KEY", "")
URL  = "http://127.0.0.1:20128/v1/chat/completions"

def chat(model, messages, max_tokens=2000, timeout=90):
    body = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
    }, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8", "ignore")
    # trailing tokens (e.g. "data: [DONE]") -> raw_decode, NOT json.loads
    obj = JSONDecoder().raw_decode(raw)[0]
    return obj["choices"][0]["message"]["content"]

# Try user-requested model, fall back on ANY failure (incl. non-JSON body)
content = None
for m in ["openrouter/poolside/laguna-s-2.1:free", "groq/llama-3.3-70b-versatile"]:
    try:
        content = chat(m, [{"role": "user", "content": "..."}])
        if content and content.strip():
            model_used = m
            break
    except Exception as e:
        print(f"MODEL {m} failed: {e}")   # non-JSON body -> JSONDecodeError here
        continue

# Delimiter extraction (normalize whitespace)
def grab(text, tag):
    i = text.find(f"==={tag}===")
    if i < 0:
        i = text.find(f"=== {tag} ===")
    if i < 0:
        return ""
    j = text.find("===", i + len(f"==={tag}==="))
    return text[i + len(f"==={tag}==="): j if j > 0 else len(text)].strip()
```

## Notes
- `openrouter/poolside/laguna-s-2.1:free` returned a non-JSON body (HTML/empty)
  through 9Router -> `JSONDecodeError: Expecting value: line 1 column 1`. The
  fallback `groq/llama-3.3-70b-versatile` succeeded. Hence the try/except chain.
- `raw_decode` is mandatory: 9Router responses carry trailing text.
- For delimiter-delimited LLM output, always normalize spacing (see `grab`).
