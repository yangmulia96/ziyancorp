---
name: llm-structured-extraction
description: "Parse structured output from free LLM chat APIs reliably."
version: 1.0.0
license: MIT
---

# LLM Structured Output Extraction

## When to use
You prompt an LLM (especially a FREE model via a proxy like 9Router) to return
JSON or custom-delimiter sections, then parse it in code. This skill prevents the
three failure modes that silently produce empty/garbage output.

## The three failure modes

### 1. Trailing tokens after JSON
Many proxies append non-JSON text to a JSON response (e.g. 9Router appends
`data: [DONE]`). `json.loads()` FAILS with "Extra data". 
**FIX:** use `json.JSONDecoder().raw_decode(raw)[0]` — it parses the leading
JSON and ignores trailing bytes.

```python
from json import JSONDecoder
obj = JSONDecoder().raw_decode(raw_text)[0]
```

### 2. Non-JSON error body (NOT a 429)
An unsupported/invalid model name does NOT always return a JSON `{"error":...}`.
The proxy may return an **empty body or an HTML error page**, which surfaces as
`json.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` — NOT an HTTP
429. (Observed 2026-08-13: `openrouter/poolside/laguna-s-2.1:free` via 9Router
returned a non-JSON body; `groq/llama-3.3-70b-versatile` worked.)
**FIX:** wrap parsing in try/except and treat ANY exception as failure → fall
back to a known-good model. Do not assume the failure is a 429.

### 3. Delimiter whitespace drift
When you extract sections by markers like `===SCRIPT===`, the model MAY emit
`=== SCRIPT ===` (with spaces) or `===SCRIPT===` (no spaces). A parser that
matches only one spelling returns empty.
**FIX:** normalize — try both `"==={tag}==="` and `"=== {tag} ==="`, or strip
spaces around the markers before matching.

```python
def grab(text, tag):
    i = text.find(f"==={tag}===")
    if i < 0:
        i = text.find(f"=== {tag} ===")
    if i < 0:
        return ""
    j = text.find("===", i + len(f"==={tag}==="))
    return text[i + len(f"==={tag}==="): j if j > 0 else len(text)].strip()
```

## Robust call pattern (9Router free models)
1. Try the user-requested model first (honor intent).
2. On any HTTP non-2xx OR `JSONDecodeError` OR empty content → fall back to a
   verified-stable model for FINAL output (e.g. `groq/llama-3.3-70b-versatile`).
3. Always parse with `raw_decode` inside try/except.
4. For delimiter output, use the `grab()` normalizer above.

## Pitfalls
- Never trust `rc==0` / no-exception as "valid" for binary/download content —
  that is a different concern (verify magic bytes separately).
- Don't hardcode delimiter spacing; normalize.
- Don't assume a 429 when parsing fails — a bad model name yields a non-JSON body.

## References
- `references/9router-parsing.md` — concrete re-runnable Python snippet for the
  full try/except + raw_decode + model-fallback chat call.
