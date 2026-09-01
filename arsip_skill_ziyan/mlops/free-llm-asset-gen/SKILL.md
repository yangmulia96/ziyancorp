---
name: free-llm-asset-gen
description: "Generate assets via 9Router free models on Windows."
version: 1.0.0
author: Hermes autonomous (ZIYAN pipeline)
license: MIT
platforms: [windows]
---

# Free LLM Asset Generation via 9Router (Windows-native python)

## When to use
- Generating text assets (YouTube Shorts scripts, video metadata, social posts, blog drafts) through the local 9Router proxy (`http://127.0.0.1:20128/v1`) using FREE models only.
- You need a self-contained, re-runnable script that does NOT depend on `requests` (the terminal's Windows-native `python3` often lacks it).
- You want graceful degradation when the requested free model returns an empty body (Poolside/laguna is notorious for this on content-sized prompts).

## Hard rules
- **Use stdlib `urllib.request`, NOT `requests`.** The terminal runs Windows-native `python3` (e.g. `C:\Users\...\AppData\Local\Microsoft\WindowsApps\python3.exe`); `requests` is frequently absent there. `urllib` is always available.
- **API key via header `Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY`** (9Router default env var on this host). Without it → 401.
- **Parse with `json.JSONDecoder().raw_decode(raw)[0]`, never `json.loads`.** 9Router appends trailing text (`data: [DONE]`) to chat completions; `json.loads` raises "Extra data".
- **Ask for DELIMITED per-line output** (`SCRIPT:`, `TITLE:`, `X1:`…), one value per line, NO newlines inside a value, NO markdown. Extract with `re.match(r'^([A-Z0-9]+):\s*(.*)$', line)`. Free models routinely emit literal newlines inside JSON string values or truncate JSON — delimited text is far more robust than asking for JSON.
- **Model fallback**: try `openrouter/poolside/laguna-s-2.1:free` first, but it RELIABLY returns an empty/invalid body on content-sized prompts (even though a tiny probe like "reply OK" succeeds). Wrap every call in a loop that falls back to `groq/llama-3.3-70b-versatile` on ANY exception or empty body. Treat groq as the effective primary for content generation — do not retry laguna more than twice.
- **Enforce output constraints** (e.g. word count) with a second targeted call: if the first script is too short/long, call again with "expand/compress to N words, return only SCRIPT:" and replace.
- **Windows paths**: when invoking a Python script from the terminal, pass Windows-native paths with forward slashes (`C:/Users/arija/...`) or relative paths run from the target dir. MSYS `/c/...` paths break Windows-native python (double-drive-prefix `C:\c\...`). Single-quote backslash paths in bash so they stay literal.

## Reusable client
See `scripts/gen_assets.py` — a complete, runnable generator that calls 9Router for (1) a YouTube Short script + metadata and (2) social posts, parses the delimited output, enforces a 120–180 word script, and writes `script_short.md` + `metadata_qc.json`.

```
python3 C:/path/to/gen_assets.py --topic "..." --url "..." --outdir "C:/path/to/out"
```

## Pitfalls
- `laguna-s-2.1:free` empty-body on content prompts is NOT a one-off — expect it and rely on the groq fallback. Don't raise `max_tokens` hoping laguna recovers; let groq handle the heavy lift.
- `execute_code` is blocked for subprocess in cron mode; always use on-disk scripts + `terminal`.
- If a chat call returns a 0-byte/empty body (raised as `Expecting value: line 1 column 1`), that is the laguna empty-body failure — the broad-Exception fallback handles it; do not assume the requested model will answer.
