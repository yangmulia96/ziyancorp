# Higgsfield CLI — Reference (verified 2026-08-07)

## Package
- Correct npm name: `@higgsfield/cli` (version 1.1.20 at time of test).
  User-pasted `npm i -g @file:"higgsfield/cli`." is BROKEN (contains `@file:` artifact
  + unclosed quote) → npm 404. Always `npm view <name> version` first.
- What it is: a PAID credit-based aggregator CLI over 40+ commercial models
  (Nano Banana Pro, Veo 3.1, Kling v3, FLUX.2, Seedance 2.0, Gemini Omni Flash, etc.).
  No meaningful free tier for bulk image/video generation.

## Windows install workaround (postinstall binary download fails)
Symptom: `npm i -g @higgsfield/cli` fails at `node install.js` —
`tar: Cannot connect to higgsfield\cli\vendor\hf_1.1.20_windows_amd64.tar.gz: resolve failed`.
The install.js corrupts the path with Windows backslashes before passing to `tar`.

Fix (proven):
```
npm i -g @higgsfield/cli --ignore-scripts
CLI_DIR="C:/Users/arija/AppData/Roaming/npm/node_modules/@higgsfield/cli"
mkdir -p "$CLI_DIR/vendor"
curl -sSL -o "$CLI_DIR/vendor/hf_1.1.20_windows_amd64.tar.gz" \
  "https://github.com/higgsfield-ai/cli/releases/download/v1.1.20/hf_1.1.20_windows_amd64.tar.gz"
cd "$CLI_DIR/vendor" && tar -xzf hf_1.1.20_windows_amd64.tar.gz   # extracts hf.exe (19MB)
```
- `bin/run.js` looks for `vendor/hf.exe` (win32) — placing it there makes `higgsfield` work.
- Verify: `higgsfield --version` → `higgsfield 1.1.20 ...`.
- Bin wrapper already in PATH: `C:/Users/arija/AppData/Roaming/npm/higgsfield(.cmd|.ps1)`.

## Companion skills (9)
Repo: `higgsfield-ai/skills` — brandkit, game-generation, generate, marketplace-cards,
product-photoshoot, soul-id, video-explainer, websites, youtube-thumbnail.
```
npx --yes skills add higgsfield-ai/skills --yes
```
- DO NOT use `--global` → "PromptScript does not support global skill installation".
- `--yes` skips the interactive multi-select prompt.
- Result: symlinked into `~/.agents/skills/` (Hermes Agent reads them).

## Auth bug (vendor-side, NOT local setup)
- `higgsfield auth login` starts a loopback listener on `localhost:8765` (OAuth PKCE).
  Run it in a BACKGROUND terminal so the listener survives while the user signs in;
  hand the user the printed `https://clerk.higgsfield.ai/oauth/authorize?...` URL.
- v1.1.20 FAILS server-side:
  `Error: Authorization failed: The requested scope is invalid, unknown, or malformed.
   The OAuth 2.0 Client is not allowed to request scope 'user:'`
  Cause: Higgsfield's Clerk client requests scope `user:org:read` which is rejected.
  Listener exits code 2. This is a vendor bug — wait for fix or log in via web and
  supply token via `higgsfield auth token`. Do NOT re-attempt blindly.

## Pricing intel (for ZIYAN budget decisions)
- Higgsfield = paid credits (no free bulk generation).
- Nano Banana = Gemini Flash Image. Gemini API has a FREE TIER: free input/output tokens
  (rate-limited), Google AI Studio access free. Generate images free via AI Studio or
  Gemini API free quota. Latest model in docs: Gemini 3.1 Flash Image (Nano Banana 2).
- Decision: use Nano Banana (Gemini free tier, also in ZIYAN infra via 9router/aux gemini)
  for gratis image gen; reserve Higgsfield for premium paid video (Veo/Kling) only.

## Verification recipe when web_search / browser time out
Pricing pages are SPA / gzipped; fetch + strip tags:
```python
import urllib.request, re, html
req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
t=urllib.request.urlopen(req,timeout=30).read().decode("utf-8","ignore")
t=re.sub(r"<script.*?</script>","",t,flags=re.S)
t=re.sub(r"<[^>]+>"," ",t); t=html.unescape(t); t=re.sub(r"\s+"," ",t)
# then regex for free/$/credit/plan keywords
```
