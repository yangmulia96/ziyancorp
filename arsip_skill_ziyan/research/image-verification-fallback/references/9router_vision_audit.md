# 9router Vision Audit (ZIYAN host, Aug 2026)

## Finding
Querying `http://127.0.0.1:20128/v1/models` (115 live models) and the saved `models9r.json` snapshot (71 models) shows:

- Vision/multimodal-capable models exist ONLY in the `gemini/` channel:
  - gemini/gemini-3.6-flash
  - gemini/gemini-3.5-flash-lite
  - gemini/gemini-3.1-pro-preview
  - gemini/gemini-3.1-flash-lite-preview
  - gemini/gemini-3-flash-preview
  - gemini/gemma-4-31b-it
- The `gemini/` channel is DEAD: every call returns `400 API key not valid`. So none of these can actually be used.
- All other channels (groq, kimi, kr, openrouter, ag, cf, root) are TEXT-ONLY or IMAGE-GENERATION only (e.g. `ag/gemini-3.1-flash-image` generates images, does not read them).

## Conclusion
No model on the free 9router proxy can READ an image. For screenshots the user sends via Discord/attachments, use OCR (tesseract — see OCR recipe in SKILL.md). Do NOT route images to 9router expecting vision.

## Fix attempt (failed — recorded so it is not repeated)
`9router` is a desktop Electron app, not a node-script entry point. `runtime/package.json` has empty `scripts` (no `start`). Killing its PID via terminal does NOT restart it — the user must open it from Start Menu/tray. Do not attempt `npm start` in `runtime/`. The `gemini/` dead channel is NOT fixed by editing the DB key (the stored key was already identical to a key that works directly against Google's API — the failure is in proxy routing, not the credential).

## Reproduce
```
curl -s http://127.0.0.1:20128/v1/models | python3 -c "import sys,json; d=json.load(sys.stdin); print([m['id'] for m in d['data'] if any(k in m['id'].lower() for k in ['vision','vl','llava','qwen-vl','pixtral','gemini'])])"
```
