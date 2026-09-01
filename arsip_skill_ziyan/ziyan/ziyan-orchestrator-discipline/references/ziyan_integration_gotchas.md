# ZIYAN Integration Gotchas (verified 2026-08-08)

Reusable fixes for integrations the orchestrator built this session. Non-transient — these are API/SDK quirks, not environment flakes.

## 1. 9router chat completions returns PADDED JSON
`http://127.0.0.1:20128/v1/chat/completions` (OpenAI-compatible) sometimes prepends many
`\r\n` / whitespace before the `{...}` and may append `data: [DONE]`. A naive `json.load(raw)`
fails with `Extra data` / `Expecting value`.

FIX (always):
```python
raw = urllib.request.urlopen(req, timeout=25).read().decode().strip()
s = raw.find("{"); e = raw.rfind("}")
r = json.loads(raw[s:e+1])
return r["choices"][0]["message"]["content"].strip()
```
Note: model string `openrouter/auto` works. Key from `HERMES_CUSTOM_9ROUTER_API_KEY`.

## 2. Telegram bot polling DROPS messages after the first
Symptom: `/start` replies, but every later message is silently ignored.
Root cause: if `getUpdates` blocks on `call_9router` (9router can take >20s) inside the
loop, or if offset isn't advanced before a long call, Telegram re-delivers / the loop
stalls and updates pile up un-acked.

FIX (robust loop):
- ACK offset IMMEDIATELY after reading `u["update_id"]` (`offset = u["update_id"] + 1`),
  BEFORE doing any LLM call.
- Spawn `threading.Thread(target=handle, ...)` for the reply so polling never blocks.
- Use `timeout=20` on getUpdates, `timeout=25` on the 9router call.

```python
while True:
    try:
        upd = json.load(urllib.request.urlopen(
            f".../getUpdates?offset={offset}&timeout=20", timeout=25))
        for u in upd.get("result", []):
            offset = u["update_id"] + 1          # ack now
            threading.Thread(target=handle,
                args=(cid, text, history), daemon=True).start()
    except Exception as e:
        time.sleep(3)
```
CS bot lives at `ziyan_corp_cs_bot.py` (bot @Employeezynbot). FROZEN per discipline §13 —
do not alter prompt/logic without explicit order.

## 3. Vite + GitHub Pages → blank white page
Symptom: deploy succeeds, HTML loads, but page is blank. Root cause: `vite.config.js`
`base:` points to a path that doesn't exist on the served site, so `/assets/*.js` 404s
and React never mounts.

Rules:
- **Project page** (`<user>.github.io/<repo>/`): `base: '/<repo>/'`  (e.g. repo `ziyancorp`
  → `base: '/ziyancorp/'`).
- **User site** (`<user>.github.io/`): `base: '/'` AND the repo MUST be named
  `<user>.github.io` (e.g. `ziyancorp.github.io`). A repo named `ziyancorp` served at the
  user-site root will 404 its assets.
- After changing `base`, ALWAYS `rm -rf dist && npm run build` (stale hashed filenames
  otherwise linger) then redeploy.
- Verify live: `curl -s <url> | grep assets` must show the SAME base as configured, and
  `curl -o /dev/null -w "HTTP: %{http_code}" <url>/assets/index-*.js` must be `200`.

Gotcha seen: repo was `ziyancorp` but `base: '/zyn-aicorp-site/'` (wrong project name
copied from history) → blank. Renaming the GitHub account/username does NOT auto-fix the
base path; rebuild+redeploy is required. Renaming `yangmulia96` → `ziyancorp` moved the
site from `yangmulia96.github.io/ziyancorp` (404 after rename) to `ziyancorp.github.io`
(needs repo `ziyancorp.github.io` + `base: '/'`).
